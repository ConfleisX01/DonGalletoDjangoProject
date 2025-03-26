from django.db import models
from Recetas_app.models import Receta

class Venta(models.Model):
    fecha_venta = models.DateTimeField(auto_now=True)
    estatus = models.BooleanField()

class VentaDetalle(models.Model):
    total = models.FloatField()
    cantidad = models.FloatField()
    tipo_unidad = models.CharField(max_length=50)
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE, null=False)
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, null=False)