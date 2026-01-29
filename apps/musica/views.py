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


# Artist C-U-D Views:
@login_required
@permission_required('musica.add_artista', raise_exception=True)
def add_artista(request):
    form = ArtistForm()

    if request.method == 'POST':
        form = ArtistForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('artists_view')
        
    return render(request, 'musica/add_artista.html', {'form':form})

@login_required
@permission_required('musica.change_artista', raise_exception=True)
def artista_update(request, slug):
    artista = Artista.objects.get(slug=slug)
    form = ArtistForm(instance=artista)

    if request.method == 'POST':
        form = ArtistForm(request.POST, instance=artista)
        if form.is_valid():
            form.save()
            return redirect('artists_view')
        
    return render(request, 'musica/artista_update.html', {'form':form, 'artista':artista})

@login_required
@permission_required('musica.delete_artista', raise_exception=True)
def artista_delete(request, slug):
    artista = Artista.objects.prefetch_related('albums').get(slug=slug)

    # Obtener número de albumes y canciones del artista:
    num_albums = artista.albumes
    num_songs = artista.albums.aggregate(canciones = Count('canciones'))

    if request.method == 'POST':
        artista.delete()
        return redirect('artists_view')
    
    return render(request, 'musica/artista_delete.html', 
                  {'artista': artista, 'num_albums':num_albums, 'num_songs':num_songs['canciones']})

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
def detail_song(request, slug):
    cancion = Cancion.objects.select_related('album__artista').get(slug = slug)
    return render(request, 'musica/cancion_detail.html', {'cancion':cancion})

@login_required
@permission_required('musica.add_cancion', raise_exception=True)
def add_song(request, slug):
    album = Album.objects.get(slug = slug)
    if request.method == 'POST':
        form = CancionForm(request.POST, initial={'album':album})
        if form.is_valid():
            form.save()
            return redirect('detail_album', slug=slug)
    else:
        form = CancionForm(initial={'album':album})

    return render(request, 'musica/add_cancion.html', {'form':form})

@login_required
@permission_required('musica.change_cancion', raise_exception=True)
def update_song(request, slug):
    cancion = Cancion.objects.select_related('album').get(slug=slug)
    if request.method == 'POST':
        form = CancionForm(request.POST, instance=cancion)
        if form.is_valid():
            form.save()
            return redirect('detail_album', slug=cancion.album.slug)
    else:
        form = CancionForm(instance=cancion)

    return render(request, 'musica/cancion_update.html', {'form':form})

@login_required
@permission_required('musica.delete_cancion', raise_exception=True)
def delete_song(request, slug):
    cancion = Cancion.objects.get(slug=slug)

    if request.method == 'POST':    
        cancion.delete()
        return redirect('detail_album', slug=cancion.album.slug)
    
    return render(request, 'musica/cancion_delete.html', {'cancion': cancion})