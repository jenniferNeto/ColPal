from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from django.contrib.auth.models import User


class Command(BaseCommand):
    # Create a superuser account
    def handle(self, *args, **options):
        try:
            User.objects.create_superuser(username='admin', email='', password='')
            print("Admin account successfully created.")
        except IntegrityError:
            print('Admin account already exists: skipping')
