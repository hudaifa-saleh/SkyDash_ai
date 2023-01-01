from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import *
from .models import *


@login_required
def dashboard(request):
    context = {}
    return render(request, "dashboard/index.html", context)


def profile(request):
    context = {}
    user = request.user
    profile = user.profile

    if request.method == "GET":
        form = ProfileForm(instance=profile)
        context["form"] = form
        return render(request, "dashboard/profile.html", context)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile")

    return render(request, "dashboard/profile.html", context)
