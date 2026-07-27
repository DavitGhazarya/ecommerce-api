import cloudinary.uploader

from app import cloudinary_config


def upload_image(file):

    result = cloudinary.uploader.upload(
        file
    )

    return result["secure_url"]