from django.db import models

class MateriaPrima(models.Model):
    UNIDADES_DE_MEDIDA = [
        ('kg', 'Kilogramo'),
        ('g', 'Gramo'),
        ('l', 'Litro'),
        ('ml', 'Mililitro'),
        ('m', 'Metro'),
        ('cm', 'Centímetro'),
        ('ud', 'Unidad'),
    ]

    nombre_insumo = models.CharField(max_length=255, unique=True)
    unidad_base = models.CharField(
        max_length=50,
        choices=UNIDADES_DE_MEDIDA,
        default='kg'
    )

    def __str__(self):
        return self.nombre_insumo
