import logging
from airtable import Airtable

from django.conf import settings
from django.utils import timezone
from django.core.management.base import BaseCommand

from core.airbender import AirBender


class Command(BaseCommand):
    """Django command to reflect local DB by Airtable table"""

    # used https://airtable.com/shri28o0LL6WHL6jM

    def handle(self, *args, **options):
        try:
            base_key = options.get('base_id', settings.AIRTABLE_BASE_ID)
            table_name = options.get('table_name', settings.AIRTABLE_TABLE_NAME)
            if not base_key or not table_name:
                raise ValueError('airtable credentials missing')
            table = Airtable(base_key, table_name, settings.AIRTABLE_API_KEY)
            self.stdout.write(f'>>> retrieving data from table {table_name}')
            payload = table.get_all()
            self.stdout.write(self.style.SUCCESS('data retrieved, starting local DB sync...'))
            syncer = AirBender(payload, timezone.now())
            syncer.save_raw()
            syncer.save()
            syncer.cleanup_after_sync()
            self.stdout.write(self.style.SUCCESS('DB sync completed!'))
        except Exception as e:
            logging.exception(f'{e}')
            self.stdout.write(self.style.ERROR(f'{e}'))
