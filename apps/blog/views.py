from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from apps.blog.models import *
from apps.musica.models import *
from .forms import ContenidoReseniaForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.
def index(request):
    musicas = Cancion.objects.select_related('album__artista').prefetch_related('resenias')
    
    # print(request.user)

    if request.user.is_authenticated:
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
            query_search = request.GET.get('query_search', None)

    else:
        query_search = request.GET.get('query_search', None)

    print(query_search)

    # fiter using 'query_search':
    if query_search:
        musicas = musicas.filter(Q(album__nombre__icontains=query_search) | 
                                 Q(album__artista__nombre__icontains=query_search) | 
                                 Q(nombre__icontains=query_search))

    # Extend context with 'resenias' query
    for musica in musicas:
        musica.resenias_list = musica.resenias.all()

        if request.user.is_authenticated:
            # Comprobar si current user has review en la canción:
            musica.has_review = musica.resenias.filter(user=request.user).exists()

    # definición de paginator:
    paginator = Paginator(musicas, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'blog/index.html', {'musicas': page_obj, 'query_search':query_search})

def detail_view(request, slug):
    musica = Cancion.objects.prefetch_related('resenias').get(slug=slug)
    if request.user.is_authenticated:
        musica.has_review = musica.resenias.filter(user=request.user).exists()
    resenias = musica.resenias.all()
    return render(request, 'blog/music_detail.html', {'musica':musica, 'resenias':resenias})

@login_required
@permission_required('blog.add_contenidoresenia', raise_exception=True)
def add_resenia(request, slug):
    
    musica = Cancion.objects.get(slug=slug)

    if request.method == 'POST':
        form = ContenidoReseniaForm(request.POST)
        if form.is_valid():
            resenia = form.save(commit=False)
            resenia.musica = musica
            resenia.user = request.user
            resenia.save()

            return redirect('detail_view', slug = slug)
    else:
        form = ContenidoReseniaForm()

    return render(request, 'blog/add_resenia.html', {'form':form, 'musica':musica})

@login_required
@permission_required('blog.change_contenidoresenia', raise_exception=True)
def edit_resenia(request, slug):
    
    resenia = ContenidoResenia.objects.select_related('musica', 'user').get(musica__slug=slug, user=request.user)
    musica = resenia.musica

    if request.method == 'POST':
        form = ContenidoReseniaForm(request.POST, instance=resenia)
        if form.is_valid:
            form.save()
            return redirect('detail_view', slug = slug)
    else:
        form = ContenidoReseniaForm(instance=resenia)

    return render(request, 'blog/update_resenia.html', {'form':form, 'musica':musica})

@login_required
@permission_required('blog.delete_contenidoresenia', raise_exception=True)
def delete_resenia(request, slug):
    resenia = ContenidoResenia.objects.select_related('musica', 'user').get(musica__slug=slug, user=request.user)
    
    if request.method == 'POST':
        resenia.delete()
        return redirect('detail_view', slug)
    
    return render(request, 'blog/delete_confirm.html', {'resenia':resenia})

@login_required
def liked_resenia(request, pk):
    resenia = get_object_or_404(ContenidoResenia, id=pk)
    
    like, created = Like.objects.get_or_create(user=request.user, resenia=resenia)

    if not created:
        like.delete()

    # Obtener metadata de la solicitud entrante, en este caso 'HTTP_REFERER' (página de origen):
    return redirect(request.META.get('HTTP_REFERER', 'index_view'))