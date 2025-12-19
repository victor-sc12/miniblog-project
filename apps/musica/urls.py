from django.urls import path, include
from . import views

urlpatterns = [
    path('artists/', views.artists_view, name='artists_view'),
    path('add/<slug:slug>/album/', views.add_album, name='add_album'),
]
