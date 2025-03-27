from django.db import models
from Recetas_app.models import Receta
from clientes.models import Cliente

class Venta(models.Model):
    fecha_venta = models.DateTimeField(auto_now=True)
    estatus = models.BooleanField(default=False)

class VentaDetalle(models.Model):
    UNIDADES_DE_COMPRA = [
        ('pq', 'Paquete'),
        ('g', 'Gramos'),
        ('ud', 'Unidad'),
    ]

    total = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    cantidad = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    tipo_unidad = models.CharField(
        max_length=50,
        choices=UNIDADES_DE_COMPRA,
        default='ud'
    )
    fecha_recoleccion = models.DateField(null=True, blank=True)
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE, null=False)
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    # comprado_por = models.ForeignKey(Cliente, on_delete=models.CASCADE)