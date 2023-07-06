import os
from django.utils import timezone


app_model_pair = {
    'accounting.adminprofile': 'admins',
    'accounting.publisherprofile': 'publishers',
}

def custom_file_handler(instance, filename):
    ext = filename.split('.')[-1]
    ts = timezone.now()
    filename = f'{ts.year}_{ts.month}_{ts.day}.{ext}'
    object_class_name = str(instance._meta)
    folder_name = app_model_pair.get(str(instance._meta))

    return os.path.join(folder_name, filename)
