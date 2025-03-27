from django.db import models
from Recetas_app.models import Receta
from clientes.models import Cliente
from decimal import Decimal

def calcularPrecioGalleta(tipo_compra, cantidad, precio_galleta, peso_galleta):
    cantidad = Decimal(cantidad)
    precio_galleta = Decimal(precio_galleta)
    
    if tipo_compra == 'pq':  # Para paquetes (12 galletas)
        return cantidad * 12 * precio_galleta
    elif tipo_compra == 'g':  # Para gramos
        return (cantidad / Decimal(peso_galleta)) * precio_galleta
    elif tipo_compra == 'ud':  # Para unidades
        return cantidad * precio_galleta
    return Decimal(0)

class Venta(models.Model):  # Modelo de ventas
    fecha_venta = models.DateTimeField(auto_now=True)
    estatus = models.BooleanField(default=False)

class CarritoCompras(models.Model):  # Modelo del carrito de compras
    usuario = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)
    creado_en = models.DateTimeField(auto_now=True)

    def agregar_producto(self, receta, cantidad, tipo_unidad, precio_galleta):
        total = calcularPrecioGalleta(tipo_unidad, cantidad, precio_galleta, receta.peso_individual)

        detalle = self.detalles.create(
            receta=receta,
            cantidad=cantidad,
            tipo_unidad=tipo_unidad,
            total=total
        )

        return detalle

    def eliminar_producto(self, detalle_id):
        detalle = self.detalles.get(id=detalle_id)
        detalle.delete()

    def calcular_total(self):
        total = sum(item.total for item in self.detalles.all())
        return round(total, 2)
    
    def vaciar_carrito(self):
        self.detalles.all().delete()

class VentaDetalle(models.Model):  # Modelo del detalle del pedido
    UNIDADES_DE_COMPRA = [
        ('pq', 'Paquete'),
        ('g', 'Gramos'),
        ('ud', 'Unidad'),
    ]

    total = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    cantidad = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    tipo_unidad = models.CharField(
        max_length=50,
        choices=UNIDADES_DE_COMPRA,
        default='ud'
    )
    fecha_recoleccion = models.DateField(null=True, blank=True)
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE, null=False)
    venta = models.ForeignKey("ventas_app.Venta", on_delete=models.CASCADE, null=True, blank=True)
    carrito = models.ForeignKey("ventas_app.CarritoCompras", on_delete=models.CASCADE, related_name="detalles", null=True, blank=True)
