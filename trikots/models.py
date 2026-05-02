import uuid

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.views.decorators.csrf import requires_csrf_token


class Country(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Club(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class League(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Season(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    startYear = models.IntegerField(validators=[MinValueValidator(1001, "Jahreszahl muss valid sein.")])
    endYear = models.IntegerField(validators=[MinValueValidator(1001,"Jahreszahl muss valid sein.")])

    def clean(self):
        if self.startYear is None or self.endYear is None:
            return

        if self.startYear >= self.endYear:
            raise ValidationError({
                'endYear': 'Endjahr muss grösser als Startjahr sein.'
            })

    def __str__(self):
        return self.name
