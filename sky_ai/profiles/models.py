from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils import timezone
from uuid import uuid4
import os
from django_resized import ResizedImageField
from django.dispatch import receiver
from django.db.models.signals import post_save


class Profile(models.Model):
    SUBSCRIPTION_OPTIONS = [
        ("free", "free"),
        ("advanced", "advanced"),
        ("starter", "starter"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address_line1 = models.CharField(null=True, blank=True, max_length=100)
    address_line2 = models.CharField(null=True, blank=True, max_length=100)
    city = models.CharField(null=True, blank=True, max_length=100)
    province = models.CharField(null=True, blank=True, max_length=100)
    country = models.CharField(null=True, blank=True, max_length=100)
    postalCode = models.CharField(null=True, blank=True, max_length=100)
    profileImage = ResizedImageField(size=[200, 200], quality=90, upload_to="profileImage")
    
    # Subscription Helpers
    monthlyCount = models.CharField(null=True, blank=True, max_length=100)
    subscribed = models.BooleanField(default=False)
    subscriptionType = models.CharField(choices=SUBSCRIPTION_OPTIONS, default="free", max_length=20)
    subscriptionReference = models.CharField(null=True, blank=True, max_length=500)

    # Utility functions
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    dateCreated = models.DateTimeField(blank=True, null=True)
    lastUpdated = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "{}".format(self.user.email)

    def save(self, *args, **kwargs):
        if self.dateCreated is None:
            self.dateCreated = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split("-")[4]

        self.slug = slugify("{} {} {}".format(self.user.first_name, self.user.last_name, self.user.email))
        self.lastUpdated = timezone.localtime(timezone.now())
        super(Profile, self).save(*args, **kwargs)


@receiver(post_save, sender=User)
def createUserProfile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def saveUserProfile(sender, instance, **kwargs):
    instance.profile.save()
