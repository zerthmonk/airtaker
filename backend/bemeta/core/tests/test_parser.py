import os
import json

from django.utils import timezone
from django.test import TestCase

from core import models
from core.airbender import AirBender
from core.helpers import DotDict


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


class AirBenderSetup(TestCase):

    def setUp(self):
        self.timestamp = timezone.now()
        self.data = get_test_data(TEST_JSON_PATH)
        self.parser = AirBender(self.data, self.timestamp)


class SaveDataTestCase(AirBenderSetup):

    def setUp(self):
        super().setUp()

    def test_parser_persons(self):
        self.assertTrue(isinstance(self.parser.payload, list))
        result = self.parser.parse_item(self.parser.payload[0])
        self.assertEqual(result, get_expected())

    def test_parser_save_photo(self):
        photo_data = get_expected('photo')
        photo = self.parser.save_photo(photo_data)
        self.assertEqual(photo.pk, photo_data['id'])
        self.assertEqual(photo.url, photo_data['url'])

    def test_parser_save_method(self):
        method_name = get_expected('methods')[0]
        method = self.parser.save_method(method_name)
        self.assertEqual(method.pk, method_name)

    def test_parser_save(self):
        self.parser.save()
        test_person = models.Therapist.objects.get(pk=get_expected('id'))
        self.assertTrue(test_person)


class SyncDataTestCase(AirBenderSetup):

    def setUp(self):
        super().setUp()
        self.update = get_test_data(os.path.join(TEST_DATA_ROOT, 'update.json'))
        self.update_parser = AirBender(self.update, self.timestamp)
        self.update_parser.save()
        self.expected = self.parser.parse_item(self.update[0])

    def test_parser_update(self):
        """test existed local record is updated by remote table record values"""
        instance = models.Therapist.objects.get(pk=get_expected('id'))
        instance_method_set = sorted([m.pk for m in instance.methods.all()])
        expected = self.expected

        self.assertEqual(instance.id, expected['id'])
        self.assertEqual(instance.name, expected['name'])
        self.assertEqual(instance.photo.id, expected['photo']['id'])
        self.assertEqual(instance.photo.url, expected['photo']['url'])
        self.assertEqual(instance_method_set, sorted(expected['methods']))

    def test_parser_sync(self):
        """test only remote records stays in local db"""
        self.update_parser.cleanup_after_sync()

        ids = [m.pk for m in models.Therapist.objects.all()]
        photos = [m.pk for m in models.Photo.objects.all()]
        methods = sorted([m.pk for m in models.TherapyMethod.objects.all()])

        self.assertEqual(ids, [self.expected['id']])
        self.assertEqual(photos, [self.expected['photo']['id']])
        self.assertEqual(methods, sorted(self.expected['methods']))
