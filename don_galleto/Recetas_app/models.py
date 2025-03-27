from django.db import models
from django.utils.timezone import now
from materia_prima.models import MateriaPrima

class Receta(models.Model):
    """Modelo que representa una receta de galletas.""" 

    nombre = models.CharField(max_length=100)
    cantidad_galletas_producidas = models.IntegerField()
    peso_individual = models.DecimalField(max_digits=10, decimal_places=2)
    precio_galleta = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    # Agregar el precio de cada galleta

    class Meta:
        permissions = [("puede_ver_recetas", "Puede ver recetas")]

    def __str__(self):
        return self.nombre


class IngredienteReceta(models.Model):
    """Modelo intermedio que representa la relación entre Receta e Insumo."""
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE, related_name="ingredientes")
    insumo = models.ForeignKey(MateriaPrima, on_delete=models.PROTECT)
    cantidad_necesaria = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.receta.nombre} - {self.insumo.nombre} ({self.cantidad_necesaria})"