from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

# Aplicar login_required a todas las vistas del panel
# Esto asegura que toda la ruta /panel/ esté protegida
urlpatterns = [
#                                              PANEL ADMINISTRADOR
    # Pág principal del panel
    path('', login_required(views.inicio_admin), name='inicio_admin'),

    # productos - IMPORTANTE: Las URLs más específicas deben ir ANTES de las genéricas
    path('catalogo/', login_required(views.mi_panel), name='mi_panel'),
    path('catalogo/agregar/', login_required(views.agregar_producto), name='agregar_producto'),  # ← MOVER ESTA ANTES
    path('catalogo/editar/<int:producto_id>/', login_required(views.editar_producto), name='editar_producto'),
    path('catalogo/eliminar/<int:producto_id>/', login_required(views.eliminar_producto), name='eliminar_producto'),
    path('catalogo/<str:categoria_id>/', login_required(views.categoria_servicios), name='categoria_servicios'),  # ← ESTA VA AL FINAL

    # Contenido institucional (Quiénes somos)
    path('institucional/', login_required(views.editar_contenido_institucional), name='editar_contenido_institucional'),

    # Puntos de venta
    path('puntos-venta/', login_required(views.lista_puntos_venta), name='lista_puntos_venta'),
    path('puntos-venta/agregar/', login_required(views.agregar_punto_venta), name='agregar_punto_venta'),
    path('puntos-venta/editar/<int:pk>/', login_required(views.editar_punto_venta), name='editar_punto_venta'),
    path('puntos-venta/eliminar/<int:pk>/', login_required(views.eliminar_punto_venta), name='eliminar_punto_venta'),


#Paginas

]

