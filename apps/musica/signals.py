from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from apps.blog.models import ContenidoResenia
from .models import *

@receiver(post_save, sender=ContenidoResenia)
def set_song_media_rating(sender, instance, created, **kwargs):

    # Receiver funct para actualizar rating promedio de canción en cuanto se instancie nuevo obj Resenia
    print("Seteando rating promedio...")
    if created:
        song = Cancion.objects.get(id=instance.musica_id)
        song.save()

@receiver(post_save, sender=ContenidoResenia)
def update_song_media_rating(sender, instance, **kwargs):
    
    # Receiver funct para actualizar rating promedio de canción en cuanto se actualize una instancia existente de Resenia
    print("Actualizando rating promedio...")
    song = Cancion.objects.get(id=instance.musica_id)
    song.save()

@receiver(post_delete, sender=ContenidoResenia)
def update_song_media_rating_post_delete(sender, instance, **kwargs):

    print("Actualizando rating promedio pos eliminación de review...")
    song = Cancion.objects.get(id=instance.musica_id)
    song.save()