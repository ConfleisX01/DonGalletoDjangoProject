from django.db import models
from django.contrib.auth.models import User


#modelo de usaurios
class Usuario(models.Model):
    user =models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=10)
    user_type = models.CharField(max_length=10, default='usuario')


    class Meta:
        permissions = [
            #permisos usaurios
            ('view_user', 'Can view user'),
            ('add_user', 'Can add user'),
            ('change_user', 'Can change user'),
            
            #permisos dash
            ('view_dashboard', 'Can view dash'),
            
            #permisos inventario
            ('view_inventario_prudcto', 'Can view inventario'),
            
            #permisos materia prima
            ('view_mareia_prima', 'Can view inventario material'),
            ('add_materia_prima', 'Can add inventario material'),
            ('change_materia_prima', 'Can change inventario material'),
            
            #permisos produccion
            ('view_lotes_produccion', 'Can view lotes produccion'),
            ('add_lotes_produccion', 'Can add lotes produccion'),
            ('add_solicitudes_produccion', 'Can add crear solicitudes produccion'),
            ('add_produccion_galletas', 'Can add change  produccion galletas'),
            
            #permisos provedores
            ('view_provedores', 'Can view provedores'),
            ('add_provedores', 'Can add provedores'),
            ('change_provedores', 'Can change provedores'),
            
            #permisos recetas
            ('view_recetas', 'Can view recetas'),
            ('add_recetas', 'Can add recetas'),
            ('change_recetas', 'Can change recetas'),
            
            #permisos ventas
            ('view_ventas', 'Can view ventas'),
            ('add_ventas', 'Can add ventas'),
            ('change_ventas', 'Can change ventas'),
        ]