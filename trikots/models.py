import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from trikots.validators import max_year, validate_year_range, validate_match_home_away_club


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


    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["first_name", "last_name"],
                name="unique_person_full_name"
            )
        ]

    def __str__(self):
        return self.first_name + " " + self.last_name

class Supplier(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class SeasonClub(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    description = models.TextField(max_length=2000, null=True, blank=True)
    presidents = models.ManyToManyField(
        Person,
        related_name="president_season_clubs",
        blank=True
    )
    captains = models.ManyToManyField(
        Person,
        related_name="captain_season_clubs",
        blank=True
    )
    trainers = models.ManyToManyField(
        Person,
        related_name="trainer_season_clubs",
        blank=True
    )
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.season} - {self.club}"

class Match(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    home_club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="home_club")
    away_club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="away_club")
    goals_home = models.IntegerField(validators=[MinValueValidator(0, "Das Resultat muss positiv sein.")])
    goals_away = models.IntegerField(validators=[MinValueValidator(0, "Das Resultat muss positiv sein.")])
    goal_scorers = models.ManyToManyField(
        Person,
        related_name="goal_scorer",
        blank=True
    )
    date = models.DateField()

    def clean(self):
        validate_match_home_away_club(self.home_club_id, self.away_club_id)

    def __str__(self):
        return f"{self.home_club} - {self.away_club} ({self.goals_home}:{self.goals_away}) - {self.date}"