from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index_view'),
    path('<slug:slug>/detail/', views.detail_view, name='detail_view'),
    path('<slug:slug>/reseniar/', views.add_resenia, name='add_resenia'),
    path('<slug:slug>/reseniar/update/', views.edit_resenia, name='update_resenia'),
    path('<slug:slug>/delete/', views.delete_resenia, name='delete_resenia'),
]
