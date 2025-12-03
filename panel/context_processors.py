from .models import PuntoVenta
from django.core.exceptions import FieldError

def puntos_venta_context(request):
    try:
        # Solo puntos fijos y activos para el footer
        puntos_venta = PuntoVenta.objects.filter(activo=True)
        
        # Intentar filtrar por tipo='fijo' si el campo existe
        try:
            puntos_venta = puntos_venta.filter(tipo='fijo')
        except (FieldError, AttributeError):
            # Si el campo 'tipo' no existe, mostrar todos los puntos activos
            # Esto puede pasar si la migración no se ha aplicado aún
            pass
        
        puntos_venta = puntos_venta.order_by('nombre')
        return {
            'puntos_venta': puntos_venta
        }
    except Exception as e:
        # Si hay algún error, retornar lista vacía para evitar errores 500
        return {
            'puntos_venta': []
        }
