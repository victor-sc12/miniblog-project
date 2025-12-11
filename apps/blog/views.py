from django.shortcuts import render, redirect
from .models import ContenidoResenia
from apps.musica.models import *
from .forms import ContenidoReseniaForm

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

def add_resenia(request, slug):
    
    musica = Cancion.objects.get(slug=slug)

    if request.method == 'POST':
        form = ContenidoReseniaForm(request.POST)
        if form.is_valid():
            resenia = form.save(commit=False)
            resenia.musica = musica
            resenia.save()

            return redirect('detail_view', slug = slug)
    else:
        form = ContenidoReseniaForm()

    return render(request, 'blog/add_resenia.html', {'form':form, 'musica':musica})