"""
EasyToYou - Professional IonicCube Decoder
==========================================

A high-performance, reliable IonicCube decoder using easytoyou.eu service
with enhanced bot detection avoidance and comprehensive error handling.

Example usage:
    from easytoyou import IonicubeDecoder
    
    decoder = IonicubeDecoder("username", "password")
    success = decoder.decode_directory("./source", "./output")
"""

__version__ = "2.0.0"
__author__ = "RBW-Tech"
__email__ = "radipta111@gmail.com"
__license__ = "MIT"

from .decoder import IonicubeDecoder
from .exceptions import (
    EasyToYouError,
    LoginError,
    UploadError,
    DownloadError,
    NetworkError
)

__all__ = [
    "IonicubeDecoder",
    "EasyToYouError", 
    "LoginError",
    "UploadError", 
    "DownloadError",
    "NetworkError"
]
