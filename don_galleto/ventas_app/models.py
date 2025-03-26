from django.db import models
from Recetas_app.models import Receta

class Venta(models.Model):
    fecha_venta = models.DateTimeField(auto_now=True)

class VentaDetalle(models.Model):
    venta = models.OneToOneField(Venta, on_delete=models.CASCADE)
    receta = models.ManyToManyField