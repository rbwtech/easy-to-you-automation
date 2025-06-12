# API Documentation

## Package Overview

The `easytoyou` package provides a clean, object-oriented interface for IonicCube decoding using the easytoyou.eu service.

## Core Classes

### IonicubeDecoder

Main class for decoding IonicCube encrypted PHP files.

```python
from easytoyou import IonicubeDecoder

decoder = IonicubeDecoder(username, password, decoder_version)
```

#### Constructor Parameters

| Parameter  | Type  | Default       | Description            |
| ---------- | ----- | ------------- | ---------------------- |
| `username` | `str` | Required      | easytoyou.eu username  |
| `password` | `str` | Required      | easytoyou.eu password  |
| `decoder`  | `str` | `"ic11php72"` | Decoder version to use |

#### Methods

##### `login() -> bool`

Authenticate with easytoyou.eu service.

```python
success = decoder.login()
if success:
    print("Authentication successful")
```

**Returns:** `True` if login successful, `False` otherwise  
**Raises:** `LoginError` if authentication fails

##### `decode_directory(source_path, dest_path, overwrite=False) -> bool`

Decode all IonicCube files in a directory.

```python
success = decoder.decode_directory(
    source_path="./encoded_project",
    dest_path="./decoded_project",
    overwrite=True
)
```

**Parameters:**

- `source_path` (str): Path to directory containing encoded files
- `dest_path` (str): Output directory path
- `overwrite` (bool): Whether to overwrite existing files

**Returns:** `True` if successful, `False` otherwise

##### `clear_decoder_queue() -> None`

Clear any existing files in the easytoyou.eu decoder queue.

```python
decoder.clear_decoder_queue()
```

##### `upload_files(source_dir, files) -> Tuple[List[str], List[str]]`

Upload specific files for decoding.

```python
success_files, failed_files = decoder.upload_files(
    source_dir="./source",
    files=["file1.php", "file2.php"]
)
```

**Returns:** Tuple of (successful_files, failed_files)

##### `download_decoded_files(destination_dir) -> bool`

Download decoded files from easytoyou.eu.

```python
success = decoder.download_decoded_files("./output")
```

#### Properties

##### `processed_count: int`

Number of files successfully processed.

##### `not_decoded: List[str]`

List of file paths that failed to decode.

##### `total_files: int`

Total number of files to process.

## Exception Classes

### EasyToYouError

Base exception for all package-related errors.

```python
from easytoyou.exceptions import EasyToYouError

try:
    decoder.decode_directory("./source", "./output")
except EasyToYouError as e:
    print(f"Decoding error: {e}")
```

### LoginError

Raised when authentication with easytoyou.eu fails.

```python
from easytoyou.exceptions import LoginError

try:
    decoder.login()
except LoginError as e:
    print(f"Login failed: {e}")
```

### UploadError

Raised when file upload fails.

### DownloadError

Raised when file download fails.

### NetworkError

Raised when network operations fail.

### FormNotFoundError

Raised when upload form cannot be found on the page.

## Utility Functions

### File Detection

```python
from easytoyou.utils import is_ioncube_file, find_ioncube_files

# Check if single file is IonicCube encoded
if is_ioncube_file("./file.php"):
    print("File is IonicCube encoded")

# Find all IonicCube files in directory
ioncube_files = find_ioncube_files("./project")
print(f"Found {len(ioncube_files)} IonicCube files")
```

### File Operations

```python
from easytoyou.utils import create_directory, batch_list

# Create directory safely
success = create_directory("./output/nested/path")

# Split list into batches
files = ["file1.php", "file2.php", "file3.php", "file4.php"]
batches = batch_list(files, batch_size=2)
# Returns: [["file1.php", "file2.php"], ["file3.php", "file4.php"]]
```

### File Information

```python
from easytoyou.utils import get_file_info, format_file_size

# Get detailed file information
info = get_file_info("./large_file.php")
print(f"Size: {info['size_formatted']}")
print(f"IonicCube: {info['is_ioncube']}")

# Format file size
size_str = format_file_size(1048576)  # "1.0 MB"
```

## Advanced Usage Examples

### Custom Session Management

```python
from easytoyou.session import SessionManager

# Manual session management
session_manager = SessionManager("https://easytoyou.eu")
success = session_manager.login("username", "password")

if success:
    # Use session for custom requests
    response = session_manager.get("/custom-endpoint")
```

