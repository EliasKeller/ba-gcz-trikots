from django.contrib.admin import SimpleListFilter

from trikots.models import Country, League


class CountryFilter(SimpleListFilter):
    title = "Land"
    parameter_name = "country"

    def lookups(self, request, model_admin):
        countries = Country.objects.all()
        return [(c.id, c.name) for c in countries]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(country__id=self.value())
        return queryset

class LeagueFilter(SimpleListFilter):
    title = "Liga"
    parameter_name = "league"

    def lookups(self, request, model_admin):
        countries = League.objects.all()
        return [(c.id, c.name) for c in countries]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(country__id=self.value())
        return queryset