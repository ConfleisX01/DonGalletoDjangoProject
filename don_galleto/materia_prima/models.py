from django.db import models
from provedores.models import Provedor
from django.utils.timezone import now

class MateriaPrima(models.Model):
    UNIDADES_DE_MEDIDA = [
        ('g', 'Gramo'),
        ('ml', 'Mililitro'),
        ('ud', 'Unidad'),
    ]

    nombre_insumo = models.CharField(max_length=255, unique=True)
    unidad_base = models.CharField(
        max_length=50,
        choices=UNIDADES_DE_MEDIDA,
        default='kg'
    )

    def __str__(self):
        return f"{self.nombre_insumo}-{self.unidad_base}" 

class LoteMateriaPrima(models.Model):
    insumo = models.ForeignKey(MateriaPrima, on_delete=models.CASCADE, related_name='lotes')
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    fecha_compra = models.DateField(auto_now=True)
    fecha_caducidad = models.DateField(null=False)
    proveedor = models.ForeignKey(Provedor, on_delete=models.DO_NOTHING ,related_name='insumo_proveedor')
    costo_uniario = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0.0)
    
    def esta_caducado(self):
        return now().date() > self.fecha_caducidad
    
    def __str__(self):
        return f"Lote {self.id} - {self.insumo.nombre_insumo} {self.cantidad} - Vence el {self.fecha_caducidad}"
