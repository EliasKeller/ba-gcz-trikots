from django.contrib import admin
from django.urls import path

from trikots.admin import custom_admin_dashboard

urlpatterns = [
    path("admin/", custom_admin_dashboard),
    path("admin/", admin.site.urls),
]