import logging
from typing import List

from django.db import transaction

from core import models
from core.helpers import DotDict


class AirBender(object):

    field_names = DotDict(dict(
        name='Имя',
        photo='Фотография',
        methods='Методы'
    ))

    def __init__(self, payload: List[dict], timestamp: str):
        self.payload = payload
        self.timestamp = timestamp
        self.parsed = [self.parse_item(item) for item in self.payload]

    def save_raw(self) -> models.RawData:
        """Save raw data as string"""
        logging.info(f'[SAVE RAW] at {self.timestamp}')
        return models.RawData.objects.create(timestamp=self.timestamp,
                                             payload=f'{self.payload}')

    def parse_item(self, item: dict) -> dict:
        """Parse payload item"""
        try:
            _id = item.get('id')
            fields = item.get('fields', {})
            photo_attrs = ['id', 'url']

            name = fields.get(self.field_names.name, '')
            photo = self.parse_photo(data=fields, field_list=photo_attrs)
            methods = fields.get(self.field_names.methods, [])

            result = {
                'id': _id,
                'name': name,
                'photo': photo,
                'methods': methods
            }

            for k, v in result.items():
                if not v:
                    raise ValueError(f'{k} is missing')

            return result
        except ValueError or Exception:
            logging.exception(f'when parsing {item}: ')
            return {}

    def parse_photo(self, data: dict, field_list: list) -> dict:
        """Parse photo data"""
        photo_data = data.get(self.field_names.photo)
        if isinstance(photo_data, list):
            return {k: v for k, v in photo_data[0].items()
                    if k in field_list}

    def save_parsed(self):
        """Upsert records from fetched payload"""
        for item in self.parsed:

            photo = self.save_photo(item['photo'])

            params = {
                'id': item['id'],
                'name': item['name'],
                'photo': photo
            }
            # get object or create new record.
            # note: get_or_create returns tuple(obj, bool)
            # https://docs.djangoproject.com/en/3.1/ref/models/querysets/
            obj, created = models.Therapist.objects.get_or_create(pk=item['id'],
                                                                  defaults=params)
            if not created:
                # record exists, updating
                models.Therapist.objects.filter(id=obj.id).update(**params)
            # update methods anyway
            person = self.update_methods(obj, item.get('methods'))
            return person

    def update_methods(self, person: models.Therapist, methods: list) -> models.Therapist:
        """Update method list for person"""
        if methods:
            methods = (self.save_method(name) for name in methods)  # populate db with presented methods
            person.methods.clear()  # clears M2M relationship with TherapyMethod set
            for obj in methods:
                person.methods.add(obj)
        return person

    @staticmethod
    def save_photo(photo: dict) -> models.Photo:
        obj, created = models.Photo.objects.get_or_create(pk=photo['id'],
                                                          defaults={**photo})
        return obj

    @staticmethod
    def save_method(method_name: str) -> models.TherapyMethod:
        obj, created = models.TherapyMethod.objects.get_or_create(pk=method_name)
        return obj

    @transaction.atomic
    def cleanup_after_sync(self):
        """Cleanup local records not presented in remote Airtable"""
        try:
            models.Therapist.cleanup_other_than(ids=(item['id'] for item in self.parsed))
            models.Photo.cleanup_other_than(ids=(item['photo']['id'] for item in self.parsed))
            models.TherapyMethod.cleanup_other_than(names=set(item['methods'] for item in self.parsed))
        except Exception:
            logging.exception('when cleanup: ')
            raise

    def __str__(self):
        return f'AirBender <{self.timestamp}>'



