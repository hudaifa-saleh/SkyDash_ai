from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test


@login_required
def dashboard(request):

    context = {}
    return render(request, "dashboard/index.html", context)
