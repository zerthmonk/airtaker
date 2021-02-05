from typing import Union, List
from django.db.models import QuerySet

from core.models import Therapist


class ProfileSerializer:

    """Serializing therapist profile data

       what a shame without DRF :)
    """

    def serialize(self, profiles: Union[QuerySet, List[Therapist]]):
        return [self.to_representation(obj) for obj in profiles]

    @staticmethod
    def to_representation(obj):
        return {
            'name': obj.name,
            'photo': obj.photo.url,
            'methods': obj.method_names
        }

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return f'{exc_type} {exc_val} {exc_tb}'
