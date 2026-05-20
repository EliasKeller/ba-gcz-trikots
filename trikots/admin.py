from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.template.response import TemplateResponse
from django.utils.html import format_html
from django.db.models import Count, Sum, Avg

from trikots.filter import CountryFilter, LeagueFilter
from trikots.models import Country, Club, League, Season, Person, Supplier, SeasonClub, Match, Shirt




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
        "get_goal_scorers",
        "result_colored",
    ]

    search_fields = [
        "home_club__name",
        "away_club__name",
        "goal_scorers__first_name",
        "goal_scorers__last_name",
    ]

    list_filter = [
        "date",
        "home_club",
        "away_club",
        "goal_scorers"
    ]

    def get_goal_scorers(self, obj):
        return ", ".join(
            [f"{p.first_name} {p.last_name}" for p in obj.goal_scorers.all()]
        )

    get_goal_scorers.short_description = "Torschützen"

    search_help_text = SEARCH_FIELD_PREFIX_PLACEHOLDER + "Datum, Heimclub..."


    ordering = ["-date"]

    list_select_related = ["home_club", "away_club"]

    list_per_page = MAX_LIST_SIZE

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

    search_help_text = SEARCH_FIELD_PREFIX_PLACEHOLDER + "Saison, Club, Präsidenten..."

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

@admin.register(Shirt)
class ShirtAdmin(admin.ModelAdmin):
    readonly_fields = ['image_preview']

    fieldsets = [
        (None, {
            'fields': [
                'image_preview',
                'image',
                'number',
                'club',
                'season',
                'match_worn',
                'player',
                'match',
                'price',
                'purchase_date',
                'description',
            ]
        }),
    ]

    list_display = [
        "number",
        "club",
        "season",
        "match_worn",
        "player",
        "match",
        "price",
        "purchase_date",
    ]

    search_fields = [
        "number",
        "club__name",
        "season__name",
        "season__league__name",
        "player__first_name",
        "player__last_name",
        "match__home_club__name",
        "match__away_club__name",
        "price",
        "purchase_date",
    ]

    list_filter = [
        "number",
        "club",
        "season",
        "player",
        "match",
        "match_worn",
        "price",
        "purchase_date",
    ]

    ordering = ["number"]

    search_help_text = SEARCH_FIELD_PREFIX_PLACEHOLDER + "Liga, Bezeichnung..."
    list_per_page = MAX_LIST_SIZE

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 300px;"/>', obj.image.url)
        return "Kein Bild"

    image_preview.short_description = "Vorschau"


# -----------------------------
#           DASHBOARD
# -----------------------------

@staff_member_required
def custom_admin_dashboard(request):
    context = admin.site.each_context(request)

    context["shirt_count"] = Shirt.objects.count()
    context["match_worn_count"] = Shirt.objects.filter(
        match_worn=True
    ).count()

    context["total_value"] = (
        Shirt.objects.aggregate(
            Sum("price")
        )["price__sum"] or 0
    )

    context["average_price"] = round(
        (
            Shirt.objects.aggregate(
                Avg("price")
            )["price__avg"] or 0
        ),
        2
    )

    context["top_clubs"] = (
        Shirt.objects
        .values("club__name")
        .annotate(total=Count("id"))
        .order_by("-total")[:5]
    )

    context["top_players"] = (
        Shirt.objects
        .exclude(player=None)
        .values(
            "player__first_name",
            "player__last_name"
        )
        .annotate(total=Count("id"))
        .order_by("-total")[:5]
    )

    context["club_count"] = Club.objects.count()
    context["league_count"] = League.objects.count()
    context["player_count"] = Person.objects.count()
    context["season_count"] = Season.objects.count()

    return TemplateResponse(
        request,
        "admin/index.html",
        context
    )