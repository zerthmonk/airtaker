import os
import json

from django.test import TestCase
from django.utils import timezone
from core.airbender import AirBender

TEST_DATA_ROOT = os.path.join(os.path.dirname(__file__), 'testdata')
TEST_JSON_PATH = os.path.join(TEST_DATA_ROOT, 'table.json')


def get_test_data(file_path: str):
    with open(file_path) as fh:
        return json.loads(fh.read())


def get_expected(field: str = None) -> dict:
    data = {
        'id': 'rec59sIJUxkEHMLtT',
        'name': 'Георгий',
        'photo': {
            'id': 'att9KnVSSmHaLJNUm',
            'url': 'https://dl.airtable.com/.attachments/c15cce685652a0670beb0f4bb2485041/0d0720fe/3.jpg',
        },
        'methods': [
            'Психоанализ',
            'Музыкотерапия',
            'Сказкотерапия'
        ]
    }
    return data.get(field) if field else data


class AirBenderSetup(TestCase):

    def setUp(self):
        self.timestamp = timezone.now()
        self.data = get_test_data(TEST_JSON_PATH)
        self.parser = AirBender(self.data, self.timestamp)
