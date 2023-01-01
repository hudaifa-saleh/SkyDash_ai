from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import authenticate  # , login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test


def anonymous_required(function=None, redirect_url=None):
    if not redirect_url:
        redirect_url = "dashboard"
    actual_decorator = user_passes_test(lambda u: u.is_anonymous, login_url=redirect_url)
    if function:
        return actual_decorator(function)
    return actual_decorator


@anonymous_required
def login_(request):
    if request.method == "POST":
        email = request.POST["email"].replace("", "").lower()
        password = request.POST["password"]

        user = authenticate(username=email, password=password)
        if user:
            auth.login(request, user)
            return redirect("index")
        else:
            messages.error(request, "Incorrect email or password")
            return redirect("register")

    return render(request, "auth/auth-login-basic.html", {})


@anonymous_required
def register(request):
    if request.method == "POST":
        email = request.POST["email"].replace("", "").lower()
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
        return redirect("index")

    return render(request, "auth/auth-register-basic.html", {})


@login_required
def logout_(request):
    auth.logout(request)
    messages.success(request, "You have been logged out")
    return redirect("login")
