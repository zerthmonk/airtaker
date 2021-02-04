import time

import django.db
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to pause execution until database is available"""

    def handle(self, *args, **options):
        pass
        #while not django.db.connection.ensure_connection():
        #    self.stdout.write('Database unavailable, waiting 1 second...')
        #    time.sleep(1)
        #self.stdout.write(self.style.SUCCESS('Database is available!'))
