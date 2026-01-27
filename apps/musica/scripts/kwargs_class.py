from ..forms import AlbumForm
from ..models import *
from django.db.models import Avg
from django.forms import modelformset_factory

def run():
    album1 = Album.objects.prefetch_related('canciones').first()
    album_avrg = album1.canciones.aggregate(promedio=Avg('avg_rating'))

    for song in album1.canciones.all():
        print(song.avg_rating)