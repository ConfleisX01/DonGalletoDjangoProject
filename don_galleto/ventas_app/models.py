from django.db import models

# Modelo Venta
class Venta(models.Model):
    fecha = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"Venta del {self.fecha.strftime('%Y-%m-%d %H:%M:%S')}"


# Modelo Receta
class Receta(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

# Modelo DetalleVenta
class DetalleVenta(models.Model):
    id_venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    id_receta = models.ForeignKey(Receta, on_delete=models.CASCADE)  
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detalle de venta {self.id_venta} - Receta {self.id_receta}"
