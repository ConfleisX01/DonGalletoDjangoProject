from django.db import models
from Recetas_app.models import Receta
from materia_prima.models import MateriaPrima
from django.utils.timezone import now

class InventarioProducto(models.Model):
    galleta = models.OneToOneField(Receta, on_delete=models.CASCADE)
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.galleta.nombre_galleta} - {self.cantidad} unidades"
    
    def calcular_stock(self):
        lotes_validos = self.galleta.lotes.filter(fecha_caducidad__gte=now().date())
        stock_total = sum(lote.cantidad for lote in lotes_validos)
        return stock_total

class InventarioMaterial(models.Model):
    insumo = models.OneToOneField(MateriaPrima, on_delete=models.CASCADE)
    cantidad = models.PositiveBigIntegerField(default=0, null=False, blank=False)
    ultima_actualizacion = models.DateTimeField(auto_now=True)