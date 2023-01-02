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
        image_form = ProfileImageForm(instance=profile)
        context["form"] = form
        context["image_form"] = image_form
        return render(request, "dashboard/profile.html", context)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        image_form = ProfileImageForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile")
        if image_form.is_valid():
            image_form.save()
            return redirect("profile")

    return render(request, "dashboard/profile.html", context)
