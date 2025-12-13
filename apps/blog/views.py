from django.shortcuts import render, redirect
from django.db.models import Q
from .models import ContenidoResenia
from apps.musica.models import *
from .forms import ContenidoReseniaForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def index(request):

    musicas = Cancion.objects.select_related('album__artista').prefetch_related('resenias')
    
    # Catch 'fav_artista'
    if request.user.is_blogger:
        fav_artista = request.user.blogger_profile.artista.nombre
    else:
        fav_artista = None

    # 1st session:
    if not request.session.get('first_session'):
        request.session['first_session'] = True
        query_search = fav_artista
    else:
        query_search = request.GET.get('query_search')

    # fiter using 'query_search':
    if query_search:
        musicas = musicas.filter(Q(album__nombre__icontains=query_search) | 
                                 Q(album__artista__nombre__icontains=query_search) | 
                                 Q(nombre__icontains=query_search))

    # Extend context with 'resenias' query
    for musica in musicas:
        musica.resenias_list = musica.resenias.all()

    # definición de paginator:
    paginator = Paginator(musicas, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'blog/index.html', {'musicas': page_obj, 'fav_artista':fav_artista, 'query_search':query_search})

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