from random import getrandbits
from django.utils import timezone

from django.test import TestCase
from unittest.mock import patch

from core.models import RawData, SyncAble, Photo, Therapist, TherapyMethod
from core.airbender import AirBender

NOW = timezone.now()
PAYLOAD = [{'test': 'payload'}]


def pseudo_id():
    return getrandbits(16)


class RawDataTestCase(TestCase):

    def setUp(self):
        self.from_default = RawData.objects.create(timestamp=NOW,
                                                   payload=f'{PAYLOAD}')
        with patch.object(AirBender, 'parse_item', return_value=None):
            air = AirBender(payload=PAYLOAD, timestamp=NOW)
            self.from_air = air.save_raw()

    def test_default_save(self):
        data = RawData.objects.get(id=self.from_default.id)
        self.assertEqual(f'{PAYLOAD}', f'{data.payload}')
        self.assertEqual(NOW, data.timestamp)

    def test_bender_save(self):
        air = RawData.objects.get(id=self.from_air.id)
        self.assertEqual(f'{PAYLOAD}', air.payload)
        self.assertEqual(NOW, air.timestamp)


# TEST DATA (should be separated, ofc)
TEST_URL = 'http://test.url.com'
TEST_NAME = 'Доктор Врач'
TEST_METHOD_NAME = 'Абсолютный метод'


class PhotoTestCase(TestCase):

    def setUp(self):
        self.test_id = pseudo_id()
        self.test_url = TEST_URL
        self.instance = Photo.objects.create(pk=self.test_id,
                                             url=self.test_url)

    def test_model_photo(self):
        self.assertEqual(self.instance.id, self.test_id)
        self.assertEqual(self.instance.url, self.test_url)


class MethodTestCase(TestCase):

    def setUp(self):
        self.test_name = TEST_METHOD_NAME
        self.instance = TherapyMethod.objects.create(pk=self.test_name)

    def test_model_method(self):
        print(f'{self.instance}')
        self.assertTrue(self.instance.pk)
        self.assertEqual(self.instance.pk, self.test_name)


class TherapistTestCase(TestCase):

    def setUp(self):
        self.test_name = TEST_NAME
        self.photo = Photo.objects.create(pk=pseudo_id(), url=TEST_URL)
        self.method = TherapyMethod.objects.create(pk=TEST_METHOD_NAME)
        self.instance = Therapist(name=self.test_name,
                                  photo=self.photo)
        self.instance.save()
        self.instance.methods.add(self.method)

    def test_model_therapist(self):
        self.assertEqual(self.instance.name, self.test_name)
        self.assertEqual(self.instance.methods.get(pk=self.method.pk), self.method)
