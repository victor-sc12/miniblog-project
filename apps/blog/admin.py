from django.contrib import admin
from .models import ContenidoResenia

# Register your models here.
class ContenidoReseniaAdmin(admin.ModelAdmin):
    readonly_fields = ['created_date', 'updated_date']

admin.site.register(ContenidoResenia)