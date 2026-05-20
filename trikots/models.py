import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from trikots.validators import max_year, validate_year_range, validate_match_home_away_club


class Country(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True, verbose_name="Name")

    class Meta:
        verbose_name = "Land"
        verbose_name_plural = "Länder"

    def __str__(self):
        return self.name


class Club(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True, verbose_name="Name")
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name="Land")

    class Meta:
        verbose_name = "Club"
        verbose_name_plural = "Clubs"

    def __str__(self):
        return self.name


class League(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True, verbose_name="Name")
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name="Land")

    class Meta:
        verbose_name = "Liga"
        verbose_name_plural = "Ligen"

    def __str__(self):
        return self.name


class Season(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    league = models.ForeignKey(League, on_delete=models.CASCADE, verbose_name="Liga")
    name = models.CharField(max_length=100, unique=True, verbose_name="Bezeichnung (Prefix)")
    startYear = models.IntegerField(validators=[
        MinValueValidator(1001, "Jahreszahl muss valid sein."),
        MaxValueValidator(max_year(), "Jahreszahl ist zu gross.")
    ], verbose_name="Jahr der Vorrunde")
    endYear = models.IntegerField(validators=[
        MinValueValidator(1001, "Jahreszahl muss valid sein."),
        MaxValueValidator(max_year(), "Jahreszahl ist zu gross.")
    ], verbose_name="Jahr der Rückrunde")

    class Meta:
        verbose_name = "Saison"
        verbose_name_plural = "Saisons"

    def clean(self):
        validate_year_range(self.startYear, self.endYear)

    def __str__(self):
        return f"{self.name} {self.league} {str(self.startYear)[-2:]}/{str(self.endYear)[-2:]}"


class Person(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100, verbose_name="Vorname")
    last_name = models.CharField(max_length=100, verbose_name="Nachname")

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "Personen"
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
    name = models.CharField(max_length=100, unique=True, verbose_name="Name")

    class Meta:
        verbose_name = "Ausrüster"
        verbose_name_plural = "Ausrüster"

    def __str__(self):
        return self.name


class SeasonClub(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    season = models.ForeignKey(Season, on_delete=models.CASCADE, verbose_name="Saison")
    club = models.ForeignKey(Club, on_delete=models.CASCADE, verbose_name="Club")
    description = models.TextField(max_length=2000, null=True, blank=True, verbose_name="Beschreibung")
    presidents = models.ManyToManyField(
        Person,
        related_name="president_season_clubs",
        blank=True,
        verbose_name="Präsidenten"
    )
    captains = models.ManyToManyField(
        Person,
        related_name="captain_season_clubs",
        blank=True,
        verbose_name="Kaptains"

    )
    trainers = models.ManyToManyField(
        Person,
        related_name="trainer_season_clubs",
        blank=True,
        verbose_name="Trainer"
    )
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Ausrüster"
    )

    class Meta:
        verbose_name = "Saison-Club"
        verbose_name_plural = "Saison-Clubs"

    def __str__(self):
        return f"{self.season} - {self.club}"


class Match(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    home_club = models.ForeignKey(
        Club,
        on_delete=models.CASCADE,
        related_name="home_club",
        verbose_name="Heimclub"
    )
    away_club = models.ForeignKey(
        Club,
        on_delete=models.CASCADE,
        related_name="away_club",
        verbose_name="Auswärtsclub"
    )
    goals_home = models.IntegerField(
        validators=[MinValueValidator(0, "Das Resultat muss positiv sein.")],
        verbose_name="Tore Heimclub"
    )
    goals_away = models.IntegerField(
        validators=[MinValueValidator(0, "Das Resultat muss positiv sein.")],
        verbose_name="Tore Auswärtsclub"
    )
    goal_scorers = models.ManyToManyField(
        Person,
        related_name="goal_scorer",
        blank=True,
        verbose_name="Torschützen"
    )
    date = models.DateField(verbose_name="Datum")

    class Meta:
        verbose_name = "Spiel"
        verbose_name_plural = "Spiele"

    def clean(self):
        validate_match_home_away_club(self.home_club_id, self.away_club_id)

    def __str__(self):
        return f"{self.home_club} - {self.away_club} ({self.goals_home}:{self.goals_away}) - {self.date}"


class Shirt(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    number = models.IntegerField(null=True, blank=True, verbose_name="Trikotnummer")
    image = models.ImageField(upload_to='shirts/', verbose_name="Bild")
    description = models.TextField(max_length=2000, null=True, blank=True, verbose_name="Beschreibung")
    club = models.ForeignKey(Club, on_delete=models.CASCADE, verbose_name="Club")
    season = models.ForeignKey(Season, on_delete=models.CASCADE, verbose_name="Saison")
    match_worn = models.BooleanField(default=False, verbose_name="Matchworn")
    player = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Spieler"
    )
    match = models.ForeignKey(
        Match,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Spiel"
    )
    price = models.IntegerField(null=True, blank=True, verbose_name="Preis")
    purchase_date = models.DateField(null=True, blank=True, verbose_name="Kaufdatum")

    class Meta:
        verbose_name = "Trikot"
        verbose_name_plural = "Trikots"

    def __str__(self):
        if self.number and self.player and self.match:
            return f"{self.number } - {self.player.first_name} {self.player.last_name} - {self.club}"

        if self.number and self.player:
            return f"{self.player.first_name} {self.player.last_name} - {self.club}"

        return f"Shirt - {self.club}"