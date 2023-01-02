from django.shortcuts import render, redirect
from .functions import *
from django.contrib import messages


def blog_topic(request):
    context = {}
    if request.method == "POST":
        blogIdea = request.POST["blogIdea"]
        keywords = request.POST["keywords"]
        blogTopics = genatate_blog_topic_ideas(blogIdea, keywords)
        if len(blogTopics) > 0:
            request.session["blogTopics"] = blogTopics
            return redirect("blog_section")
        else:
            messages.error(request, "Try again later")
    return render(request, "dashboard/blog_topic.html", context)


def blog_section(request):
    if "blogTopics" in request.session:
        pass
    else:
        messages.error(request, "start by creating a new blog section")
        return redirect("blog-topic")

    context = {}
    context["blogTopics"] = request.session["blogTopics"]
    return render(request, "dashboard/blog_section.html", context)
