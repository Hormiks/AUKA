from django.shortcuts import render, get_object_or_404
from panel.models import Producto, ContenidoInstitucional, PuntoVenta

def home(request):
    return render(request, "site/home.html")

def about(request):
    contenido = ContenidoInstitucional.objects.order_by("-actualizado").first()
    # Mostrar todos los puntos activos (fijos y temporales) en la página about
    # Usar un nombre diferente para no sobrescribir el context processor del footer
    puntos_venta_about = PuntoVenta.objects.filter(activo=True).order_by("nombre")
    return render(request, "site/about.html", {
        "contenido": contenido,
        "puntos_venta_about": puntos_venta_about
    })

def catalogo(request):
    productos = Producto.objects.filter(activo=True).order_by("nombre")
    
    # Categorías basadas en palabras clave en nombre o descripción
    categorias = [
        {
            'id': 'flores-bach',
            'nombre': 'Flores de Bach',
            'descripcion': 'Esencias florales para equilibrar emociones',
            'productos': productos.filter(
                nombre__icontains='bach'
            ) | productos.filter(
                descripcion__icontains='flor'
            ) | productos.filter(
                nombre__icontains='flor'
            )
        },
        {
            'id': 'masajes',
            'nombre': 'Masajes',
            'descripcion': 'Sesiones de masaje terapéutico',
            'productos': productos.filter(
                nombre__icontains='masaje'
            ) | productos.filter(
                descripcion__icontains='masaje'
            )
        },
        {
            'id': 'reiki',
            'nombre': 'Reiki',
            'descripcion': 'Sanación energética',
            'productos': productos.filter(
                nombre__icontains='reiki'
            ) | productos.filter(
                descripcion__icontains='reiki'
            )
        },
        {
            'id': 'fitoterapia',
            'nombre': 'Fitoterapia y Cosmética',
            'descripcion': 'Productos herbales y cosméticos naturales',
            'productos': productos.exclude(
                nombre__icontains='bach'
            ).exclude(
                nombre__icontains='masaje'
            ).exclude(
                nombre__icontains='reiki'
            ).exclude(
                descripcion__icontains='bach'
            ).exclude(
                descripcion__icontains='masaje'
            ).exclude(
                descripcion__icontains='reiki'
            )
        }
    ]
    
    return render(request, "site/catalogo.html", {
        "productos": productos,
        "categorias": categorias
    })

def producto_detalle(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id, activo=True)
    return render(request, "site/producto_detalle.html", {
        "producto": producto
    })
