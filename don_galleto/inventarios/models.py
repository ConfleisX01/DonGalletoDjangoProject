from django.db import models
from Recetas_app.models import Receta
from materia_prima.models import MateriaPrima
from django.utils.timezone import now

class InventarioProducto(models.Model):
    galleta = models.OneToOneField(Receta, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=1)
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.galleta.nombre} - {self.cantidad} unidades"
    
    def calcular_stock(self):
        lotes_validos = self.galleta.lotes.filter(fecha_caducidad__gte=now().date())
        stock_total = sum(lote.cantidad for lote in lotes_validos)
        return stock_total

    def verificar_stock(self, cantidad):
        return self.cantidad >= cantidad
    
    def disminuir_cantidad(self, cantidad_solicitada):
        self.cantidad -= cantidad_solicitada
        self.save()

    def agregar_cantidad(self, cantidad_agregada):
        self.cantidad += cantidad_agregada
        self.save()

class InventarioMaterial(models.Model):
    insumo = models.OneToOneField(MateriaPrima, on_delete=models.CASCADE)
    cantidad = models.PositiveBigIntegerField(default=0, null=False, blank=False)
    ultima_actualizacion = models.DateTimeField(auto_now=True)