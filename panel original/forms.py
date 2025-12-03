# forms.py
from django import forms
from .models import Producto, ContenidoInstitucional, PuntoVenta

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'precio', 'descripcion', 'imagen', 'activo', 'temporadas']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'temporadas': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        }

class ContenidoInstitucionalForm(forms.ModelForm):
    class Meta:
        model = ContenidoInstitucional
        fields = ['nuestra_historia', 'nuestros_valores', 'origen_productos']
        widgets = {
            'nuestra_historia': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'nuestros_valores': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'origen_productos': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class PuntoVentaForm(forms.ModelForm):
    class Meta:
        model = PuntoVenta
        fields = ['nombre', 'direccion', 'ciudad', 'region', 'horario', 'telefono', 'link_mapa', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control'}),
            'region': forms.TextInput(attrs={'class': 'form-control'}),
            'horario': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'link_mapa': forms.URLInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }