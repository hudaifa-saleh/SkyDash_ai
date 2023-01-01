from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("landing/", include("landing.urls")),
    path("auth/", include("authantication.urls")),
    path("dashboard/", include("dashboard.urls")),
]
