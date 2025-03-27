from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateView
from django.views.generic.base import View
from django.views.generic import FormView
from django.urls import reverse_lazy
from inventarios.models import InventarioProducto, InventarioMaterial

class inventarioProductoView(TemplateView):
    template_name = 'inventario_productos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        listaGalletas = InventarioProducto.objects.all()
        context['lista']=listaGalletas
        return context
    
class inventrioMateriaView(TemplateView):
    template_name = 'inventario_materia.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        listaInsumos = InventarioMaterial.objects.all()
        context['lista']=listaInsumos
        return context