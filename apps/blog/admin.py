from django.contrib import admin
from .models import ContenidoResenia

# Register your models here.
class ContenidoReseniaAdmin(admin.ModelAdmin):
    readonly_fields = ['created_date', 'updated_date']
    list_display = ['title', 'musica__nombre', 'user__username', 'calificacion']

admin.site.register(ContenidoResenia, ContenidoReseniaAdmin)