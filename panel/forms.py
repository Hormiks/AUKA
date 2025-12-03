# forms.py
from django import forms
from .models import Producto, ContenidoInstitucional, PuntoVenta


class ProductoForm(forms.ModelForm):
    categoria_id = forms.CharField(required=False, widget=forms.HiddenInput())
    
    class Meta:
        model = Producto
        fields = ['nombre', 'precio', 'descripcion', 'imagen', 'activo', 'temporadas']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '1'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'temporadas': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        categoria_id = kwargs.pop('categoria_id', None)
        super().__init__(*args, **kwargs)
        if categoria_id:
            self.fields['categoria_id'].initial = categoria_id
            # Si no es fitoterapia, excluir el campo temporadas del formulario
            if categoria_id != 'fitoterapia':
                if 'temporadas' in self.fields:
                    del self.fields['temporadas']
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Obtener categoria_id de múltiples fuentes
        categoria_id = (
            cleaned_data.get('categoria_id') or 
            self.data.get('categoria') or 
            self.data.get('categoria_id')
        )
        
        nombre = cleaned_data.get('nombre', '').lower()
        descripcion = cleaned_data.get('descripcion', '').lower()
        
        if categoria_id:
            palabras_clave = {
                'flores-bach': {
                    'palabras': ['bach', 'flor'],
                    'nombre_categoria': 'Flores de Bach',
                },
                'masajes': {
                    'palabras': ['masaje'],
                    'nombre_categoria': 'Masajes',
                },
                'reiki': {
                    'palabras': ['reiki'],
                    'nombre_categoria': 'Reiki',
                },
                'fitoterapia': {
                    'palabras': None,
                    'nombre_categoria': 'Fitoterapia y Cosmética',
                }
            }
            
            if categoria_id in palabras_clave:
                categoria_info = palabras_clave[categoria_id]
                
                if categoria_id == 'fitoterapia':
                    # Para fitoterapia, NO debe contener las otras palabras
                    palabras_prohibidas = ['bach', 'masaje', 'reiki']
                    texto_completo = f"{nombre} {descripcion}"
                    
                    for palabra in palabras_prohibidas:
                        if palabra in texto_completo:
                            raise forms.ValidationError({
                                '__all__': [
                                    f'El servicio contiene la palabra "{palabra}" '
                                    f'que no está permitida para la categoría {categoria_info["nombre_categoria"]}. '
                                    f'Por favor, elimina esta palabra del nombre o descripción, o cambia a otra categoría.'
                                ]
                            })
                else:
                    # Para otras categorías, DEBE contener al menos una palabra clave
                    palabras = categoria_info['palabras']
                    texto_completo = f"{nombre} {descripcion}"
                    
                    contiene_palabra = any(palabra in texto_completo for palabra in palabras)
                    
                    if not contiene_palabra:
                        palabras_str = '", "'.join(palabras)
                        raise forms.ValidationError({
                            '__all__': [
                                f'El nombre o descripción debe contener al menos una de estas palabras: "{palabras_str}" '
                                f'para que el servicio aparezca en la categoría {categoria_info["nombre_categoria"]}. '
                                f'Por favor, agrega una de estas palabras al nombre o descripción antes de guardar.'
                            ]
                        })
        
        return cleaned_data


class ContenidoInstitucionalForm(forms.ModelForm):
    class Meta:
        model = ContenidoInstitucional
        fields = ['nuestra_historia', 'nuestros_valores', 'origen_productos']
        widgets = {
            'nuestra_historia': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'nuestros_valores': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'origen_productos': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
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