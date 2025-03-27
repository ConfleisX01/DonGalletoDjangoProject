from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import ListView, FormView
from ventas_app.models import VentaDetalle

class ListaPedidosView(ListView):
    model = VentaDetalle
    template_name = 'lista_pedidos.html'
    context_object_name = 'pedidos'