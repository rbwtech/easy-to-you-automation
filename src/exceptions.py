"""
Custom exceptions for EasyToYou decoder
"""

class EasyToYouError(Exception):
    """Base exception for all EasyToYou related errors"""
    pass

class LoginError(EasyToYouError):
    """Raised when login to easytoyou.eu fails"""
    pass

class UploadError(EasyToYouError):
    """Raised when file upload fails"""
    pass

class DownloadError(EasyToYouError):
    """Raised when file download fails"""
    pass

class NetworkError(EasyToYouError):
    """Raised when network operations fail"""
    pass

class FormNotFoundError(EasyToYouError):
    """Raised when upload form cannot be found"""
    pass

class DecoderNotAvailableError(EasyToYouError):
    """Raised when specified decoder version is not available"""
    pass
