from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils import timezone
from uuid import uuid4

from dashboard.models import Profile


class Blog(models.Model):
    title = models.CharField(max_length=100)
    keywords = models.CharField(max_length=100, blank=True, null=True)
    word_count = models.CharField(max_length=100, blank=True, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "{} {}".format(self.title, self.uniqueId)

    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split("-")[4]

        self.slug = slugify("{} {}".format(self.title, self.uniqueId))
        self.last_updated = timezone.localtime(timezone.now())
        super(Blog, self).save(*args, **kwargs)


class BlogSection(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField(blank=True, null=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "{} {}".format(self.title, self.uniqueId)

    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split("-")[4]

        self.slug = slugify("{} {}".format(self.title, self.uniqueId))
        self.last_updated = timezone.localtime(timezone.now())
        super(BlogSection, self).save(*args, **kwargs)