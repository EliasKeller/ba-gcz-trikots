from django.contrib import admin

from trikots.models import Country, Club, League, Season, Person, Supplier, SeasonClub, Match, Shirt

admin.site.register(Country)
admin.site.register(Club)
admin.site.register(League)
admin.site.register(Season)
admin.site.register(Person)
admin.site.register(Supplier)
admin.site.register(SeasonClub)
#admin.site.register(Match)
admin.site.register(Shirt)

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    search_fields = ["home_club__name", "away_club__name"]
    list_filter = ["date"]