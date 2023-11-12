from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from .models import Blog, BlogSection
from .utils_ai import (
    check_count_allowance,
    generate_blog_section_detail,
    generate_blog_to_section_titles,
    generate_blog_to_topic_ideas,
)


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/home.html"

    def get(self, request, *args, **kwargs):
        empty_blog = []
        completed_blog = []
        month_count = 0
        blogs = Blog.objects.filter(profile=request.user.profile)
        for blog in blogs:
            sections = BlogSection.objects.filter(blog=blog)
            if sections.exists():
                blogWords = 0
                for section in sections:
                    blogWords += int(section.wordCount)
                    month_count += int(section.wordCount)
                blog.wordCount = str(blogWords)
                blog.save()
                completed_blog.append(blog)
            else:
                empty_blog.append(blog)
        allowance = check_count_allowance(request.user.profile)
        context = {}
        context["num_blog"] = len(completed_blog)
        context["month_count"] = request.user.profile.monthlyCount
        context["count_reset"] = "12 July 2023"
        context["empty_blog"] = empty_blog
        context["completed_blog"] = completed_blog
        context["allowance"] = allowance
        return render(request, self.template_name, context)


@login_required
def home(request):
    empty_blog = []
    completed_blog = []
    month_count = 0
    blogs = Blog.objects.filter(profile=request.user.profile)
    for blog in blogs:
        sections = BlogSection.objects.filter(blog=blog)
        if sections.exists():  # calculate blog worrds
            blogWords = 0
            for section in sections:
                blogWords += int(section.wordCount)
                month_count += int(section.wordCount)
            blog.wordCount = str(blogWords)
            blog.save()
            completed_blog.append(blog)
        else:
            empty_blog.append(blog)

    allowance = check_count_allowance(request.user.profile)
    context = {}
    context["num_blog"] = len(completed_blog)
    context["month_count"] = request.user.profile.monthlyCount
    context["count_reset"] = "12 July 2023"
    context["empty_blog"] = empty_blog
    context["completed_blog"] = completed_blog
    context["allowance"] = allowance
    return render(request, "dashboard/home.html", context)


@login_required
def blog_topic(request):
    context = {}
    if request.method == "POST":
        blog_idea = request.POST.get("blog_idea")
        request.session["blog_idea"] = blog_idea
        keywords = request.POST["keywords"]
        request.session["keywords"] = keywords
        audience = request.POST["audience"]
        request.session["audience"] = audience

        blog_topics = generate_blog_to_topic_ideas(blog_idea, audience, keywords)
        if len(blog_topics) > 0:
            request.session["blog_topics"] = blog_topics
            return redirect("blog_sections")
        else:
            messages.error(request, "Try again later")
    return render(request, "dashboard/blog_topic.html", context)


@login_required
def blog_section(request):
    if "blog_topics" in request.session:
        pass
    else:
        messages.error(request, "start by creating a new blog section")
        return redirect("blog-topic")

    context = {}
    context["blog_topics"] = request.session["blog_topics"]
    return render(request, "dashboard/blog_section.html", context)


@login_required
def save_blog_topic(request, blogTopic):
    if "blog_idea" in request.session and "keywords" in request.session and "audience" in request.session and "blog_topics" in request.session:
        blog = Blog.objects.create(
            title=blogTopic,
            blog_idea=request.session["blog_idea"],
            keywords=request.session["keywords"],
            audience=request.session["audience"],
            profile=request.user.profile,
        )
        blog.save()
        blog_topics = request.session["blog_topics"]
        blog_topics.remove(blogTopic)
        request.session["blog_topics"] = blog_topics
        return redirect("blog_sections")
    else:
        return redirect("blog_topic")


@login_required
def use_blog_topic(request, blogTopic):
    context = {}

    if "blog_idea" in request.session and "keywords" in request.session and "audience" in request.session:
        blog = Blog.objects.create(
            title=blogTopic,
            blog_idea=request.session["blog_idea"],  # topic
            keywords=request.session["keywords"],
            audience=request.session["audience"],
            profile=request.user.profile,
        )
        # blog.save()
        # blog.delete()
        blog_sections = generate_blog_to_section_titles(blogTopic, request.session["audience"],
                                                        request.session["keywords"])
    else:
        return redirect("blog_topic")

    if len(blog_sections) > 0:
        request.session["blog_sections"] = blog_sections  # Adding the section to the session
        context["blog_sections"] = blog_sections  # Adding the section to the context
    else:
        messages.error(request, "Oops, you beat the AI try again")
        return redirect("blog_topic")

    if request.method == "POST":
        for val in request.POST:
            if not "csrfmiddlewaretoken" in val:  # Generation the blog section details
                section = generate_blog_section_detail(blogTopic, val, request.session["audience"],
                                                       request.session["keywords"], request.user.profile)
                blogSec = BlogSection.objects.create(title=val, body=section, blog=blog)
                blogSec.save()
        return redirect("view_blog_generator", slug=blog.slug)

    return render(request, "dashboard/selact-blog_section.html", context)


@login_required
def delete_blog_topic(request, uniqueId):
    try:
        blog = Blog.objects.get(uniqueId=uniqueId)
        if blog.profile == request.user.profile:
            blog.delete()
            return redirect("dashboard")
        else:
            messages.error(request, "Somthing went wording try again.")
            return redirect("dashboard")
    except:
        messages.error(request, "Blog not found")
        return redirect("dashboard")


@login_required
def view_blog_generator(request, slug):
    try:
        blog = Blog.objects.get(slug=slug)
    except:
        messages.error(request, "Something went wrong")
        return redirect("blog-topic")

    blog_section = BlogSection.objects.filter(blog=blog)
    context = {
        "blog": blog,
        "blog_sections": blog_section,
    }
    # context["blog"] = blog
    # context["blog_sections"] = blogSection

    return render(request, "dashboard/view-blog-generator.html", context)


@login_required
def create_blog_from_topic(request, uniqueId):
    context = {}
    try:
        blog = Blog.objects.get(uniqueId=uniqueId)
    except:
        messages.error(request, "Blog not found")
        return redirect("dashboard")

    blog_sections = generate_blog_to_section_titles(blog.title, blog.audience, blog.keywords)
    if len(blog_sections) > 0:
        request.session["blog_sections"] = blog_sections
        context["blog_sections"] = blog_sections
    else:
        messages.error(request, "Oops, you beat the AI try again")
        return redirect("blog_topic")

    if request.method == "POST":
        for val in request.POST:
            if not "csrfmiddlewaretoken" in val:  # Generation the blog section details
                section = generate_blog_section_detail(val, blog.title, blog.audience, blog.keywords,
                                                       request.user.profile)
                blogSec = BlogSection.objects.create(title=val, body=section, blog=blog)
                blogSec.save()
        return redirect("view_blog_generator", slug=blog.slug)
    return render(request, "dashboard/selact-blog_section.html", context)

# ########################### Billing #######################################
# @login_required
# def billing(request):
#     return render(request, "dashboard/billing.html", {})
