from django.urls import path
from . import views


urlpatterns = [
    path("", views.HomeView.as_view(), name="dashboard"),
    path("pricing/", views.pricing, name="pricing"),
]
