from ..forms import AlbumForm
from ..models import *
from django.forms import modelformset_factory

def run():
    # formset test:
    AlbumFormSet = modelformset_factory(Album, fields=['nombre', 'description'])
    formset = AlbumFormSet()
    print(formset)