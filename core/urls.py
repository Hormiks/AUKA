from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('quienes-somos/', views.about, name='about'),
    path('catalogo/', views.catalogo, name='catalogo'),
]