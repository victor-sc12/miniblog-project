from django.shortcuts import render
from .models import *
from .forms import *

# Create your views here.
def artists_view(request):
    artistas = Artista.objects.all()
    return render(request, 'musica/artists.html', {'artistas':artistas})

def add_album(request, pk):
    if request.method == 'POST':
        form = AlbumForm(request.POST)
        if form.is_valid():
            album_instance = form.save(commit=False)
            album_instance.artista = Artista.objects.get(id=pk)
            album_instance.save()
    else:
        form = AlbumForm()
    
    return render(request, 'musica/add_album.html', context={'form':form})