from django.contrib import admin
from .models import *

# Inlines:
class AlbumInline(admin.StackedInline):
    model = Album
    extra = 1
    exclude = ['description', 'imagen']
    classes = ('collapse',)

class CancionInline(admin.StackedInline):
    model = Cancion
    extra = 1
    exclude = ['slug']
    classes = ('collapse',)

# Model Admin config:
@admin.register(Artista)
class ArtistaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'albumes',]
    readonly_fields = ['slug',]
    inlines = [AlbumInline]

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_filter = ['artista__nombre', 'categorias__nombre', 'year']
    list_display = ['nombre', 'artista', 'songs', 'year']
    search_fields = ['nombre', 'artista__nombre']
    readonly_fields = ['slug',]
    inlines = [CancionInline]
    fieldsets = (
        ('General', {
            'fields': ('nombre', 'artista', 'year')
        }),
        ('Detalles', {
            'fields': ('slug', 'description', 'imagen', 'categorias'),
            'classes': ('collapse',)
        })
    )

@admin.register(Cancion)
class CancionAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'album__nombre', 'album__artista__nombre']
    list_filter = ['album__nombre', 'album__artista__nombre']
    search_fields = ['album__nombre', 'album__artista__nombre']
    fieldsets = (
        ('General', {
            'fields': ('nombre', 'album')
        }),
        ('Detalles', {
            'fields': ('slug', 'description', 'avg_rating'),
            'classes': ('collapse',)
        })
    )
    readonly_fields = ['avg_rating',]

    def get_readonly_fields(self, request, obj = ...):        
        read_only = super().get_readonly_fields(request, obj)
        
        if not request.user.groups.filter(name="complete_admin").exists():
            read_only.append('slug')
        else:
            print('se supone que si eres admin completito')

        return read_only

# Register your models here.
admin.site.register(CategoriaMusical)