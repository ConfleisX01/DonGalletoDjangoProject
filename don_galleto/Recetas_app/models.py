from django.db import models
from django.utils.timezone import now
from materia_prima.models import MateriaPrima

class Receta(models.Model):
    """Modelo que representa una receta de galletas.""" 

    nombre = models.CharField(max_length=100)
    cantidad_galletas_producidas = models.IntegerField()
    peso_individual = models.DecimalField(max_digits=10, decimal_places=2)
    precio_galleta = models.DecimalField(max_digits=5, decimal_places=2, default=10.00)
    
    def calcular_costo(self):
        costo_total = 0
        for ingrediente in self.ingredientes.all():
            # Buscar el último lote del insumo
            ultimo_lote = ingrediente.insumo.lotes.order_by('-fecha_compra').first()
            if ultimo_lote:
                costo_total += ingrediente.cantidad_necesaria * ultimo_lote.costo_unitario
        return costo_total

    class Meta:
        permissions = [("puede_ver_recetas", "Puede ver recetas")]

    def __str__(self):
        return  f" {self.id} - {self.nombre}"


class IngredienteReceta(models.Model):
    """Modelo intermedio que representa la relación entre Receta e Insumo."""
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE, related_name="ingredientes")
    insumo = models.ForeignKey(MateriaPrima, on_delete=models.PROTECT)
    cantidad_necesaria = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.receta.nombre} - {self.insumo.nombre_insumo} ({self.cantidad_necesaria})"