from ..forms import AlbumForm
from ..models import *
from django.db.models import Avg, Sum, Count
from django.forms import modelformset_factory

def run():
    artitsa = Artista.objects.get(nombre__icontains = 'spin')
    albums = artitsa.albums.all()
    suma = albums.aggregate(canciones = Count('canciones'))
    print(artitsa.albumes)
    print(artitsa, suma['canciones'])