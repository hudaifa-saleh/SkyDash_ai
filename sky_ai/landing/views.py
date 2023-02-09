from django.views import View
from django.shortcuts import render


class HomeView(View):
    def get(self, request):
        return render(request, "landing/index.html", {})


# def pricing(request):
#     return render(request, "landing/pricing.html", {})
