from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProfileForm, ProfileImageForm
from .models import Profile


class ProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = ProfileForm(instance=request.user.profile)
        image_form = ProfileImageForm(instance=request.user.profile)
        return render(request, "dashboard/profile.html", {"form": form, "image_form": image_form})

    def post(self, request, *args, **kwargs):
        form = ProfileForm(request.POST, instance=request.user.profile)
        image_form = ProfileImageForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect("profile")
        if image_form.is_valid():
            image_form.save()
            return redirect("profile")
        return render(request, "dashboard/profile.html", {"form": form})
