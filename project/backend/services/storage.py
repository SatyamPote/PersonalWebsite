import cloudinary
import cloudinary.uploader
from fastapi import UploadFile
from ..core.config import settings

# Configure Cloudinary using the settings from our .env file
cloudinary.config(
    cloud_name = settings.CLOUDINARY_CLOUD_NAME,
    api_key = settings.CLOUDINARY_API_KEY,
    api_secret = settings.CLOUDINARY_API_SECRET,
    secure = True
)

def upload_file_to_cloudinary(file: UploadFile) -> dict:
    """
    Uploads a file to Cloudinary and returns the result.

    Args:
        file: The file to upload, received from a FastAPI endpoint.

    Returns:
        A dictionary containing the upload result from Cloudinary.
    """
    try:
        # The upload function from the cloudinary library does all the work
        upload_result = cloudinary.uploader.upload(file.file, resource_type="auto")
        return upload_result
    except Exception as e:
        # Handle potential errors during upload
        print(f"Error uploading to Cloudinary: {e}")
        raise e