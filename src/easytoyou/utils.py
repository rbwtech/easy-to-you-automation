"""
Utility functions for EasyToYou decoder
"""

import os
import re
import logging
from typing import List, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

def is_ioncube_file(filepath: str) -> bool:
    """
    Check if a file is ionCube encoded
    
    Args:
        filepath: Path to the file to check
        
    Returns:
        True if file is ionCube encoded, False otherwise
    """
    try:
        with open(filepath, 'rb') as f:
            content = f.read(1024)  # Read first 1KB
            return b"ionCube Loader" in content or b"ioncube" in content.lower()
    except Exception as e:
        logger.warning(f"Could not read file {filepath}: {e}")
        return False

def find_php_files(directory: str) -> List[str]:
    """
    Find all PHP files in a directory recursively
    
    Args:
        directory: Directory to search
        
    Returns:
        List of PHP file paths
    """
    php_files = []
    try:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.lower().endswith('.php'):
                    php_files.append(os.path.join(root, file))
    except Exception as e:
        logger.error(f"Error scanning directory {directory}: {e}")
    
    return php_files

def find_ioncube_files(directory: str) -> List[str]:
    """
    Find all ionCube encoded PHP files in a directory
    
    Args:
        directory: Directory to search
        
    Returns:
        List of ionCube encoded PHP file paths
    """
    ioncube_files = []
    php_files = find_php_files(directory)
    
    for php_file in php_files:
        if is_ioncube_file(php_file):
            ioncube_files.append(php_file)
    
    return ioncube_files

def create_directory(path: str) -> bool:
    """
    Create directory if it doesn't exist
    
    Args:
        path: Directory path to create
        
    Returns:
        True if successful, False otherwise
    """
    try:
        Path(path).mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        logger.error(f"Failed to create directory {path}: {e}")
        return False

def batch_list(items: List, batch_size: int = 20) -> List[List]:
    """
    Split a list into batches
    
    Args:
        items: List to split
        batch_size: Size of each batch
        
    Returns:
        List of batches
    """
    batches = []
    for i in range(0, len(items), batch_size):
        batches.append(items[i:i + batch_size])
    return batches

def validate_decoder_version(decoder: str) -> bool:
    """
    Validate decoder version format
    
    Args:
        decoder: Decoder version string
        
    Returns:
        True if valid format, False otherwise
    """
    # Pattern: ic + version + php + version
    pattern = r'^ic\d+php\d+$'
    return bool(re.match(pattern, decoder))

def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing invalid characters
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Remove invalid characters for Windows/Unix
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human readable format
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted size string
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"

def get_file_info(filepath: str) -> dict:
    """
    Get file information
    
    Args:
        filepath: Path to file
        
    Returns:
        Dictionary with file information
    """
    try:
        stat = os.stat(filepath)
        return {
            'name': os.path.basename(filepath),
            'size': stat.st_size,
            'size_formatted': format_file_size(stat.st_size),
            'modified': stat.st_mtime,
            'is_ioncube': is_ioncube_file(filepath)
        }
    except Exception as e:
        logger.error(f"Could not get file info for {filepath}: {e}")
        return {}