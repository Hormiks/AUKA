from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Producto, ContenidoInstitucional, PuntoVenta
from .forms import ProductoForm, ContenidoInstitucionalForm, PuntoVentaForm

@login_required
def inicio_admin(request):
    return render(request, 'inicio_admin.html')

@login_required
def mi_panel(request):
    # Solo productos del usuario actual
    productos = Producto.objects.filter(usuario=request.user)
    return render(request, 'catalogo/panel.html', {'productos': productos})

@login_required
def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.usuario = request.user  # Asigna el usuario
            producto.save()
            return redirect('mi_panel')
    else:
        form = ProductoForm()
    return render(request, 'catalogo/agregar_producto.html', {'form': form})

@login_required
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id, usuario=request.user)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('mi_panel')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'catalogo/editar_producto.html', {'form': form})

@login_required
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id, usuario=request.user)
    
    if request.method == "POST":
        producto.delete()
        return redirect('mi_panel')
    
    # Si alguien entra por GET, lo mandamos de vuelta al panel
    return redirect('mi_panel')

# -------- CONTENIDO INSTITUCIONAL (QUIÉNES SOMOS) --------

@login_required
def editar_contenido_institucional(request):
    # Usamos siempre el registro con pk=1, si no existe lo creamos
    contenido, created = ContenidoInstitucional.objects.get_or_create(pk=1)

    if request.method == 'POST':
        form = ContenidoInstitucionalForm(request.POST, instance=contenido)
        if form.is_valid():
            form.save()
            return redirect('inicio_admin')
    else:
        form = ContenidoInstitucionalForm(instance=contenido)

    return render(request, 'institucional/contenido_institucional.html', {'form': form})


# -------- PUNTOS DE VENTA --------

@login_required
def lista_puntos_venta(request):
    puntos = PuntoVenta.objects.all()
    return render(request, 'institucional/puntos_venta.html', {'puntos': puntos})


@login_required
def agregar_punto_venta(request):
    if request.method == 'POST':
        form = PuntoVentaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_puntos_venta')
    else:
        form = PuntoVentaForm()
    return render(request, 'institucional/punto_venta_form.html', {'form': form, 'titulo': 'Agregar punto de venta'})


@login_required
def editar_punto_venta(request, pk):
    punto = get_object_or_404(PuntoVenta, pk=pk)
    if request.method == 'POST':
        form = PuntoVentaForm(request.POST, instance=punto)
        if form.is_valid():
            form.save()
            return redirect('lista_puntos_venta')
    else:
        form = PuntoVentaForm(instance=punto)
    return render(request, 'institucional/punto_venta_form.html', {'form': form, 'titulo': 'Editar punto de venta'})


@login_required
def eliminar_punto_venta(request, pk):
    punto = get_object_or_404(PuntoVenta, pk=pk)
    if request.method == 'POST':
        punto.delete()
    return redirect('lista_puntos_venta')