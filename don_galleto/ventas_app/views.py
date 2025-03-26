from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from inventarios.models import InventarioProducto

class ListaProductosView(ListView):
    model = InventarioProducto
    template_name = 'lista_productos.html'
    context_object_name = 'productos'