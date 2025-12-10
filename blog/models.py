from django.db import models

# Create your models here.
class ContenidoResenia(models.Model):
    title = models.CharField(max_length=200)
    contenido = models.TextField()
    musica = models.ForeignKey('musica.Cancion', on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.title}'