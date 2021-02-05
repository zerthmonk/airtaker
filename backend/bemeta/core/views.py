from django.http import JsonResponse
from core.models import Therapist
from core.serializers import ProfileSerializer


def healthcheck(*args, **kwargs):
    """simple healthcheck view function"""
    return JsonResponse({'result': 'it works'})


def profile(*args, **kwargs):
    """view function unloads full profiles info"""
    try:
        with ProfileSerializer() as serializer:
            data = serializer.serialize(Therapist.objects.all())
            return JsonResponse({'result': data})
    except Exception as e:
        return JsonResponse({'error': f'{e}'})
