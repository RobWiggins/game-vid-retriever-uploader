from django.urls import path

from . import views

urlpatterns = [
    path('clips/', views.clips, name='clips'),
    path('', views.index, name='index'),
]
