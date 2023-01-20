import time
from django.shortcuts import render, redirect
from .functions import (
    checkCountAllowance,
    genarateBlogSectionDetail,
    genarateBlogtoSectionTitles,
    genarateBlogtoTpicIdeas,
)
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Blog, BlogSection


@login_required
def home(request):
    emptyBlog = []
    completedBlog = []
    monthCount = 0
    blogs = Blog.objects.filter(profile=request.user.profile)
    for blog in blogs:
        sections = BlogSection.objects.filter(blog=blog)
        if sections.exists():  # calculate blog worrds
            blogWords = 0
            for section in sections:
                blogWords += int(section.wordCount)
                monthCount += int(section.wordCount)
            blog.wordCount = str(blogWords)
            blog.save()
            completedBlog.append(blog)
        else:
            emptyBlog.append(blog)

    allowance = checkCountAllowance(request.user.profile)
    context = {}
    context["numBlogs"] = len(completedBlog)
    context["monthCount"] = str(monthCount)
    context["countReset"] = "12 July 2023"
    context["emptyBlog"] = emptyBlog
    context["completedBlog"] = completedBlog
    context["allowance"] = allowance
    return render(request, "dashboard/home.html", context)


@login_required
def blogTopic(request):
    context = {}
    if request.method == "POST":
        blogIdea = request.POST["blogIdea"]  # Retrive the blog topic string from the form the user submitted which comes in the request.POST
        request.session["blogIdea"] = blogIdea  # saveing the blogidea in the session to access later in another route for example
        keywords = request.POST["keywords"]
        request.session["keywords"] = keywords
        audience = request.POST["audience"]
        request.session["audience"] = audience

        blogTopics = genarateBlogtoTpicIdeas(blogIdea, audience, keywords)
        if len(blogTopics) > 0:
            request.session["blogTopics"] = blogTopics
            return redirect("blog_sections")
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
    if "blogIdea" in request.session and "keywords" in request.session and "audience" in request.session and "blogTopics" in request.session:
        blog = Blog.objects.create(
            title=blogTopic,
            blogIdea=request.session["blogIdea"],
            keywords=request.session["keywords"],
            audience=request.session["audience"],
            profile=request.user.profile,
        )
        blog.save()
        blogTopics = request.session["blogTopics"]
        blogTopics.remove(blogTopic)
        request.session["blogTopics"] = blogTopics
        return redirect("blog_sections")
    else:
        return redirect("blog_topic")


@login_required
def useBlogTopic(request, blogTopic):
    context = {}
    if "blogIdea" in request.session and "keywords" in request.session and "audience" in request.session:
        blog = Blog.objects.create(
            title=blogTopic,
            blogIdea=request.session["blogIdea"],  # topic
            keywords=request.session["keywords"],
            audience=request.session["audience"],
            profile=request.user.profile,
        )
        blog.save()
        blogSections = genarateBlogtoSectionTitles(blogTopic, request.session["audience"], request.session["keywords"])
    else:
        return redirect("blog_topic")
    if len(blogSections) > 0:
        request.session["blogSections"] = blogSections  # Adding the section to the session
        context["blogSections"] = blogSections  # Adding the section to the context
    else:
        messages.error(request, "Oops, you beat the AI try again")
        return redirect("blog_topic")

    if request.method == "POST":
        for val in request.POST:
            if not "csrfmiddlewaretoken" in val:  # Generation the blog section details
                section = genarateBlogSectionDetail(blogTopic, val, request.session["audience"], request.session["keywords"])
                blogSec = BlogSection.objects.create(title=val, body=section, blog=blog)
                blogSec.save()
        return redirect("view_blog_generator", slug=blog.slug)
    return render(request, "dashboard/selact-blog_section.html", context)


@login_required
def deleteBlogTopic(request, uniqueId):
    try:
        blog = Blog.objects.get(uniqueId=uniqueId)
        if blog.profile == request.user.profile:
            blog.delete()
            return redirect("dashboard")
        else:
            messages.error(request, "Somthing went worng try again.")
            return redirect("dashboard")
    except:
        messages.error(request, "Blog not found")
        return redirect("dashboard")


@login_required
def viewBlogGenerator(request, slug):
    try:
        blog = Blog.objects.get(slug=slug)
    except:
        messages.error(request, "Something went wrong")
        return redirect("blog-topic")

    blogSection = BlogSection.objects.filter(blog=blog)
    context = {}
    context["blog"] = blog
    context["blogSections"] = blogSection

    return render(request, "dashboard/view-blog-generator.html", context)


@login_required
def createBlogFromTopic(request, uniqueId):
    context = {}
    try:
        blog = Blog.objects.get(uniqueId=uniqueId)
    except:
        messages.error(request, "Blog not found")
        return redirect("dashboard")

    blogSections = genarateBlogtoSectionTitles(blog.title, blog.audience, blog.keywords)
    if len(blogSections) > 0:
        request.session["blogSections"] = blogSections
        context["blogSections"] = blogSections
    else:
        messages.error(request, "Oops, you beat the AI try again")
        return redirect("blog_topic")

    if request.method == "POST":
        for val in request.POST:
            if not "csrfmiddlewaretoken" in val:  # Generation the blog section details
                section = genarateBlogSectionDetail(val, blog.title, blog.audience, blog.keywords)
                blogSec = BlogSection.objects.create(title=val, body=section, blog=blog)
                blogSec.save()
        return redirect("view_blog_generator", slug=blog.slug)
    return render(request, "dashboard/selact-blog_section.html", context)


########################### Billing #######################################
@login_required
def billing(request):
    return render(request, "dashboard/billing.html", {})
