from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import *


@login_required
def profile(request):
    context = {}
    # profile = request.user.profile

    if request.method == "GET":
        form = ProfileForm(instance=request.user.profile)
        image_form = ProfileImageForm(instance=request.user.profile)
        context["form"] = form
        context["image_form"] = image_form
        return render(request, "dashboard/profile.html", context)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user.profile)
        image_form = ProfileImageForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect("profile")
        if image_form.is_valid():
            image_form.save()
            return redirect("profile")

    return render(request, "dashboard/profile.html", context)
