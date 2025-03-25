from django.db import models
from django.utils.timezone import now  

# MODELO CREADO APARTIR DE LA BASA DE DATOS DE LUIS

# !!!!!!Insumos temporales hasta tener los reales que quien sabe a quien vrga le toco!!!!!!
class MateriaPrima(models.Model):
    nombreIn = models.CharField(max_length=255, unique=True)
    unidad_base = models.CharField(max_length=50)  
    cantidad_disponible = models.DecimalField(max_digits=10, decimal_places=2, default=0) #CREO QUE SE REFIERE A LA CANTIDAD DE GALLETAS QUE SE HACEN? POR ANALIZAR

    def __str__(self):
        return self.nombreIn

class Receta(models.Model):
    """Modelo que representa una receta de galletas.""" 

    nombre = models.CharField(max_length=100)
    cantidad_galletas_producidas = models.IntegerField()
    peso_individual = models.DecimalField(max_digits=10, decimal_places=2)

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


