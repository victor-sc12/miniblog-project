from django import forms
from .models import *


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        exclude = ['imagen',]
    
    def __init__(self, *args, **kwargs):
        super(AlbumForm, self).__init__(*args, **kwargs)
        self.fields['artista'].disabled = True