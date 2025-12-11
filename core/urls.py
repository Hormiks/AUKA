from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('quienes-somos/', views.about, name='about'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('producto/<int:producto_id>/', views.producto_detalle, name='producto_detalle'),
]