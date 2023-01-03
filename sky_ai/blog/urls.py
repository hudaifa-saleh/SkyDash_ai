from django.urls import path
from . import views

urlpatterns = [
    path("topic/", views.blogTopic, name="blog-topic"),
    path("section/", views.blogSection, name="blog-section"),
    # saveing the blog topic for future use
    path("save/blog/topic/<str:blogTopic>/", views.saveBlogTopic, name="save-blog-topic"),
    path("use/blog/topic/<str:blogTopic>/", views.useBlogTopic, name="use-blog-topic"),
    path("view/blog/generator/<slug:slug>/", views.viewBlogGenerator, name="view-blog-generator"),
    
]
