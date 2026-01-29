from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from apps.blog.models import ContenidoResenia
from .models import *

@receiver([post_save, post_delete], sender=ContenidoResenia)
def update_ratings_cascade(sender, instance, **kwargs):

    # Receiver funct para actualizar 'avg_rating' en cascada de modelos correspondientes:
    # Cancion -> Album -> Artista 
    # Se ejecuta automáticamente al crear/actualizar/eliminar una reseña
    
    cancion = instance.musica

    # 1ro actualizamos 'avg_rating' de cancion
    cancion.save()

    # 2do actualizamos 'avg_rating' de album
    album = cancion.album
    album.save()

    # 3ro actualizamos 'avg_rating' de artista
    artista = album.artista
    artista.save()