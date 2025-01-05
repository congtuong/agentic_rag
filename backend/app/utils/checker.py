from tempfile import SpooledTemporaryFile
from const import SUPPORTED_FILE_TYPES

def check_upload_file(
    file: SpooledTemporaryFile,
) -> bool:
    """
    Check the upload file object.
    """
    if file.content_type not in SUPPORTED_FILE_TYPES:
        return False
    
    return True
    