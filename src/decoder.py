import os
import re
import sys
import shutil
import threading
import urllib.parse
import zipfile
from io import BytesIO
from typing import Callable, List, Optional, Tuple, TypeVar

import bs4
import requests
import time
import logging

from rich.progress import (
    Progress, SpinnerColumn, BarColumn, TextColumn,
    TimeElapsedColumn, TimeRemainingColumn,
)
from rich.console import Console

from session import SessionManager
from utils import (
    is_ioncube_file,
    find_ioncube_files,
    create_directory,
    batch_list,
    get_file_info,
)
from exceptions import (
    EasyToYouError,
    LoginError,
    UploadError,
    DownloadError,
    FormNotFoundError,
)

logger = logging.getLogger(__name__)
console = Console()

T = TypeVar("T")


class IonicubeDecoder:

    def __init__(
        self,
        username: str,
        password: str,
        decoder: str = "ic11php74",
        custom_watermark: Optional[str] = None,
        max_retries: int = 4,
    ):
        self.username = username
        self.password = password
        self.decoder = decoder
        self.max_retries = max_retries
        self.base_url = "https://easytoyou.eu"

        self.custom_watermark = custom_watermark or (
            "/*\n * Decoded by RBW-Tech\n * https://rbwtech.io\n */\n\n"
        )

        self.session_manager = SessionManager(self.base_url)

        self.not_decoded: List[str] = []
        self.processed_count = 0
        self.total_files = 0
        self._lock = threading.Lock()

    def _retry(self, fn: Callable[[], T], delays: Optional[List[int]] = None) -> T:
        if delays is None:
            delays = [5, 15, 45, 120]
        last_exc: Optional[Exception] = None
        for attempt in range(self.max_retries):
            try:
                return fn()
            except Exception as exc:
                last_exc = exc
                if attempt < self.max_retries - 1:
                    wait = delays[min(attempt, len(delays) - 1)]
                    logger.warning(f"Attempt {attempt + 1}/{self.max_retries} failed: {exc}. Retrying in {wait}s")
                    time.sleep(wait)
                else:
                    logger.error(f"All {self.max_retries} attempts exhausted: {exc}")
        raise last_exc  # type: ignore[misc]

    def _replace_watermark(self, content: bytes) -> bytes:
        try:
            content_str: str
            if isinstance(content, bytes):
                for encoding in ("utf-8", "latin-1", "cp1252"):
                    try:
                        content_str = content.decode(encoding)
                        break
                    except UnicodeDecodeError:
                        continue
                else:
                    content_str = content.decode("utf-8", errors="replace")
            else:
                content_str = content

            patterns = [
                r"/\*\s*\*\s*@\s*https://EasyToYou\.eu.*?\*/\s*\n*",
                r"/\*[^*]*\*\s*@\s*https://EasyToYou\.eu.*?\*/\s*\n*",
                r"//\s*Decoded\s*file\s*for\s*php\s*version.*?\n",
                r"/\*.*?EasyToYou\.eu.*?\*/\s*\n*",
                r"//.*?EasyToYou\.eu.*?\n",
            ]
            for pattern in patterns:
                content_str = re.sub(pattern, "", content_str, flags=re.DOTALL | re.IGNORECASE)

            content_str = re.sub(r"//\s*Decoder\s*version:.*?\n", "", content_str, flags=re.IGNORECASE)
            content_str = re.sub(r"//\s*Release:.*?\n", "", content_str, flags=re.IGNORECASE)
            content_str = re.sub(r"//\s*PHP\s*\d+\.\d+.*?\n", "", content_str, flags=re.IGNORECASE)

            php_pattern = r"(<\?php\s*)"
            if re.search(php_pattern, content_str, re.IGNORECASE):
                content_str = re.sub(
                    php_pattern, r"\1\n" + self.custom_watermark,
                    content_str, count=1, flags=re.IGNORECASE,
                )
            else:
                content_str = self.custom_watermark + content_str

            content_str = re.sub(r"\n{3,}", "\n\n", content_str)
            return content_str.encode("utf-8")

        except Exception as e:
            logger.warning(f"Watermark replacement failed: {e}")
            return content

    def replace_watermark(self, content: bytes) -> bytes:
        return self._replace_watermark(content)

    def login(self) -> bool:
        return self.session_manager.login(self.username, self.password)

    def clear_decoder_queue(self) -> None:
        cleared = 0
        for attempt in range(5):
            try:
                response = self.session_manager.get(
                    f"{self.base_url}/decoder/{self.decoder}/1", timeout=30
                )
                if response.status_code == 404:
                    break
                response.raise_for_status()

                soup = bs4.BeautifulSoup(response.content, "html.parser")
                file_inputs = soup.find_all("input", attrs={"name": "file[]"})

                if not file_inputs:
                    break

                delete_data = "&".join(
                    urllib.parse.urlencode({inp["name"]: inp["value"]})
                    for inp in file_inputs
                    if inp.get("value")
                )

                if delete_data:
                    self.session_manager.post(
                        f"{self.base_url}/decoder/{self.decoder}/1",
                        data=delete_data,
                        headers={"Content-Type": "application/x-www-form-urlencoded"},
                        timeout=30,
                    )
                    cleared += len(file_inputs)

                time.sleep(0.5)

            except Exception as e:
                logger.warning(f"Queue clear pass {attempt + 1}: {e}")
                break

        if cleared:
            logger.info(f"Queue cleared ({cleared} files removed)")

    def upload_files(self, source_dir: str, files: List[str]) -> Tuple[List[str], List[str]]:
        if not files:
            return [], []

        response = self.session_manager.get(
            f"{self.base_url}/decoder/{self.decoder}", timeout=60
        )
        response.raise_for_status()

        soup = bs4.BeautifulSoup(response.content, "html.parser")
        upload_input = (
            soup.find("input", id="uploadfileblue")
            or soup.find("input", type="file")
            or soup.find("input", attrs={"name": lambda x: x and "file" in x.lower()})
        )

        if not upload_input:
            raise FormNotFoundError("Upload form not found on page")

        input_name = upload_input.get("name", "uploadfile[]")

        file_objects = []
        upload_fields = []

        try:
            for filename in files:
                filepath = os.path.join(source_dir, filename)
                if filename.endswith(".php") and os.path.exists(filepath):
                    try:
                        fobj = open(filepath, "rb")
                        file_objects.append(fobj)
                        upload_fields.append((input_name, (filename, fobj, "application/x-php")))
                    except Exception as e:
                        logger.warning(f"Could not open {filename}: {e}")

            if not upload_fields:
                return [], files

            upload_fields.append(("submit", (None, "Decode")))

            def do_post() -> requests.Response:
                return self.session_manager.post(
                    f"{self.base_url}/decoder/{self.decoder}",
                    headers={"Referer": f"{self.base_url}/decoder/{self.decoder}"},
                    files=upload_fields,
                    timeout=120,
                )

            post_response = self._retry(do_post)
            post_response.raise_for_status()

        except Exception as e:
            logger.error(f"Upload failed: {e}")
            raise UploadError(f"Failed to upload files: {e}")
        finally:
            for fobj in file_objects:
                try:
                    fobj.close()
                except Exception:
                    pass

        return self._parse_upload_result(post_response)

    def _parse_upload_result(self, response) -> Tuple[List[str], List[str]]:
        try:
            soup = bs4.BeautifulSoup(response.content, "html.parser")
            success, failure = [], []

            for el in soup.find_all(["div", "span"], class_=["alert-success", "success"]):
                parts = el.get_text().split()
                if len(parts) > 1:
                    success.append(parts[1])

            for el in soup.find_all(["div", "span"], class_=["alert-danger", "error", "danger"]):
                parts = el.get_text().split()
                if len(parts) > 3:
                    failure.append(parts[3])

            return success, failure

        except Exception as e:
            logger.error(f"Error parsing upload result: {e}")
            return [], []

    def download_decoded_files(self, destination_dir: str) -> bool:
        create_directory(destination_dir)

        def do_download() -> bool:
            response = self.session_manager.get(
                f"{self.base_url}/download.php?id=all", timeout=120
            )
            response.raise_for_status()

            if not response.headers.get("content-type", "").startswith("application/zip"):
                raise DownloadError("Response is not a ZIP archive")

            with zipfile.ZipFile(BytesIO(response.content)) as zf:
                count = 0
                for name in zf.namelist():
                    data = zf.read(name)
                    if name.lower().endswith(".php"):
                        data = self._replace_watermark(data)
                    dest_path = os.path.join(destination_dir, os.path.basename(name))
                    with open(dest_path, "wb") as f:
                        f.write(data)
                    count += 1
                logger.info(f"Extracted {count} files")
            return True

        try:
            return self._retry(do_download)
        except Exception as e:
            logger.error(f"Download failed after all retries: {e}")
            raise DownloadError(f"Failed to download files: {e}")

    def copy_files(self, source_dir: str, dest_dir: str, files: List[str]) -> None:
        copied = 0
        for filename in files:
            try:
                src_path = os.path.join(source_dir, filename)
                dest_path = os.path.join(dest_dir, filename)
                create_directory(os.path.dirname(dest_path))
                shutil.copy2(src_path, dest_path)
                copied += 1
            except Exception as e:
                logger.warning(f"Failed to copy {filename}: {e}")
        if copied:
            logger.info(f"Copied {copied} non-PHP files")

    def _process_batch(
        self,
        source_dir: str,
        dest_dir: str,
        batch: List[str],
        batch_label: str,
        progress: Progress,
        task_id,
    ) -> bool:
        def attempt_batch() -> None:
            success, failure = self.upload_files(source_dir, batch)
            if success:
                self.download_decoded_files(dest_dir)
            if failure:
                with self._lock:
                    self.not_decoded.extend([os.path.join(source_dir, f) for f in failure])

        try:
            self._retry(attempt_batch)
            with self._lock:
                self.processed_count += len(batch)
            progress.advance(task_id, len(batch))
            return True
        except Exception as e:
            logger.error(f"{batch_label} failed: {e}")
            with self._lock:
                self.not_decoded.extend([os.path.join(source_dir, f) for f in batch])
            progress.advance(task_id, len(batch))
            return False
        finally:
            self.clear_decoder_queue()

    def process_directory_batch(
        self,
        source_dir: str,
        dest_dir: str,
        php_files: List[str],
        batch_size: int = 20,
        progress: Optional[Progress] = None,
        task_id=None,
    ) -> None:
        if not php_files:
            return

        batches = batch_list(php_files, batch_size)
        for i, batch in enumerate(batches):
            label = f"batch {i + 1}/{len(batches)} in {os.path.basename(source_dir)}"
            self._process_batch(source_dir, dest_dir, batch, label, progress, task_id)

    def decode_directory(self, source_path: str, dest_path: str, overwrite: bool = False) -> bool:
        logger.info(f"Starting decode: {source_path} -> {dest_path}")

        if not self.login():
            logger.error("Login failed")
            return False

        self.clear_decoder_queue()

        total_ioncube = find_ioncube_files(source_path)
        self.total_files = len(total_ioncube)
        logger.info(f"Found {self.total_files} ionCube files")

        work_items: List[Tuple[str, str, List[str], List[str]]] = []
        for root, _, filenames in os.walk(source_path):
            rel = os.path.relpath(root, source_path)
            dest_dir = os.path.join(dest_path, rel).rstrip(".")

            create_directory(dest_dir)

            php_files, other_files = [], []
            for filename in filenames:
                filepath = os.path.join(root, filename)
                if filename.endswith(".php") and is_ioncube_file(filepath):
                    dest_file = os.path.join(dest_dir, filename)
                    if not overwrite and os.path.exists(dest_file):
                        continue
                    php_files.append(filename)
                else:
                    other_files.append(filename)

            work_items.append((root, dest_dir, php_files, other_files))

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=40),
            TextColumn("[cyan]{task.completed}/{task.total}[/] files"),
            TimeElapsedColumn(),
            TimeRemainingColumn(),
            console=console,
            transient=False,
        ) as progress:
            task = progress.add_task("[bold]Decoding[/]", total=max(self.total_files, 1))

            for root, dest_dir, php_files, other_files in work_items:
                if other_files:
                    self.copy_files(root, dest_dir, other_files)
                if php_files:
                    self.process_directory_batch(
                        root, dest_dir, php_files, progress=progress, task_id=task
                    )

        logger.info(f"Decoded: {self.processed_count} | Failed: {len(self.not_decoded)}")

        if self.not_decoded:
            logger.warning("Failed files:")
            for f in self.not_decoded:
                logger.warning(f"  {f}")
            print("\nFailed files:", file=sys.stderr)
            for f in self.not_decoded:
                print(f"  {f}", file=sys.stderr)

        self.session_manager.close()
        return True

