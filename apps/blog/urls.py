from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index_view'),
    path('resenia/<slug:slug>/detail/', views.detail_view, name='detail_view'),
    path('resenia/<slug:slug>/add/', views.add_resenia, name='add_resenia'),
    path('resenia/<slug:slug>/update/', views.edit_resenia, name='update_resenia'),
    path('resenia/<slug:slug>/delete/', views.delete_resenia, name='delete_resenia'),
    path('resenia/<int:pk>/liked/', views.liked_resenia, name='liked_resenia'),
]
