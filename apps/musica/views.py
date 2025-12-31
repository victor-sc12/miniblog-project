from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.

def artists_view(request):
    artistas = Artista.objects.prefetch_related('albums')

    for artista in artistas:
        artista.albumes_list = artista.albums.all()

    return render(request, 'musica/artists.html', {'artistas':artistas})

def album_detail(request, slug):
    album = Album.objects.prefetch_related('canciones').get(slug = slug)
    canciones = album.canciones.all()
    return render(request, 'musica/album_detail.html', {'album':album, 'canciones':canciones})

# Album CRUD Views:
@login_required
@permission_required('musica.add_album', raise_exception=True)
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

@login_required
@permission_required('musica.change_album', raise_exception=True)
def album_update(request, slug):
    album = Album.objects.get(slug = slug)

    if request.method == 'POST':
        form = AlbumForm(request.POST, instance=album)
        if form.is_valid():
            form.save()
            return redirect('detail_album', slug=slug)
    
    else:
        form = AlbumForm(instance=album)
    
    return render(request, 'musica/album_update.html', {'form':form, 'album':album})
    
@login_required
@permission_required('musica.delete_album', raise_exception=True)
def album_delete(request, slug):
    album = Album.objects.get(slug = slug)

    if request.method == 'POST':
        album.delete()
        return redirect('artists_view')
    
    return render(request, 'musica/album_delete.html', {'album': album})

# Cancion CRUD Views:
def add_inline_songs(request, slug):
    album = Album.objects.get(slug = slug)
    if request.method == 'POST':
        formset = CancionInlineFormSet(request.POST, instance=album)
        if formset.is_valid():
            formset.save()
            return redirect('detail_album', slug=slug)
    else:
        formset = CancionInlineFormSet(queryset=Cancion.objects.none(), instance=album)

    return render(request, 'musica/add_cancion.html', {'formset':formset})