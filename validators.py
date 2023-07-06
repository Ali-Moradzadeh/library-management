import os
#import magic
from django.core.exceptions import ValidationError


def validate_file_extension(file):
    return file
"""
    valid_mime_types = ['image/svg+xml', 'image/png', 'image/jpeg']
    file_mime_type = magic.from_buffer(file.read(1024), mime=True)
    if file_mime_type not in valid_mime_types:
        raise ValidationError('Unsupported file type.')

    valid_file_extensions = ['.svg', '.png', '.jpeg', '.jpg']
    ext = os.path.splitext(file.name)[1]
    if ext.lower() not in valid_file_extensions:
        raise ValidationError('Unacceptable file extension.')
"""