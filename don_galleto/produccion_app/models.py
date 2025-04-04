from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from Recetas_app.models import Receta
from datetime import timedelta


class LoteGalletas(models.Model):
    ESTADOS = [
        ('CREADO', 'Creado'),
        ('PREPARANDO', 'Preparando'),
        ('COCINANDO', 'Cocinando'),
        ('TERMINADO', 'Terminado'),
    ]

    galleta = models.ForeignKey(Receta, on_delete=models.CASCADE, related_name='lotes')
    cantidad_lotes = models.PositiveIntegerField(default=1)
    fecha_produccion = models.DateField()
    fecha_caducidad = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='CREADO')

    @property
    def cantidad(self):
        """Devuelve la cantidad de galletas producidas por lote, tomada del modelo Receta"""
        return self.galleta.cantidad_galletas_producidas

    def esta_caducado(self):
        return now().date() > self.fecha_caducidad
    
    
    def __str__(self):
        return f"Lote {self.id} - {self.galleta.nombre_galleta} ({self.cantidad} unidades) - Vence el {self.fecha_caducidad}"

class SolicitudProduccion(models.Model):
    ESTADOS_SOLICITUD = [
        ('PENDIENTE', 'Pendiente'),
        ('APROBADA', 'Aprobada'),
        ('RECHAZADA', 'Rechazada'),
    ]

    galleta = models.ForeignKey(Receta, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=ESTADOS_SOLICITUD, default='PENDIENTE')
    fecha_solicitud = models.DateTimeField(auto_now=True)
    fecha_solicitud = models.DateTimeField(auto_now=True)
    lote_generado = models.OneToOneField(LoteGalletas, on_delete=models.SET_NULL, null=True, blank=True)

    def aprobar_solicitud(self):
        """Si la solicitud es aprobada, crea un lote y lo asocia."""
        if self.estado == 'PENDIENTE':
            lote = LoteGalletas.objects.create(
                galleta=self.galleta,
                fecha_caducidad=now().date() + timedelta(days=15),  # Ejemplo de 30 días de vida útil
                estado='CREADO'
            )
            self.lote_generado = lote
            self.estado = 'APROBADA'
            self.save()

    def __str__(self):
        return f"Solicitud {self.id} - {self.galleta.nombre_galleta} ({self.cantidad_solicitada} unidades) - Estado: {self.estado}"