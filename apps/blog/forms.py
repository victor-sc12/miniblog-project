from django import forms
from .models import ContenidoResenia

# ModelForm para crear reseña:
class ContenidoReseniaForm(forms.ModelForm):
    class Meta:
        model = ContenidoResenia
        fields = ['title', 'contenido', 'calificacion']