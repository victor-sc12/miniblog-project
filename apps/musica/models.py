from django.db import models
from django.utils.text import slugify
from django.db.models import Avg, Count
from django.utils.text import slugify

# Abstract Model:
class BaseModel(models.Model):
    slug = models.SlugField(max_length=200, unique=True, null=True)

    class Meta:
        abstract = True

    def get_slug_source(self):
        """Override en cada modelo para indicar el campo fuente"""
        raise NotImplementedError("Debes definir get_slug_source()")

    def save(self, *args, **kwargs):
        source_value = self.get_slug_source()

        if self.pk:
            original = self.__class__.objects.get(id = self.pk)

            if original.get_slug_source() != self.get_slug_source() or not self.slug:
                self.slug = slugify(source_value)
        else:
            self.slug = slugify(source_value)

        return super().save(*args, **kwargs)

# Create your models here.
class Artista(BaseModel):
    nombre = models.CharField(max_length=200)
    # slug = models.SlugField(max_length=200, unique=True, null=True)

    def __str__(self):
        return self.nombre
    
    def get_slug_source(self):
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

class CategoriaMusical(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre
    
    def get_slug_source(self):
        return self.nombre

class Album(BaseModel):
    nombre = models.CharField(max_length=200)
    # slug = models.SlugField(max_length=200, unique=True, null=True)
    description = models.TextField(blank=True, null=True)
    year = models.DateField()
    artista = models.ForeignKey(Artista, on_delete=models.CASCADE, related_name='albums')
    imagen = models.ImageField(upload_to='musica', null=True, blank=True, default=None)
    categorias = models.ManyToManyField(CategoriaMusical)

    def __str__(self):
        return self.nombre
    
    def get_slug_source(self):
        return self.nombre

    @property
    def songs(self):
        return self.canciones.count()

class Cancion(BaseModel):
    nombre = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    # slug = models.SlugField(max_length=200, unique=True, null=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='canciones')
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True, default=None)

    def __str__(self):
        return self.nombre
    
    def get_slug_source(self):
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

    def save(self, *args, **kwargs):
        self.avg_rating = self.media_rating()
        super().save(*args, **kwargs)