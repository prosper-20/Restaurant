import imp
from django.db.models import signals
from django.dispatch import receiver
from django.contrib.auth.models import User
from Order.models import UserProfile
from django.db.models.signals import post_save


@receiver(post_save, sender=User)
def create_userprofile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_userprofile(sender, instance, **kwargs):
    instance.profile.save()