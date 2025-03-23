from django.db import models
from django.utils.timezone import now

# Create your models here.
class Provedor(models.Model):
    provedor_nombre = models.TextField(max_length=100)
    provedor_telefono = models.TextField(max_length=100)
    provedor_identificacionNumero = models.TextField(max_length=100)
    provedor_razonSocial = models.TextField(max_length=100)
    provedor_direccion = models.TextField(max_length=100)
    provedor_email = models.TextField(max_length=100)
    provedor_tipo = models.TextField(max_length=100)
    estatus = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.provedor_nombre}-{self.provedor_telefono}-{self.provedor_identificacionNumero}-{self.provedor_razonSocial}-{self.provedor_direccion}-{self.provedor_email}-{self.provedor_tipo}-{self.estatus}"