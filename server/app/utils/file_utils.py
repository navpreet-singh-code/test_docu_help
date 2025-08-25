def is_supported_file_type(mime_type: str) -> bool:
    return mime_type.startswith("image/") or mime_type == "application/pdf"

def is_image_type(mime_type: str) -> bool:
    return mime_type.startswith("image/")
