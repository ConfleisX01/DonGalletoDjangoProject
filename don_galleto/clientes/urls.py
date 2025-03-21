from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from clientes.views import clientesList

urlpatterns = [
    path('clientes_crud/', clientesList, name='clientes_crud')
]