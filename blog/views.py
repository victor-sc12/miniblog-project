from django.shortcuts import render
from .models import ContenidoResenia

# Create your views here.
def index(request):
    contenidos = ContenidoResenia.objects.all()
    return render(request, 'blog/index.html', {'contenidos':contenidos})