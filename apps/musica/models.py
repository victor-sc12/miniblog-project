from django.db import models
from django.utils.text import slugify
from django.db.models import Avg, Count
from django.utils.text import slugify

# Create your models here.
class Artista(models.Model):
    nombre = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, null=True)

    def __str__(self):
        return self.nombre
    
    @property
    def albumes(self):
        return self.albums.count()
    
    @property
    def media_rating(self):
        sum_avgs, cont = 0, 0
        for album in self.albums.all():
            if album.canciones.exclude(avg_rating=None):
                promedio = album.canciones.aggregate(promedio=Avg('avg_rating'))
                cont += 1
                sum_avgs += promedio['promedio']

        if cont == 0:
            return None
        return sum_avgs / cont   

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)     

class CategoriaMusical(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

class Album(models.Model):
    nombre = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, null=True)
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
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

class Cancion(models.Model):
    nombre = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=200, unique=True, null=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='canciones')
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True, default=None)

    def __str__(self):
        return self.nombre

    @property
    def resenias_count(self):
        return self.resenias.count()

    def media_rating(self):
        if not self.id:
            return None
        resenias = self.resenias.all()
        avg_rating = resenias.aggregate(promedio=Avg('calificacion'))
        return avg_rating['promedio']

    def save(self, **kwargs):
        self.avg_rating = self.media_rating()
        super().save(**kwargs)