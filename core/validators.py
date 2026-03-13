from django.core.exceptions import ValidationError


ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/webp']
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


def validate_file_size(file):
    if file.size > MAX_FILE_SIZE:
        raise ValidationError(f'File size must not exceed {MAX_FILE_SIZE // (1024 * 1024)} MB.')


def validate_image_type(file):
    import mimetypes
    mime_type = getattr(file, 'content_type', None)
    if mime_type is None:
        mime_type, _ = mimetypes.guess_type(file.name)
    if mime_type not in ALLOWED_IMAGE_TYPES:
        raise ValidationError(
            f'Unsupported image type. Allowed: {", ".join(ALLOWED_IMAGE_TYPES)}'
        )
