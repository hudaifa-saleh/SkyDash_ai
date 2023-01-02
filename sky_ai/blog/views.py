from django.shortcuts import render, redirect
from .functions import *
from django.contrib import messages


def blog_topic(request):
    context = {}
    if request.method == "POST":
        # Retrive the blog topic string from the form the user submitted which comes in the request.POST
        blogIdea = request.POST["blogIdea"]
        # saveing the blogidea in the session to access later in another route for example
        request.session["blogIdea"] = blogIdea
        keywords = request.POST["keywords"]
        request.session["keywords"] = keywords
        audience = request.POST["audience"]
        request.session["audience"] = audience

        blogTopics = genatate_blog_topic_ideas(blogIdea, keywords)
        if len(blogTopics) > 0:
            request.session["blogTopics"] = blogTopics
            return redirect("blog-section")
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


# 'Cool gadgets ypu get right now '
# 'free gadgets, gadgets, cheap'
