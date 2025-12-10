from django.db import models
from django.utils.text import slugify

# Create your models here.
class Artista(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre
    
    @property
    def albumes(self):
        return self.albums.count()

class CategoriaMusical(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

class Album(models.Model):
    nombre = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    year = models.DateField()
    artista = models.ForeignKey(Artista, on_delete=models.CASCADE, related_name='albums')
    imagen = models.ImageField(upload_to='musica', null=True, blank=True, default=None)
    categorias = models.ManyToManyField(CategoriaMusical)

    def __str__(self):
        return self.nombre
    
    @property
    def songs(self):
        return self.canciones.count()

class Cancion(models.Model):
    nombre = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=200, unique=True, null=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='canciones')

    def __str__(self):
        return self.nombre
