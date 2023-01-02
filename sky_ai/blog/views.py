from django.shortcuts import render, redirect
from .functions import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Blog


@login_required
def blogTopic(request):
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

        blogTopics = genarateBlogtoTpicIdeas(blogIdea, audience, keywords)
        if len(blogTopics) > 0:
            request.session["blogTopics"] = blogTopics
            return redirect("blog-section")
        else:
            messages.error(request, "Try again later")
    return render(request, "dashboard/blog_topic.html", context)


@login_required
def blogSection(request):
    if "blogTopics" in request.session:
        pass
    else:
        messages.error(request, "start by creating a new blog section")
        return redirect("blog-topic")

    context = {}
    context["blogTopics"] = request.session["blogTopics"]
    return render(request, "dashboard/blog_section.html", context)


@login_required
def saveBlogTopic(request, blogTopic):
    if "blogIdea" in request.session and "keyword" in request.session and "audience" in request.session and "blogTopics" in request.session:
        blog = Blog.objects.create(
            blogIdea=request.session["blogIdea"],
            title=blogTopic,
            audience=request.session["audience"],
            keywords=request.session["keywords"],
            profile=request.user.profile,
        )
        blogTopics = request.session["blogTopics"]
        blogTopics.remove()
        request.session["blogTopics"] = blogTopics
        return redirect("blog-section")
    else:
        return redirect("blog-topic")


@login_required
def useBlogTopic(request, blogTopic):
    pass
