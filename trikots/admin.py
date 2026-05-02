from django.contrib import admin

from trikots.models import Country, Club, League, Season, Person, Supplier

admin.site.register(Country)
admin.site.register(Club)
admin.site.register(League)
admin.site.register(Season)
admin.site.register(Person)
admin.site.register(Supplier)