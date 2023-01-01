from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import auth

# from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def login(request):
    return render(request, "auth/auth-login-basic.html", {})


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

        newUser = User.objects.create_user(email=email, username=email, password=password2)
        newUser.save()
        auth.login(request, newUser)
        return redirect("index")

    return render(request, "auth/auth-register-basic.html", {})
