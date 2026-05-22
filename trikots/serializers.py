from rest_framework import serializers
from trikots.models import Country, Club, League, Season, Person, Supplier, SeasonClub, Match, Shirt


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name']


class ClubSerializer(serializers.ModelSerializer):
    country = CountrySerializer()

    class Meta:
        model = Club
        fields = ['id', 'name', 'country']


class LeagueSerializer(serializers.ModelSerializer):
    country = CountrySerializer()

    class Meta:
        model = League
        fields = ['id', 'name', 'country']


class SeasonSerializer(serializers.ModelSerializer):
    league = LeagueSerializer()

    class Meta:
        model = Season
        fields = ['id', 'name', 'startYear', 'endYear', 'league']


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'first_name', 'last_name']


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name']


class SeasonClubSerializer(serializers.ModelSerializer):
    season = SeasonSerializer()
    club = ClubSerializer()
    supplier = SupplierSerializer()
    presidents = PersonSerializer(many=True)
    captains = PersonSerializer(many=True)
    trainers = PersonSerializer(many=True)

    class Meta:
        model = SeasonClub
        fields = [
            'id',
            'season',
            'club',
            'description',
            'presidents',
            'captains',
            'trainers',
            'supplier',
            'cup_result',
            'championship_results',
            'international_results',
        ]


class MatchSerializer(serializers.ModelSerializer):
    home_club = ClubSerializer()
    away_club = ClubSerializer()
    goal_scorers = PersonSerializer(many=True)

    class Meta:
        model = Match
        fields = [
            'id',
            'home_club',
            'away_club',
            'goals_home',
            'goals_away',
            'goal_scorers',
            'round_of_League',
            'date',
            'time',
            'highlight_url',
        ]


class ShirtSerializer(serializers.ModelSerializer):
    club = ClubSerializer()
    season = SeasonSerializer()
    player = PersonSerializer()
    match = MatchSerializer()

    class Meta:
        model = Shirt
        fields = [
            'id',
            'number',
            'image_front',
            'image_back',
            'description',
            'club',
            'season',
            'match_worn',
            'shirt_type',
            'is_goal_keeper_shirt',
            'player',
            'match',
            'price',
            'purchase_date',
        ]