from django.urls import path, include
from . import views

urlpatterns = [
    
    # Album management urls:
    path('artists/', views.artists_view, name='artists_view'),
    path('add/<slug:slug>/album/', views.add_album, name='add_album'),
    path('<slug:slug>/detail/', views.album_detail, name='detail_album'),
    path('<slug:slug>/update/', views.album_update, name='update_album'),
    path('<slug:slug>/delete/', views.album_delete, name='delete_album'),
    
    # Cancion management urls:
    path('add/<slug:slug>/song/', views.add_inline_songs, name='add_cancion'),
]
