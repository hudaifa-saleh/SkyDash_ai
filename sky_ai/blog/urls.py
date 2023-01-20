from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.home, name="dashboard"),
    path("blog-topic/", views.blogTopic, name="blog_topic"),
    path("blog-sections/", views.blogSection, name="blog_sections"),
    # saveing the blog topic for future use
    path("create-blog-from-topic/<str:uniqueId>/", views.createBlogFromTopic, name="create_blog_from_topic"),
    path("delete-blog_topic/<str:uniqueId>/", views.deleteBlogTopic, name="delete_blog_topic"),
    path("save-blog_topic/<str:blogTopic>/", views.saveBlogTopic, name="save_blog_topic"),
    path("use-blog_topic/<str:blogTopic>/", views.useBlogTopic, name="use_blog_topic"),
    path("view-blog-generator/<slug:slug>/", views.viewBlogGenerator, name="view_blog_generator"),
]
