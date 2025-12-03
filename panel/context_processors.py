from .models import PuntoVenta

def puntos_venta_context(request):
    try:
        puntos_venta = PuntoVenta.objects.filter(activo=True).order_by('nombre')
        return {
            'puntos_venta': puntos_venta
        }
    except Exception:
        # Si hay algún error (por ejemplo, tabla no existe), retornar lista vacía
        return {
            'puntos_venta': []
        }
