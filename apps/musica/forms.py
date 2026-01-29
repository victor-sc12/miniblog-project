from django import forms
from .models import *
from django.forms import inlineformset_factory, formset_factory, modelformset_factory, BaseInlineFormSet

class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artista
        fields = ['nombre']

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        exclude = ['avg_rating', 'imagen', 'slug']
    
    def __init__(self, *args, **kwargs):
        super(AlbumForm, self).__init__(*args, **kwargs)
        self.fields['artista'].disabled = True

class CancionForm(forms.ModelForm):
    class Meta:
        model = Cancion
        exclude = ['avg_rating', 'slug',]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['album'].disabled = True