### Error Handling Strategies

```python
from easytoyou import IonicubeDecoder
from easytoyou.exceptions import LoginError, NetworkError
import time

def robust_decode(source, dest, max_retries=3):
    """Decode with automatic retry on network errors"""

    for attempt in range(max_retries):
        try:
            decoder = IonicubeDecoder("user", "pass")
            return decoder.decode_directory(source, dest)

        except LoginError:
            print("Invalid credentials - stopping")
            return False

        except NetworkError as e:
            print(f"Network error (attempt {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                time.sleep(5 * (attempt + 1))  # Exponential backoff
                continue
            return False

        except Exception as e:
            print(f"Unexpected error: {e}")
            return False

    return False
```

### Batch Processing with Progress Tracking

```python
from easytoyou import IonicubeDecoder
from easytoyou.utils import find_ioncube_files, batch_list

def batch_decode_with_progress(source_dir, output_dir):
    """Decode with detailed progress tracking"""

    # Find all files first
    ioncube_files = find_ioncube_files(source_dir)
    print(f"Found {len(ioncube_files)} IonicCube files")

    # Initialize decoder
    decoder = IonicubeDecoder("username", "password")
    if not decoder.login():
        return False

    # Process in batches
    batches = batch_list(ioncube_files, 20)

    for i, batch in enumerate(batches):
        print(f"Processing batch {i+1}/{len(batches)}")

        try:
            success, failed = decoder.upload_files(source_dir, batch)
            print(f"  Success: {len(success)}, Failed: {len(failed)}")

            if success:
                decoder.download_decoded_files(output_dir)

        except Exception as e:
            print(f"  Batch {i+1} failed: {e}")
            continue

    print(f"Total processed: {decoder.processed_count}")
    print(f"Total failed: {len(decoder.not_decoded)}")

    return True
```

### Integration with Existing Applications

```python
import logging
from pathlib import Path
from easytoyou import IonicubeDecoder

class ProjectDecoder:
    """Integration class for existing applications"""

    def __init__(self, credentials_file="credentials.json"):
        self.logger = logging.getLogger(__name__)
        self.credentials = self._load_credentials(credentials_file)

    def _load_credentials(self, file_path):
        """Load credentials from secure file"""
        import json
        with open(file_path) as f:
            return json.load(f)

    def decode_project(self, project_path, backup=True):
        """Decode a complete project with backup"""

        project_path = Path(project_path)
        output_path = project_path.parent / f"{project_path.name}_decoded"

        # Create backup if requested
        if backup:
            backup_path = project_path.parent / f"{project_path.name}_backup"
            shutil.copytree(project_path, backup_path)
            self.logger.info(f"Backup created: {backup_path}")

        # Decode project
        try:
            decoder = IonicubeDecoder(
                self.credentials["username"],
                self.credentials["password"]
            )

            success = decoder.decode_directory(
                str(project_path),
                str(output_path)
            )

            if success:
                self.logger.info(f"Project decoded successfully: {output_path}")
                return str(output_path)
            else:
                self.logger.error("Decoding failed")
                return None

        except Exception as e:
            self.logger.error(f"Decoding error: {e}")
            return None

# Usage
decoder = ProjectDecoder("my_credentials.json")
result = decoder.decode_project("./my_encoded_project")
```

## Configuration Options

### Environment Variables

```bash
# Optional: Set default credentials
export EASYTOYOU_USERNAME="your_username"
export EASYTOYOU_PASSWORD="your_password"

# Optional: Set custom timeouts
export EASYTOYOU_TIMEOUT="300"
```

### Logging Configuration

```python
import logging

# Configure logging for the package
logging.getLogger('easytoyou').setLevel(logging.DEBUG)

# Custom formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# File handler
file_handler = logging.FileHandler('easytoyou_debug.log')
file_handler.setFormatter(formatter)
logging.getLogger('easytoyou').addHandler(file_handler)
```

## Support

For questions about the API or advanced usage:

- **Documentation**: [GitHub Wiki](https://github.com/rbwtech/easy-to-you-automation/wiki)
- **Issues**: [GitHub Issues](https://github.com/rbwtech/easy-to-you-automation/issues)
- **Email**: [radipta111@gmail.com](mailto:radipta111@gmail.com)
