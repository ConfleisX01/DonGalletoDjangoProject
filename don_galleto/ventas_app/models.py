from django.db import models
from Recetas_app.models import Receta
from clientes.models import Cliente
from decimal import Decimal
from django.contrib.auth.models import User

def calcularPrecioGalleta(tipo_compra, cantidad, precio_galleta, peso_galleta):
    cantidad = Decimal(cantidad)
    precio_galleta = Decimal(precio_galleta)
    
    if tipo_compra == 'pq':  # Para paquetes (12 galletas)
        descuento = Decimal("0.10")  # 10% de descuento
        precio_total = cantidad * 12 * precio_galleta
        return precio_total * (1 - descuento)  # Aplicar descuento
    elif tipo_compra == 'g':  # Para gramos
        return (cantidad / Decimal(peso_galleta)) * precio_galleta
    elif tipo_compra == 'ud':  # Para unidades
        return cantidad * precio_galleta
    return Decimal(0)

class Venta(models.Model):  
    ESTATUS_PEDIDO = [
        ('0', 'Creado'),
        ('1', 'Pagado'),
        ('2', 'En preparación'),
        ('3', 'Listo'),
        ('4', 'Entregado'),
    ]

    fecha_venta = models.DateTimeField(auto_now=True)
    estatus = models.CharField(
        max_length=1,
        choices=ESTATUS_PEDIDO,
        default='0'
    )
    fecha_recoleccion = models.DateField(blank=True, null=True)

    def confirmar_pedido(self):
        self.estatus = '1'
        self.save()

class CarritoCompras(models.Model):  
    ESTATUS_CARRITO = [
        ('0', 'Abierto'),
        ('1', 'Confirmado'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    creado_el = models.DateTimeField(auto_now=True)
    estatus = models.CharField(
        max_length=1,
        choices=ESTATUS_CARRITO,
        default='0'
    )
    
    def agregar_producto(self, receta, cantidad, tipo_unidad, precio_galleta):
        total = calcularPrecioGalleta(tipo_unidad, cantidad, precio_galleta, receta.peso_individual)

        detalle = self.detalles.create(
            receta=receta,
            cantidad=cantidad,
            tipo_unidad=tipo_unidad,
            total=total
        )

        return detalle

    def confirmar_pedido(self):
        for detalle in self.detalles.all():
            if detalle.venta:
                detalle.venta.confirmar_pedido()

    def eliminar_producto(self, detalle_id):
        detalle = self.detalles.get(id=detalle_id)
        detalle.delete()

    def calcular_total(self):
        total = sum(item.total for item in self.detalles.all())
        return round(total, 2)
    
    def vaciar_carrito(self):
        self.detalle.all().delete()

    def contar_productos(self):
        return self.detalles.count()

class VentaDetalle(models.Model):  
    UNIDADES_DE_COMPRA = [
        ('pq', 'Paquete'),
        ('g', 'Gramos'),
        ('ud', 'Unidad'),
    ]

    total = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    cantidad = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    tipo_unidad = models.CharField(
        max_length=2,
        choices=UNIDADES_DE_COMPRA,
        default='ud'
    )
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE)
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, null=True, blank=True)
    carrito = models.ForeignKey(CarritoCompras, on_delete=models.CASCADE, related_name="detalles", null=True, blank=True)