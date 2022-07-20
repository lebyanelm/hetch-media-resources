"""
A list of Mimetypes that can be allowed for
uploads and saving to the media resources storage.
"""

allowed_mimetypes = (
    # Images
    "image/jpg", "image/jpeg", "image/png",
    "image/bmp", "image/gif", "image/ief",
    "image/svg+xml", "image/tiff", "image/x-icon",
    
    # Documents
    "application/hta", "application/html", "application/pdf",
    "application/rtf", "application/zip",
    
    # Audio
    "audio/basic", "audio/mpeg", "audio/x-wav",

    # Video
    "video/mpeg", "video/mp4", "video/quicktime"
)