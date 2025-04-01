# models.py en produccion_app
from django.db import models
from materia_prima.models import MateriaPrima
from Recetas_app.models import Receta

class Produccion(models.Model):
    ESTADOS = [
        ('en_proceso', 'En Proceso'),
        ('finalizado', 'Finalizado'),
    ]
    
    nombre_producto = models.ForeignKey(Receta, on_delete=models.CASCADE)
    cantidad_producida = models.IntegerField() 
    materia_prima = models.ForeignKey(MateriaPrima, on_delete=models.CASCADE)
    cantidad_materia_prima_utilizada = models.IntegerField() 
    estado = models.CharField(max_length=20, choices=ESTADOS, default='en_proceso')
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_finalizacion = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.estado}"

    def finalizar_produccion(self):
        self.estado = 'finalizado'
        self.fecha_finalizacion = models.DateTimeField(auto_now=True)
        self.save()
