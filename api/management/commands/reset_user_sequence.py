from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import connection

class Command(BaseCommand):
    help = 'Resets the user ID sequence if no users exist'

    def handle(self, *args, **kwargs):
        # Check if any users exist
        user_count = User.objects.count()

        if user_count == 0:
            with connection.cursor() as cursor:
                # Reset the sequence
                cursor.execute("ALTER SEQUENCE auth_user_id_seq RESTART WITH 1;")
                self.stdout.write(self.style.SUCCESS('User ID sequence reset to 1.'))
        else:
            # If users exist, you can adjust the sequence to the highest user ID + 1
            max_id = User.objects.order_by('-id').first().id
            with connection.cursor() as cursor:
                cursor.execute(f"ALTER SEQUENCE auth_user_id_seq RESTART WITH {max_id + 1};")
            self.stdout.write(self.style.SUCCESS(f'User ID sequence reset to {max_id + 1}.'))

