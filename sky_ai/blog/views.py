from django.shortcuts import render


def blog_topic(request):
    context = {}

    return render(request, "dashboard/blog_topic.html", context)
