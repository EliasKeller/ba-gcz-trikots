from django.contrib import admin
from django.utils.html import format_html

from trikots.models import Country, Club, League, Season, Person, Supplier, SeasonClub, Match, Shirt

#admin.site.register(Country)
#admin.site.register(Club)
admin.site.register(League)
admin.site.register(Season)
admin.site.register(Person)
admin.site.register(Supplier)
admin.site.register(SeasonClub)
admin.site.register(Shirt)

MAX_LIST_SIZE = 25
SEARCH_FIELD_PREFIX_PLACEHOLDER = "Such nach "

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
        "name"
    ]

    list_filter = [
        "name",
        "country__name",
    ]

    ordering = ["name"]

    search_help_text = SEARCH_FIELD_PREFIX_PLACEHOLDER + ",".join(search_fields)
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