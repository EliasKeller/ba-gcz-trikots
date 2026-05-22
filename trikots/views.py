from rest_framework import viewsets
from trikots.models import Country, Club, League, Season, Person, Supplier, SeasonClub, Match, Shirt
from trikots.serializers import (
    CountrySerializer,
    ClubSerializer,
    LeagueSerializer,
    SeasonSerializer,
    PersonSerializer,
    SupplierSerializer,
    SeasonClubSerializer,
    MatchSerializer,
    ShirtSerializer,
)

class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

class ClubViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Club.objects.select_related('country').all()
    serializer_class = ClubSerializer

class LeagueViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = League.objects.select_related('country').all()
    serializer_class = LeagueSerializer


class SeasonViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Season.objects.select_related('league__country').all()
    serializer_class = SeasonSerializer

class PersonViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class SupplierViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

class SeasonClubViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SeasonClub.objects.select_related(
        'season__league__country',
        'club__country',
        'supplier',
    ).prefetch_related(
        'presidents',
        'captains',
        'trainers',
    ).all()
    serializer_class = SeasonClubSerializer

class MatchViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Match.objects.select_related(
        'home_club__country',
        'away_club__country',
    ).prefetch_related(
        'goal_scorers',
    ).all()
    serializer_class = MatchSerializer

class ShirtViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Shirt.objects.select_related(
        'club__country',
        'season__league__country',
        'player',
        'match__home_club__country',
        'match__away_club__country',
    ).all()
    serializer_class = ShirtSerializer