from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from inventarios.views import inventarioProductoView, inventrioMateriaView

urlpatterns = [
    path('productos/', inventarioProductoView.as_view(), name='inventario_productos'),    
    path('materia_prima/', inventrioMateriaView.as_view(), name='inventario_materia'),    
]