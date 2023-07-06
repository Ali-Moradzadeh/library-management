from django.core.management.base import BaseCommand, CommandError
from accounting.models import User

class Command(BaseCommand):
    help = 'create initial users'

    def handle(self, *args, **kwargs):
        kv = {
            "username": "ali",
            "phone_number": "09387311923",
            "email": "alimoradzadeh96@gmail.com",
            "password": "Ali541379"
        }
        User.objects.create_superuser(**kv)
        self.stdout.write(f"Superuser Successfully Created!")