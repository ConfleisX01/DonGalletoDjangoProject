from django.db import models
from django.contrib.auth.models import User


#modelo de usaurios
class Usuario(models.Model):
    user =models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=10)
    user_type = models.CharField(max_length=10, default='usuario')


    class Meta:
        permissions = [
            ('admin_permissions', 'admin actions'),
            ('user_permissions', 'user actions'),
            ('client_permissions', 'client actions'),
            
        ]