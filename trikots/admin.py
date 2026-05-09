from django.contrib import admin
from django.utils.html import format_html

from trikots.filter import CountryFilter, LeagueFilter
from trikots.models import Country, Club, League, Season, Person, Supplier, SeasonClub, Match, Shirt

#TODO: Shirt und Spiele noch final machen
admin.site.register(Shirt)

MAX_LIST_SIZE = 25
SEARCH_FIELD_PREFIX_PLACEHOLDER = "Such nach "

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):

    list_display = [
        "name",
    ]

    list_filter = [
        "name",
    ]
    ordering = ["name"]

    list_per_page = MAX_LIST_SIZE


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):

    list_display = [
        "name",
    ]

    search_fields = [
        "name"
    ]

    list_filter = [
        "name",
    ]
    ordering = ["name"]

    list_per_page = MAX_LIST_SIZE
    search_help_text = SEARCH_FIELD_PREFIX_PLACEHOLDER + ",".join(search_fields)

@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):

    list_display = [
        "name",
        "country"
    ]

    search_fields = [
        "name",
        "country__name"
    ]

    list_filter = [
        "name",
        CountryFilter,
    ]

    ordering = ["name"]

    search_help_text = SEARCH_FIELD_PREFIX_PLACEHOLDER + "Name und Land"
    list_per_page = MAX_LIST_SIZE


@admin.register(League)
class ClubAdmin(admin.ModelAdmin):

    list_display = [
        "name",
        "country"
    ]

    search_fields = [
        "name",
        "country__name"
    ]

    list_filter = [
        "name",
        CountryFilter,
    ]

    ordering = ["name"]

    search_help_text = SEARCH_FIELD_PREFIX_PLACEHOLDER + "Name und Land"
    list_per_page = MAX_LIST_SIZE


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):

    list_display = [
        "date",
        "home_club",
        "away_club",
        "result_colored",
    ]

    search_fields = [
        "home_club__name",
        "away_club__name",
    ]

    list_filter = [
        "date",
        "home_club",
        "away_club",
    ]

    ordering = ["-date"]

    list_select_related = ["home_club", "away_club"]

    list_per_page = MAX_LIST_SIZE
    search_help_text = SEARCH_FIELD_PREFIX_PLACEHOLDER + ", ".join(search_fields)

    def result_colored(self, obj):
        return format_html(
            "<strong>{}:{}</strong>",
            obj.goals_home,
            obj.goals_away
        )

    result_colored.short_description = "Resultat"

@admin.register(Person)
class ClubAdmin(admin.ModelAdmin):

    list_display = [
        "first_name",
        "last_name",
    ]

    search_fields = [
        "first_name",
        "last_name"
    ]

    list_filter = [
        "first_name",
        "last_name",
    ]

    ordering = ["first_name"]

    search_help_text = SEARCH_FIELD_PREFIX_PLACEHOLDER + "Vor- und Nachname"
    list_per_page = MAX_LIST_SIZE


@admin.register(SeasonClub)
class SeasonClubAdmin(admin.ModelAdmin):

    list_display = [
        "season",
        "club",
        "description",
        "get_presidents",
        "get_captains",
        "get_trainers",
        "supplier"
    ]

    search_fields = [
        "season__name",
        "club__name",
        "description",
        "presidents__first_name",
        "presidents__last_name",
        "captains__first_name",
        "captains__last_name",
        "trainers__first_name",
        "trainers__last_name",
        "supplier__name",
    ]

    list_filter = [
        "season",
        "club",
        "supplier",
        "presidents",
        "captains",
        "trainers",
    ]

    ordering = ["season"]

    list_per_page = MAX_LIST_SIZE

    search_help_text = (
        "Suche nach Saison, Club, Präsidenten..."
    )

    def get_presidents(self, obj):
        return ", ".join(
            [f"{p.first_name} {p.last_name}" for p in obj.presidents.all()]
        )

    get_presidents.short_description = "Präsidenten"

    def get_captains(self, obj):
        return ", ".join(
            [f"{p.first_name} {p.last_name}" for p in obj.captains.all()]
        )

    get_captains.short_description = "Captains"

    def get_trainers(self, obj):
        return ", ".join(
            [f"{p.first_name} {p.last_name}" for p in obj.trainers.all()]
        )

    get_trainers.short_description = "Trainer"

@admin.register(Season)
class ClubAdmin(admin.ModelAdmin):

    list_display = [
        "league",
        "name",
        "startYear",
        "endYear",
    ]

    search_fields = [
        "league",
        "name",
        "startYear",
        "endYear",
    ]

    list_filter = [
        LeagueFilter,
        "name",
        "startYear",
        "endYear",
    ]

    ordering = ["league"]

    search_help_text = SEARCH_FIELD_PREFIX_PLACEHOLDER + "Liga, Bezeichnung..."
    list_per_page = MAX_LIST_SIZE