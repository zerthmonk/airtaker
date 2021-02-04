from django.db import models
from django.utils import timezone


class SyncAble(models.Model):

    """Abstract for keeping consistency between local DB and remote Airtable"""

    class Meta:
        abstract = True

    id = models.CharField(max_length=128,
                          primary_key=True)

    @staticmethod
    def cleanup_other_than(model, ids: list):
        model.objects.exclude(pk__in=ids).delete()


class AirData(models.Model):

    """Airtable raw data"""

    payload = models.JSONField()
    timestamp = models.DateTimeField(default=timezone.now)


class TherapyMethod(models.Model):

    """Therapy method model"""

    class Meta:
        verbose_name_plural = 'Therapy methods'

    id = models.CharField(max_length=512, primary_key=True)

    @staticmethod
    def cleanup_other_than(model, names: list):
        model.objects.exclude(pk__in=names).delete()

    def __str__(self):
        return f'TherapyMethod <{self.pk}>'


class Photo(SyncAble):

    """Photo image file"""

    class Meta:
        verbose_name_plural = 'Photos'

    url = models.URLField()

    def __str__(self):
        return f'Photo <{self.id}> {self.url}'


class Therapist(SyncAble):

    """Therapist person profile model"""

    class Meta:
        verbose_name = 'Therapist profile'
        verbose_name_plural = 'Therapist profiles'

    name = models.CharField(max_length=512)
    photo = models.ForeignKey(Photo,
                              blank=True,
                              on_delete=models.CASCADE)
    methods = models.ManyToManyField(TherapyMethod)

    def __str__(self):
        return f'Therapist <{self.id}> {self.name} {self.methods}>'
