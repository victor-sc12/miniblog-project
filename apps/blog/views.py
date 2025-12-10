from django.shortcuts import render
from .models import ContenidoResenia
from apps.musica.models import *

# Create your views here.
def index(request):
    musicas = Cancion.objects.select_related('album__artista').prefetch_related('resenias')
    
    # Extend context with 'resenias' query
    for musica in musicas:
        musica.resenias_list = musica.resenias.all()
    
    return render(request, 'blog/index.html', {'musicas': musicas})

def detail_view(request, slug):
    musica = Cancion.objects.prefetch_related('resenias').get(slug=slug)
    resenias = musica.resenias.all()
    return render(request, 'blog/music_detail.html', {'musica':musica, 'resenias':resenias})
