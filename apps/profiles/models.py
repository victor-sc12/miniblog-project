from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
class User(AbstractUser):
    is_blogger = models.BooleanField(default=False)

    def __str__(self):
        return self.username or self.get_full_name()
    
class BloggerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blogger_profile')

    # definir artista favorito:
    artista = models.OneToOneField('musica.Artista', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username
    