import os
import json

from typing import List

from django.utils import timezone
from django.test import TestCase

from core import models
from core.airbender import AirBender
from core.helpers import DotDict


TEST_JSON_PATH = os.path.join(os.path.dirname(__file__), 'testdata', 'table.json')


def get_test_data(file_path: str) -> List[dict]:
    with open(file_path) as fh:
        return json.loads(fh.read())


def get_expected() -> dict:
    return {
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


class DotDictTestCase(TestCase):

    def setUp(self):
        self.test_data = {
            'name': 'Имярек',
            'list': ['list', 'больше', 'item'],
            'num': 12345
        }
        self.dot = DotDict(self.test_data)


    def test_dotdict(self):
        for k, v in self.test_data.items():
            self.assertEqual(getattr(self.dot, k), v)


class ParseDataTestCase(TestCase):

    def setUp(self):
        self.timestamp = timezone.now()
        self.data = get_test_data(TEST_JSON_PATH)
        self.parser = AirBender(self.data, self.timestamp)

    def test_parser_persons(self):
        self.assertTrue(isinstance(self.parser.payload, list))
        result = self.parser.parse_item(self.parser.payload[0])
        self.assertEqual(result, get_expected())

    def test_parser_save_photo(self):
        photo_data = get_expected()['photo']
        photo = self.parser.save_photo(photo_data)
        self.assertEqual(photo.id, photo_data['id'])
        self.assertEqual(photo.url, photo_data['url'])

    def test_parser_save(self):
        self.parser.save_parsed()
        test_person = models.Therapist.objects.get(id='rec59sIJUxkEHMLtT')
        self.assertTrue(test_person)
