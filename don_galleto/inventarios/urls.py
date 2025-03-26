from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from inventarios.views import inventarioProductoView

urlpatterns = [
    path('productos/', inventarioProductoView.as_view(), name='inventario_productos'),    
]