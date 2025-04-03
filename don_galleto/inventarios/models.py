from django.db import models
from Recetas_app.models import Receta
from materia_prima.models import MateriaPrima

class InventarioProducto(models.Model):
    galleta = models.OneToOneField(Receta, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=1)
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.galleta.nombre_galleta} - {self.cantidad} unidades"
    
    def incrementar_stock(self, cantidad):
        if cantidad > 0:
            self.cantidad += cantidad
            self.save()

    def disminuir_cantidad(self, cantidad):
        if cantidad > 0 and self.cantidad >= cantidad:
            self.cantidad -= cantidad
            self.save()

    def verificar_stock(self, cantidad):
        return self.cantidad >= cantidad

class InventarioMaterial(models.Model):
    insumo = models.OneToOneField(MateriaPrima, on_delete=models.CASCADE)
    cantidad = models.PositiveBigIntegerField(default=0, null=False, blank=False)
    ultima_actualizacion = models.DateTimeField(auto_now=True)