import uuid
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from datetime import datetime

from trikots.validators import max_year, validate_year_range


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
    startYear = models.IntegerField(validators=[
        MinValueValidator(1001, "Jahreszahl muss valid sein."),
        MaxValueValidator(max_year(), "Jahreszahl ist zu gross.")
    ])
    endYear = models.IntegerField(validators=[
        MinValueValidator(1001,"Jahreszahl muss valid sein."),
        MaxValueValidator(max_year(), "Jahreszahl ist zu gross.")
    ])

    def clean(self):
        validate_year_range(self.startYear, self.endYear)

    def __str__(self):
        return f"{self.name} {str(self.startYear)[-2:]}/{str(self.endYear)[-2:]}"

class Person(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return self.first_name + " " + self.last_name

