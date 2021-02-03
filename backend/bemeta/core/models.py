from django.db import models


class TherapyMethod(models.Model):

    """Therapy method model"""

    class Meta:
        verbose_name = 'Therapy method'
        verbose_name_plural = 'Therapy methods'

    name = models.CharField(max_length=512, primary_key=True)

    def __str__(self):
        return f'TherapyMethod <{self.name}>'


class TherapistPerson(models.Model):

    """Therapist person profile model"""

    class Meta:
        verbose_name = 'Therapist'
        verbose_name_plural = 'Therapists'

    name = models.CharField(max_length=512)
    photo = models.FileField(upload_to='photos/')
    methods = models.ManyToManyField(TherapyMethod)

    def __str__(self):
        return f'TherapistPerson <{self.name}> {self.methods}'

