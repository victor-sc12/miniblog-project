from django.db import models

# Create your models here.
class Artista(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

class CategoriaMusical(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

class Album(models.Model):
    nombre = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    year = models.DateField()
    artista = models.ForeignKey(Artista, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='musica', null=True, default=None)
    categorias = models.ManyToManyField(CategoriaMusical)

    def __str__(self):
        return self.nombre

class Cancion(models.Model):
    nombre = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre