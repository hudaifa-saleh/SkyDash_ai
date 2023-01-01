from django.urls import path
from . import views


urlpatterns = [
    path("login/", views.login_, name="login"),
    path("logout/", views.logout_, name="logout"),
    path("register/", views.register, name="register"),
]
