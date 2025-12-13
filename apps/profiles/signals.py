from django.db.models.signals import post_save
from django.dispatch import receiver 
from .models import BloggerProfile
from django.conf import settings

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_blogger_profile(sender, instance, created, **kwargs):
    if created and instance.is_blogger:
        BloggerProfile.objects.create(user=instance)
    