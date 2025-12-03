from django.shortcuts import render
from panel.models import Producto, ContenidoInstitucional

def home(request):
    return render(request, "site/home.html")

def about(request):
    contenido = ContenidoInstitucional.objects.order_by("-actualizado").first()
    return render(request, "site/about.html", {"contenido": contenido})

def catalogo(request):
    productos = Producto.objects.filter(activo=True).order_by("nombre")
    return render(request, "site/catalogo.html", {"productos": productos})
