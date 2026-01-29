from django.db import models
from django.utils.text import slugify
from django.db.models import Avg, Count
from django.utils.text import slugify

# Abstract Model:
class BaseModel(models.Model):
    slug = models.SlugField(max_length=200, unique=True, null=True)
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True, default=None)

    class Meta:
        abstract = True

    def get_slug_source(self):
        """Override en cada modelo para indicar el campo fuente"""
        raise NotImplementedError("Debes definir get_slug_source()")
    
    def get_query_source(self):
        """Override en cada modelo para indicar el query a partir del cual se obtendrá el rating"""
        raise NotImplementedError("Debes definir get_query_source()")

    def set_avg_value(self):
        query, attr = self.get_query_source()
        avg_agg = query.aggregate(promedio=Avg(attr))
        return avg_agg['promedio']

    def save(self, *args, **kwargs):
        source_value = self.get_slug_source()

        if self.pk:
            self.avg_rating = self.set_avg_value()
            original = self.__class__.objects.get(id = self.pk)

            # Si se actualiza el slug source o si no hay slug value en instancia existente:
            if original.get_slug_source() != self.get_slug_source() or not self.slug:
                self.slug = slugify(source_value)
        else:
            self.slug = slugify(source_value)
            self.avg_rating = None

        return super().save(*args, **kwargs)

# Create your models here.
class Artista(BaseModel):
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre
    
    def get_slug_source(self):
        return self.nombre
    
    def get_query_source(self):
        return self.albums.all(), 'avg_rating'

    @property
    def albumes(self):
        return self.albums.count()

class CategoriaMusical(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

class Album(BaseModel):
    nombre = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    year = models.DateField()
    artista = models.ForeignKey(Artista, on_delete=models.CASCADE, related_name='albums')
    imagen = models.ImageField(upload_to='musica', null=True, blank=True, default=None)
    categorias = models.ManyToManyField(CategoriaMusical)

    def __str__(self):
        return self.nombre
    
    def get_slug_source(self):
        return self.nombre
    
    def get_query_source(self):
        return self.canciones.all(), 'avg_rating'

    @property
    def songs(self):
        return self.canciones.count()

class Cancion(BaseModel):
    nombre = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='canciones')

    def __str__(self):
        return self.nombre
    
    def get_slug_source(self):
        return self.nombre

    def get_query_source(self):
        return self.resenias.all(), 'calificacion'

    @property
    def resenias_count(self):
        return self.resenias.count()