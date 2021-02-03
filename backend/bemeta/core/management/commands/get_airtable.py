import time
import logging

from airtable import Airtable

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to take data from remote AirTable"""

    # used https://airtable.com/shri28o0LL6WHL6jM

    def handle(self, *args, **options):
        try:
            base_key = options.get('base_id', settings.AIRTABLE_BASE_ID)
            table_name = options.get('table_name', settings.AIRTABLE_TABLE_NAME)
            if not base_key or not table_name:
                raise ValueError('airtable credentials missing')
            table = Airtable(base_key, table_name, settings.AIRTABLE_API_KEY)
            return f'{table.get_all()}'
        except Exception as e:
            logging.exception(f'{e}')
            self.stdout.write(self.style.ERROR(f'{e}'))
