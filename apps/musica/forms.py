from django import forms
from .models import *

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        exclude = ['imagen',]
    
    def __init__(self, *args, **kwargs):
        super(AlbumForm, self).__init__(*args, **kwargs)
        self.fields['artista'].disabled = True

class CancionForm(forms.ModelForm):
    class Meta:
        model = Cancion
        exclude = ['avg_rating',]
    
    def __init__(self, *args, **kwargs):
        super(CancionForm, self).__init__(*args, **kwargs)
        self.fields['album'].disabled = True