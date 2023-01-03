from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.home, name="dashboard"),
    path("topic/", views.blogTopic, name="blog-topic"),
    path("section/", views.blogSection, name="blog-section"),
    # saveing the blog topic for future use creatBlogFromTopic
    path("create/blog/from/topic/<str:uniqueId>/", views.creatBlogFromTopic, name="create-blog-from-topic"),
    path("delete/blog/topic/<str:uniqueId>/", views.deleteBlogTopic, name="delete-blog-topic"),
    path("save/blog/topic/<str:blogTopic>/", views.saveBlogTopic, name="save-blog-topic"),
    path("use/blog/topic/<str:blogTopic>/", views.useBlogTopic, name="use-blog-topic"),
    path("view/blog/generator/<slug:slug>/", views.viewBlogGenerator, name="view-blog-generator"),
    
]
