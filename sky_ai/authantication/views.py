from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .decorators import anonymous_required


@anonymous_required
def login(request):
    if request.method == "POST":
        email = request.POST["email"].replace(" ", "").lower()
        password = request.POST["password"]

        user = auth.authenticate(username=email, password=password)
        if user:
            auth.login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Incorrect email or password")
            return redirect("register")

    return render(request, "auth/auth-login-basic.html", {})


@anonymous_required
def register(request):
    if request.method == "POST":
        email = request.POST["email"].replace(" ", "").lower()
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if not password1 == password2:
            messages.error(request, "Please enter the correct password")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "That email address is already registered")
            return redirect("register")

        user = User.objects.create_user(email=email, username=email, password=password2)
        user.save()
        auth.login(request, user)
        return redirect("dashboard")

    return render(request, "auth/auth-register-basic.html", {})


@login_required
def logout(request):
    auth.logout(request)
    messages.success(request, "You have been logged out")
    return redirect("login")
