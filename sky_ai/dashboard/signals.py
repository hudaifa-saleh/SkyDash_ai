from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instace, created, *args, **kwargs):
    if created:
        Profile.objects.create(user=instace)


@receiver(post_save, sender=User)
def save_profile(sender, instace, *args, **kwargs):
    instace.profile.save()
