import logging
from typing import List

from django.db import transaction

from core import models
from core.helpers import DotDict, flatten_list


class AirBender(object):

    """Syncs local data with remote Airtable table"""

    field_names = DotDict(dict(
        name='Имя',
        photo='Фотография',
        methods='Методы'
    ))

    def __init__(self, payload: List[dict], timestamp: str):
        self.payload = payload
        self.timestamp = timestamp
        self.parsed = [self.parse_item(item) for item in self.payload]

    def save_raw(self) -> models.AirData:
        """Save raw data as string"""
        logging.info(f'SAVE RAW: at {self.timestamp}')
        return models.AirData.objects.create(timestamp=self.timestamp,
                                             payload=self.payload)

    def save(self):
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
            self.update_methods(obj, item.get('methods'))
        logging.info(f'SAVE PARSED: at {self.timestamp}')

    def parse_item(self, item: dict) -> dict:
        """Parse payload item"""
        try:
            _id = item.get('id')
            if not _id:
                raise AttributeError('DATA INCONSISTENCY: missing `id` field')
            fields = item.get('fields')
            if not fields:
                raise AttributeError('DATA INCONSISTENCY: missing `fields` field')

            photo_attrs = ['id', 'url']

            name = fields.get(self.field_names.name)
            photo = self.parse_photo(data=fields, field_list=photo_attrs)
            methods = fields.get(self.field_names.methods)

            result = {
                'id': _id,
                'name': name,
                'photo': photo,
                'methods': methods
            }

            for k, v in result.items():
                if not v:
                    raise AttributeError(f'{k} is missing')
            return result
        except AttributeError:
            logging.exception(f'when parsing {item}: ')
            return {}

    def parse_photo(self, data: dict, field_list: list) -> dict:
        """Parse photo data"""
        photo_data = data.get(self.field_names.photo)
        if isinstance(photo_data, list):
            return {k: v for k, v in photo_data[0].items()
                    if k in field_list}

    def update_methods(self, person: models.Therapist, methods: list) -> models.Therapist:
        """Update method list for person"""
        if methods:
            logging.debug(f'{person} updates with method list: {methods}')
            methods = (self.save_method(name) for name in methods)  # populate db with presented methods
            person.methods.clear()  # clears M2M relationship with TherapyMethod set
            for obj in methods:
                person.methods.add(obj)
        return person

    @staticmethod
    def save_photo(photo: dict) -> models.Photo:
        obj, created = models.Photo.objects.get_or_create(pk=photo['id'],
                                                          defaults={**photo})
        if created:
            logging.debug(f'new photo {photo}')
        return obj

    @staticmethod
    def save_method(method_name: str) -> models.TherapyMethod:
        obj, created = models.TherapyMethod.objects.get_or_create(pk=method_name)
        if created:
            logging.debug(f'new method {method_name}')
        return obj

    @transaction.atomic
    def cleanup_after_sync(self):
        """Cleanup local records not presented in remote Airtable"""
        try:
            models.Therapist.cleanup_other_than(model=models.Therapist,
                                                ids=(item['id'] for item in self.parsed))

            models.Photo.cleanup_other_than(model=models.Photo,
                                            ids=(item['photo']['id'] for item in self.parsed))

            models.TherapyMethod.cleanup_other_than(model=models.TherapyMethod,
                                                    names=set(flatten_list(item['methods'] for item in self.parsed)))
            logging.debug('sync cleanup complete')
        except Exception:
            logging.exception('when cleanup: ')
            raise

    def __str__(self):
        return f'AirBender <{self.timestamp}>'



