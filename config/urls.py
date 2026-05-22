from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from trikots.admin import custom_admin_dashboard
from trikots.views import (
    CountryViewSet,
    ClubViewSet,
    LeagueViewSet,
    SeasonViewSet,
    PersonViewSet,
    SupplierViewSet,
    SeasonClubViewSet,
    MatchViewSet,
    ShirtViewSet,
)

router = DefaultRouter()
router.register(r'countries', CountryViewSet)
router.register(r'clubs', ClubViewSet)
router.register(r'leagues', LeagueViewSet)
router.register(r'seasons', SeasonViewSet)
router.register(r'persons', PersonViewSet)
router.register(r'suppliers', SupplierViewSet)
router.register(r'season-clubs', SeasonClubViewSet)
router.register(r'matches', MatchViewSet)
router.register(r'shirts', ShirtViewSet)

urlpatterns = [
    path("admin/", custom_admin_dashboard),
    path("admin/", admin.site.urls),
    path('', lambda request: redirect('/admin/')),
    path('api/', include(router.urls)),
]