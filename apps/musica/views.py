from django.shortcuts import render, redirect
from .models import *
from .forms import *

# Create your views here.
def artists_view(request):
    artistas = Artista.objects.prefetch_related('albums')

    for artista in artistas:
        artista.albumes_list = artista.albums.all()

    return render(request, 'musica/artists.html', {'artistas':artistas})

def add_album(request, slug):

    artista = Artista.objects.get(slug = slug)

    if request.method == 'POST':
        form = AlbumForm(request.POST, initial = {'artista':artista})
        if form.is_valid():
            form.save()
            return redirect('artists_view')
    else:
        form = AlbumForm(initial = {'artista':artista})
    
    return render(request, 'musica/add_album.html', context={'form':form})

def album_detail(request, slug):
    album = Album.objects.prefetch_related('canciones').get(slug = slug)
    canciones = album.canciones.all()
    return render(request, 'musica/album_detail.html', {'album':album, 'canciones':canciones})