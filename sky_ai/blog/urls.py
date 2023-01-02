from django.urls import path
from . import views

urlpatterns = [
    path("blog/topic/", views.blog_topic, name="blog-topic"),
]
