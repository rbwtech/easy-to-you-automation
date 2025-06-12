"""
Main decoder class for EasyToYou IonicCube decoder
"""

import os
import shutil
import urllib.parse
import zipfile
from io import BytesIO
import requests  # FIXED: Added missing import
import bs4
import time
import logging
from typing import List, Tuple, Optional

from .session import SessionManager
from .utils import (
    is_ioncube_file, 
    find_ioncube_files, 
    create_directory, 
    batch_list,
    get_file_info
)
from .exceptions import (
    EasyToYouError,
    LoginError,
    UploadError,
    DownloadError,
    FormNotFoundError
)

logger = logging.getLogger(__name__)

class IonicubeDecoder:
    """
    Professional IonicCube decoder using easytoyou.eu service
    """
    
    def __init__(self, username: str, password: str, decoder: str = "ic11php72"):
        """
        Initialize decoder
        
        Args:
            username: easytoyou.eu username
            password: easytoyou.eu password
            decoder: Decoder version to use
        """
        self.username = username
        self.password = password
        self.decoder = decoder
        self.base_url = "https://easytoyou.eu"
        
        # Session manager
        self.session_manager = SessionManager(self.base_url)
        
        # Statistics
        self.not_decoded: List[str] = []
        self.processed_count = 0
        self.total_files = 0
        
    def login(self) -> bool:
        """
        Login to easytoyou.eu
        
        Returns:
            True if login successful
            
        Raises:
            LoginError: If login fails
        """
        return self.session_manager.login(self.username, self.password)
    
    def clear_decoder_queue(self) -> None:
        """Clear any existing files in the decoder queue"""
        logger.info("Clearing decoder queue...")
        
        try:
            max_attempts = 10
            cleared_count = 0
            
            for attempt in range(max_attempts):
                response = self.session_manager.get(
                    f"{self.base_url}/decoder/{self.decoder}/1",
                    timeout=30
                )
                response.raise_for_status()
                
                soup = bs4.BeautifulSoup(response.content, 'html.parser')
                file_inputs = soup.find_all('input', attrs={"name": "file[]"})
                
                if len(file_inputs) < 1:
                    logger.info(f"Queue cleared after {cleared_count} files")
                    break
                
                # Build deletion request
                delete_data = ""
                for input_elem in file_inputs:
                    if input_elem.get("value"):
                        delete_data += f"{urllib.parse.urlencode({input_elem['name']: input_elem['value']})}&"
                
                if delete_data:
                    headers = {"Content-Type": "application/x-www-form-urlencoded"}
                    
                    self.session_manager.post(
                        f"{self.base_url}/decoder/{self.decoder}/1",
                        data=delete_data.rstrip('&'),
                        headers=headers,
                        timeout=30
                    )
                    cleared_count += len(file_inputs)
                    logger.info(f"Cleared {len(file_inputs)} files (attempt {attempt + 1})")
                
                time.sleep(0.5)
                
        except Exception as e:
            logger.warning(f"Error clearing queue: {e}")
    
    def upload_files(self, source_dir: str, files: List[str]) -> Tuple[List[str], List[str]]:
        """
        Upload files for decoding
        
        Args:
            source_dir: Source directory path
            files: List of filenames to upload
            
        Returns:
            Tuple of (successful_files, failed_files)
            
        Raises:
            UploadError: If upload fails
        """
        if not files:
            return [], []
        
        try:
            # Get upload form
            response = self.session_manager.get(
                f"{self.base_url}/decoder/{self.decoder}",
                timeout=60
            )
            response.raise_for_status()
            
            soup = bs4.BeautifulSoup(response.content, 'html.parser')
            upload_input = soup.find('input', id="uploadfileblue")
            
            if not upload_input:
                # Try alternative selectors
                upload_input = soup.find('input', type='file')
                if not upload_input:
                    upload_input = soup.find('input', attrs={'name': lambda x: x and 'file' in x.lower()})
            
            if not upload_input:
                logger.error("Could not find upload form")
                raise FormNotFoundError("Upload form not found on page")
            
            input_name = upload_input.get('name', 'uploadfile[]')
            
            # Prepare files for upload
            upload_files = []
            for filename in files:
                filepath = os.path.join(source_dir, filename)
                if filename.endswith('.php') and os.path.exists(filepath):
                    try:
                        file_obj = open(filepath, 'rb')
                        upload_files.append((input_name, (filename, file_obj, 'application/x-php')))
                    except Exception as e:
                        logger.warning(f"Could not open file {filename}: {e}")
            
            if not upload_files:
                return [], files
            
            # Add submit button
            upload_files.append(('submit', (None, 'Decode')))
            
            # Upload files
            headers = {'Referer': f"{self.base_url}/decoder/{self.decoder}"}
            
            response = self.session_manager.post(
                f"{self.base_url}/decoder/{self.decoder}",
                headers=headers,
                files=upload_files,
                timeout=120
            )
            response.raise_for_status()
            
            # Close file objects
            for _, (_, file_obj, _) in upload_files[:-1]:
                if hasattr(file_obj, 'close'):
                    file_obj.close()
            
            return self._parse_upload_result(response)
            
        except Exception as e:
            logger.error(f"Upload failed: {e}")
            raise UploadError(f"Failed to upload files: {e}")
    
    def _parse_upload_result(self, response: requests.Response) -> Tuple[List[str], List[str]]:
        """Parse upload response to determine success/failure"""
        try:
            soup = bs4.BeautifulSoup(response.content, 'html.parser')
            success = []
            failure = []
            
            # Look for success messages
            for element in soup.find_all(['div', 'span'], class_=['alert-success', 'success']):
                text_parts = element.get_text().split()
                if len(text_parts) > 1:
                    success.append(text_parts[1])
            
            # Look for failure messages
            for element in soup.find_all(['div', 'span'], class_=['alert-danger', 'error', 'danger']):
                text_parts = element.get_text().split()
                if len(text_parts) > 3:
                    failure.append(text_parts[3])
            
            return success, failure
            
        except Exception as e:
            logger.error(f"Error parsing upload result: {e}")
            return [], []
    
    def download_decoded_files(self, destination_dir: str) -> bool:
        """
        Download decoded files as ZIP
        
        Args:
            destination_dir: Directory to extract files to
            
        Returns:
            True if download successful
            
        Raises:
            DownloadError: If download fails
        """
        try:
            create_directory(destination_dir)
            
            download_url = f"{self.base_url}/download.php?id=all"
            response = self.session_manager.get(download_url, timeout=120)
            response.raise_for_status()
            
            if response.headers.get('content-type', '').startswith('application/zip'):
                zip_data = BytesIO(response.content)
                
                with zipfile.ZipFile(zip_data) as zf:
                    extracted_count = 0
                    for name in zf.namelist():
                        data = zf.read(name)
                        dest_path = os.path.join(destination_dir, os.path.basename(name))
                        
                        with open(dest_path, 'wb') as f:
                            bytes_written = f.write(data)
                            
                        logger.info(f"Extracted {name} ({bytes_written} bytes)")
                        extracted_count += 1
                    
                    logger.info(f"Successfully extracted {extracted_count} files")
                    return True
            else:
                logger.error("Download response is not a ZIP file")
                raise DownloadError("Downloaded file is not a ZIP archive")
                
        except Exception as e:
            logger.error(f"Download failed: {e}")
            raise DownloadError(f"Failed to download files: {e}")
    
    def copy_files(self, source_dir: str, dest_dir: str, files: List[str]) -> None:
        """Copy non-PHP files to destination"""
        copied_count = 0
        for filename in files:
            try:
                src_path = os.path.join(source_dir, filename)
                dest_path = os.path.join(dest_dir, filename)
                
                # Ensure destination directory exists
                dest_parent = os.path.dirname(dest_path)
                create_directory(dest_parent)
                
                shutil.copy2(src_path, dest_path)
                copied_count += 1
                
            except Exception as e:
                logger.warning(f"Failed to copy {filename}: {e}")
        
        if copied_count > 0:
            logger.info(f"Copied {copied_count} files")
    
    def process_directory_batch(self, source_dir: str, dest_dir: str, 
                               php_files: List[str], batch_size: int = 20) -> None:
        """Process PHP files in batches"""
        if not php_files:
            return
        
        logger.info(f"Processing {len(php_files)} PHP files in batches of {batch_size}")
        
        batches = batch_list(php_files, batch_size)
        
        for i, batch in enumerate(batches):
            batch_num = i + 1
            total_batches = len(batches)
            
            logger.info(f"Processing batch {batch_num}/{total_batches} ({len(batch)} files)")
            
            try:
                success, failure = self.upload_files(source_dir, batch)
                
                if success:
                    logger.info(f"Successfully uploaded {len(success)} files")
                    
                    if self.download_decoded_files(dest_dir):
                        logger.info("Downloaded decoded files successfully")
                    else:
                        logger.warning("Download failed, adding to not_decoded list")
                        self.not_decoded.extend([os.path.join(source_dir, f) for f in batch])
                else:
                    logger.warning("No files were successfully uploaded")
                
                if failure:
                    logger.warning(f"{len(failure)} files failed to decode")
                    self.not_decoded.extend([os.path.join(source_dir, f) for f in failure])
                
                # Clear queue after each batch
                self.clear_decoder_queue()
                
                # Add delay between batches
                if batch_num < total_batches:
                    time.sleep(2)
                    
            except Exception as e:
                logger.error(f"Error processing batch {batch_num}: {e}")
                self.not_decoded.extend([os.path.join(source_dir, f) for f in batch])
    
    def decode_directory(self, source_path: str, dest_path: str, overwrite: bool = False) -> bool:
        """
        Main method to decode a directory
        
        Args:
            source_path: Source directory path
            dest_path: Destination directory path
            overwrite: Whether to overwrite existing files
            
        Returns:
            True if successful
        """
        logger.info(f"Starting decode: {source_path} -> {dest_path}")
        
        if not self.login():
            logger.error("Login failed, cannot proceed")
            return False
        
        self.clear_decoder_queue()
        
        # Count total files for progress tracking
        total_ioncube_files = find_ioncube_files(source_path)
        self.total_files = len(total_ioncube_files)
        
        logger.info(f"Found {self.total_files} ionCube encoded PHP files")
        
        for root, dirnames, filenames in os.walk(source_path):
            relative_path = os.path.relpath(root, source_path)
            dest_dir = os.path.join(dest_path, relative_path).rstrip('.')
            
            # Create destination directory
            create_directory(dest_dir)
            
            # Separate PHP and other files
            php_files = []
            other_files = []
            
            for filename in filenames:
                filepath = os.path.join(root, filename)
                
                if filename.endswith('.php') and is_ioncube_file(filepath):
                    # Check if we should skip existing files
                    dest_file = os.path.join(dest_dir, filename)
                    if not overwrite and os.path.exists(dest_file):
                        logger.info(f"Skipping existing file: {filename}")
                        continue
                    php_files.append(filename)
                else:
                    other_files.append(filename)
            
            # Copy non-PHP files
            if other_files:
                self.copy_files(root, dest_dir, other_files)
            
            # Process PHP files
            if php_files:
                self.process_directory_batch(root, dest_dir, php_files)
                self.processed_count += len(php_files)
                
                # Progress update
                if self.total_files > 0:
                    progress = (self.processed_count / self.total_files) * 100
                    logger.info(f"Progress: {self.processed_count}/{self.total_files} ({progress:.1f}%)")
        
        # Final report
        logger.info("=" * 50)
        logger.info("DECODING COMPLETE")
        logger.info(f"Total files processed: {self.processed_count}")
        logger.info(f"Files that failed to decode: {len(self.not_decoded)}")
        
        if self.not_decoded:
            logger.info("Failed files:")
            for failed_file in self.not_decoded:
                logger.info(f"  - {failed_file}")
        
        # Close session
        self.session_manager.close()
        
        return True