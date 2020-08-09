from django.urls import path

from . import views

urlpatterns = [
    path('clips/', views.get_clips, name='clips'),
    path('', views.index, name='index'),
]
