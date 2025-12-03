from .models import PuntoVenta

def puntos_venta_context(request):
    try:
        # Solo puntos fijos y activos para el footer
        # Filtrar explícitamente por tipo='fijo' y activo=True
        puntos_venta = PuntoVenta.objects.filter(
            activo=True,
            tipo='fijo'
        ).order_by('nombre')
        
        return {
            'puntos_venta': puntos_venta
        }
    except Exception:
        # Si hay algún error (por ejemplo, campo tipo no existe aún), retornar lista vacía
        # Esto evita mostrar puntos temporales si hay un problema con la migración
        return {
            'puntos_venta': []
        }
