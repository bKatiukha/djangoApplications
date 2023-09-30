from django.core.management.base import BaseCommand

from src.shared_auth.models import UserProfile


class Command(BaseCommand):
    help = 'reset online_status value (0) for all users in a table UserProfile'

    def handle(self, *args, **options):
        # Update all records in the table to set the field to 0
        UserProfile.objects.update(online_status=0)  # Replace 'your_field_name' with the actual field name

        self.stdout.write(self.style.SUCCESS('Successfully reset online_status for all users'))
