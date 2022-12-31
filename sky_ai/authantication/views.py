from django.shortcuts import render


def login(request):
    return render(request, "auth/auth-login-basic.html", {})


def register(request):
    return render(request, "auth/auth-register-basic.html", {})
