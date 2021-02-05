import json
from django.http import JsonResponse

from core.models import Therapist
from core.serializers import ProfileSerializer
from core.views import profile, healthcheck

from core.tests.config import AirBenderSetup, get_expected


def first_person_expected():
    # form up expected data
    expected = {k: get_expected(k) for k in ['name', 'methods']}
    expected.update({'photo': get_expected('photo')['url']})
    expected['methods'].sort()
    return expected


class ProfileSerializerTestCase(AirBenderSetup):

    def setUp(self):
        super().setUp()
        # not a good idea about inter-dependent test, but I was in hurry
        self.parser.save()  # populates database with test data
        self.expected = first_person_expected()
        # serialize one person data
        serializer = ProfileSerializer()
        self.serial_data = serializer.serialize([Therapist.objects.get(name=self.expected['name'])])

    def test_serializer_basic(self):
        self.assertTrue(isinstance(self.serial_data, list))
        self.assertEqual(self.serial_data, [self.expected])


class ApiProfileTestCase(AirBenderSetup):

    def setUp(self):
        super().setUp()
        self.parser.save()
        serializer = ProfileSerializer()
        self.expected = serializer.serialize(Therapist.objects.all())
        self.check_data = healthcheck()
        self.profile_data = profile()

    def test_check_response(self):
        self.assertTrue(isinstance(self.check_data, JsonResponse))

    def test_profiles_response(self):
        self.assertTrue(isinstance(self.profile_data, JsonResponse))

    def test_check_json_content(self):
        self.assertEqual(json.loads(self.check_data.content), {'result': 'it works'})

    def test_profiles_json_content(self):
        self.assertEqual(json.loads(self.profile_data.content), {'result': self.expected})
