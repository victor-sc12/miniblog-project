from django.urls import path, include
from . import views

urlpatterns = [
    
    # Album management urls:
    path('artists/', views.artists_view, name='artists_view'),
    path('album/<slug:slug>/add/', views.add_album, name='add_album'),
    path('album/<slug:slug>/detail/', views.album_detail, name='detail_album'),
    path('album/<slug:slug>/update/', views.album_update, name='update_album'),
    path('album/<slug:slug>/delete/', views.album_delete, name='delete_album'),
    
    # Cancion management urls:
    path('<slug:slug>/add/', views.add_song, name='add_cancion'),
    path('<slug:slug>/detail/', views.detail_song, name='detail_cancion'),
    path('<slug:slug>/update/', views.update_song, name='update_cancion'),
    path('<slug:slug>/delete/', views.delete_song, name='delete_cancion'),
]
