from django.urls import path, include
from . import views

urlpatterns = [
    path('artists/', views.artists_view, name='artists_view'),
    path('add/<int:pk>/album/', views.add_album, name='add_album'),
]
