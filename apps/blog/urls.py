from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index_view'),
    path('<slug:slug>/detail/', views.detail_view, name='detail_view'),
]
