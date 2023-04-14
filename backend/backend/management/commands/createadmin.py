from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from django.contrib.auth.models import User

import os


class Command(BaseCommand):
    # Create a superuser account
    def handle(self, *args, **options):
        try:
            User.objects.create_superuser(
                username=os.environ.get("DB_NAME", ""),
                email=os.environ.get("EMAIL_ADDRESS", ""),
                password=os.environ.get("DB_PASS", ""))
            print("Admin account successfully created.")
        except IntegrityError:
            print('Admin account already exists: skipping')
