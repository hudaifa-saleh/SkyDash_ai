from django.urls import path
from . import views

urlpatterns = [
    path("blog/topic/", views.blogTopic, name="blog-topic"),
    path("blog/section/", views.blogSection, name="blog-section"),
    # saveing the blog topic for future use
    path("save/blog/topic/<str:blogTopic>/", views.saveBlogTopic, name="save-blog-topic"),
    path("use/blog/topic/", views.useBlogTopic, name="use-blog-topic"),
]
