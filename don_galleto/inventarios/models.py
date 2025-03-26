from django.db import models

class Galleta(models.Model):
    nombre_galleta = models.CharField(max_length=100, unique=True)
    id_receta = models.IntegerField(default=1)
    fecha_creacion = models.DateField(auto_now=True)

    def __str__(self):
        return self.nombre_galleta

class InventarioProducto(models.Model):
    galleta = models.OneToOneField(Galleta, on_delete=models.CASCADE)
    cantidad = models.PositiveBigIntegerField(default=0, null=False, blank=False)
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