from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Producto, ContenidoInstitucional, PuntoVenta
from .forms import ProductoForm, ContenidoInstitucionalForm, PuntoVentaForm


@login_required
def inicio_admin(request):
    return render(request, 'inicio_admin.html')


@login_required
def mi_panel(request):
    categorias = [
        {
            'id': 'flores-bach',
            'nombre': 'Flores de Bach',
            'descripcion': 'Esencias florales para equilibrar emociones',
        },
        {
            'id': 'masajes',
            'nombre': 'Masajes',
            'descripcion': 'Sesiones de masaje terapéutico',
        },
        {
            'id': 'reiki',
            'nombre': 'Reiki',
            'descripcion': 'Sanación energética',
        },
        {
            'id': 'fitoterapia',
            'nombre': 'Fitoterapia y Cosmética',
            'descripcion': 'Productos herbales y cosméticos naturales',
        }
    ]
    
    return render(request, 'catalogo/panel.html', {'categorias': categorias})


@login_required
def categoria_servicios(request, categoria_id):
    productos_base = Producto.objects.filter(usuario=request.user)
    
    categorias_map = {
        'flores-bach': {
            'id': 'flores-bach',
            'nombre': 'Flores de Bach',
            'descripcion': 'Esencias florales para equilibrar emociones',
            'productos': productos_base.filter(
                Q(nombre__icontains='bach') |
                Q(descripcion__icontains='flor') |
                Q(nombre__icontains='flor')
            ).order_by("nombre")
        },
        'masajes': {
            'id': 'masajes',
            'nombre': 'Masajes',
            'descripcion': 'Sesiones de masaje terapéutico',
            'productos': productos_base.filter(
                Q(nombre__icontains='masaje') |
                Q(descripcion__icontains='masaje')
            ).order_by("nombre")
        },
        'reiki': {
            'id': 'reiki',
            'nombre': 'Reiki',
            'descripcion': 'Sanación energética',
            'productos': productos_base.filter(
                Q(nombre__icontains='reiki') |
                Q(descripcion__icontains='reiki')
            ).order_by("nombre")
        },
        'fitoterapia': {
            'id': 'fitoterapia',
            'nombre': 'Fitoterapia y Cosmética',
            'descripcion': 'Productos herbales y cosméticos naturales',
            'productos': productos_base.exclude(
                Q(nombre__icontains='bach') |
                Q(nombre__icontains='masaje') |
                Q(nombre__icontains='reiki') |
                Q(descripcion__icontains='bach') |
                Q(descripcion__icontains='masaje') |
                Q(descripcion__icontains='reiki')
            ).order_by("nombre")
        }
    }
    
    if categoria_id not in categorias_map:
        return redirect('mi_panel')
    
    categoria = categorias_map[categoria_id]
    categoria['productos'] = list(categoria['productos'])
    
    return render(request, 'catalogo/categoria_servicios.html', {'categoria': categoria})


@login_required
def agregar_producto(request):
    categoria_id = request.GET.get('categoria', None) or request.POST.get('categoria', None)
    
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, categoria_id=categoria_id)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.usuario = request.user
            if categoria_id != 'fitoterapia':
                producto.temporadas = []
            producto.save()
            if categoria_id:
                return redirect('categoria_servicios', categoria_id=categoria_id)
            return redirect('mi_panel')
    else:
        form = ProductoForm(categoria_id=categoria_id)
    
    return render(request, 'catalogo/agregar_producto.html', {
        'form': form,
        'categoria_id': categoria_id
    })


@login_required
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id, usuario=request.user)
    categoria_id = request.GET.get('categoria', None) or request.POST.get('categoria', None)
    
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto, categoria_id=categoria_id)
        if form.is_valid():
            producto = form.save(commit=False)
            if categoria_id and categoria_id != 'fitoterapia':
                producto.temporadas = []
            producto.save()
            if categoria_id:
                return redirect('categoria_servicios', categoria_id=categoria_id)
            return redirect('mi_panel')
    else:
        form = ProductoForm(instance=producto, categoria_id=categoria_id)
    
    if not categoria_id:
        nombre_lower = producto.nombre.lower()
        desc_lower = producto.descripcion.lower()
        if 'flores' in nombre_lower or 'bach' in nombre_lower:
            categoria_id = 'flores-bach'
        elif 'masaje' in nombre_lower or 'masajes' in nombre_lower:
            categoria_id = 'masajes'
        elif 'reiki' in nombre_lower:
            categoria_id = 'reiki'
        elif 'fitoterapia' in nombre_lower or 'cosmética' in nombre_lower or 'cosmetica' in nombre_lower:
            categoria_id = 'fitoterapia'
    
    return render(request, 'catalogo/editar_producto.html', {
        'form': form,
        'producto': producto,
        'categoria_id': categoria_id
    })


@login_required
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    
    if request.method == "POST":
        categoria_id = request.GET.get('categoria', None)
        producto.delete()
        if categoria_id:
            return redirect('categoria_servicios', categoria_id=categoria_id)
        return redirect('mi_panel')
    
    return redirect('mi_panel')


@login_required
def editar_contenido_institucional(request):
    contenido, created = ContenidoInstitucional.objects.get_or_create(pk=1)

    if request.method == 'POST':
        form = ContenidoInstitucionalForm(request.POST, instance=contenido)
        if form.is_valid():
            form.save()
            return redirect('inicio_admin')
    else:
        form = ContenidoInstitucionalForm(instance=contenido)

    return render(request, 'institucional/contenido_institucional.html', {
        'form': form,
        'contenido': contenido
    })


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
    return render(request, 'institucional/punto_venta_form.html', {
        'form': form,
        'titulo': 'Agregar punto de venta'
    })


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
    return render(request, 'institucional/punto_venta_form.html', {
        'form': form,
        'titulo': 'Editar punto de venta'
    })


@login_required
def eliminar_punto_venta(request, pk):
    punto = get_object_or_404(PuntoVenta, pk=pk)
    if request.method == 'POST':
        punto.delete()
    return redirect('lista_puntos_venta')