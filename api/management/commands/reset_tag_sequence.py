from django.core.management.base import BaseCommand
from django.db import connection
from api.models import Tag


class Command(BaseCommand):
    help = 'Resets the tag ID sequence if no tags exist'

    def handle(self, *args, **kwargs):
        # Check if any tags exist
        tag_count = Tag.objects.count()

        if tag_count == 0:
            with connection.cursor() as cursor:
                # Reset the sequence
                cursor.execute("ALTER SEQUENCE api_tag_id_seq RESTART WITH 1;")
                self.stdout.write(self.style.SUCCESS('Tag ID sequence reset to 1.'))
        else:
            # If tags exist, you can adjust the sequence to the highest tag ID + 1
            max_id = Tag.objects.order_by('-id').first().id
            with connection.cursor() as cursor:
                cursor.execute(f"ALTER SEQUENCE api_tag_id_seq RESTART WITH {max_id + 1};")
            self.stdout.write(self.style.SUCCESS(f'Tag ID sequence reset to {max_id + 1}.'))

