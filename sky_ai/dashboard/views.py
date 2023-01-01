from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import *
from .models import *


@login_required
def dashboard(request):
    context = {}
    return render(request, "dashboard/index.html", context)


def profile(request):
    context = {}
    # form = ProfileForm()
    return render(request, "dashboard/profile.html", context)
