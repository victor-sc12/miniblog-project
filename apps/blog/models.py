from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings

# Create your models here.
class ContenidoResenia(models.Model):
    title = models.CharField(max_length=200)
    contenido = models.TextField()
    musica = models.ForeignKey('musica.Cancion', on_delete=models.CASCADE, related_name='resenias')
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    calificacion = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='post_resenia',
                                default=None)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, 
                                   through="Like",
                                   related_name='liked_resenias',
                                   blank=True)

    def __str__(self):
        return f'{self.title}'
    
    class Meta:
        # Asegurar one review for song:
        unique_together = ['musica', 'user']

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    resenia = models.ForeignKey(ContenidoResenia, on_delete=models.CASCADE)
    liked_at = models.DateField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'resenia'], name='user_resenia_uniq'),
        ]