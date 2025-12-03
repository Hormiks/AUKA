from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField




class Producto(models.Model):
    TEMPORADAS = [
        ("verano", "Verano"),
        ("otoño", "Otoño"),
        ("invierno", "Invierno"),
        ("primavera", "Primavera"),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    precio = models.IntegerField()  # Cambiado de DecimalField a IntegerField
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='productos/')
    activo = models.BooleanField(default=True)
    temporadas = MultiSelectField(max_length=50, choices=TEMPORADAS, blank=True)

    def __str__(self):
        return self.nombre

class ContenidoInstitucional(models.Model):
    """Texto que aparece en la sección 'Quiénes somos' del sitio público."""
    nuestra_historia = models.TextField(blank=True)
    nuestros_valores = models.TextField(blank=True)
    origen_productos = models.TextField(blank=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Contenido institucional"
        verbose_name_plural = "Contenido institucional"

    def __str__(self):
        return "Contenido institucional (Quiénes somos)"


class PuntoVenta(models.Model):
    TIPO_CHOICES = [
        ('fijo', 'Fijo'),
        ('temporal', 'Temporal'),
    ]
    
    """Lugares donde se venden los productos AUKA."""
    nombre = models.CharField(max_length=150)
    direccion = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=100, blank=True)
    region = models.CharField(max_length=100, blank=True)
    horario = models.CharField(max_length=200, blank=True)
    telefono = models.CharField(max_length=30, blank=True)
    link_mapa = models.URLField(blank=True, help_text="Link a Google Maps (opcional)")
    activo = models.BooleanField(default=True)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='fijo', help_text="Fijo: se muestra en el footer. Temporal: solo en la página 'Quiénes somos'")

    def __str__(self):
        return self.nombre