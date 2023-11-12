from django.urls import path

from . import views

urlpatterns = [
    path("dashboard/", views.HomeView.as_view(), name="dashboard"),
    path("blog-topic/", views.blog_topic, name="blog_topic"),
    path("blog-sections/", views.blog_section, name="blog_sections"),
    # saving the blog topic for future use
    path("create-blog-from-topic/<str:uniqueId>/", views.create_blog_from_topic, name="create_blog_from_topic"),
    path("delete-blog_topic/<str:uniqueId>/", views.delete_blog_topic, name="delete_blog_topic"),
    path("save-blog_topic/<str:blogTopic>/", views.save_blog_topic, name="save_blog_topic"),
    path("use-blog_topic/<str:blogTopic>/", views.use_blog_topic, name="use_blog_topic"),
    path("view-blog-generator/<slug:slug>/", views.view_blog_generator, name="view_blog_generator"),
    # Billing
    # path("billing/", views.billing, name="billing"),
]
