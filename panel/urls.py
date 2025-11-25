from django.urls import path
from . import views

urlpatterns = [
    # Pág principal del panel
    path('', views.inicio_admin, name='inicio_admin'),

    # productos
    path('catalogo/', views.mi_panel, name='mi_panel'),
    path('catalogo/agregar/', views.agregar_producto, name='agregar_producto'),
    path('catalogo/editar/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('catalogo/eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),

    # Contenido institucional (Quiénes somos)
    path('institucional/', views.editar_contenido_institucional, name='editar_contenido_institucional'),

    # Puntos de venta
    path('puntos-venta/', views.lista_puntos_venta, name='lista_puntos_venta'),
    path('puntos-venta/agregar/', views.agregar_punto_venta, name='agregar_punto_venta'),
    path('puntos-venta/editar/<int:pk>/', views.editar_punto_venta, name='editar_punto_venta'),
    path('puntos-venta/eliminar/<int:pk>/', views.eliminar_punto_venta, name='eliminar_punto_venta'),
]

