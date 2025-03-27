from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic import ListView, FormView
from inventarios.models import InventarioProducto
from Recetas_app.models import Receta
from . import forms
from ventas_app.models import Venta

class ListaProductosView(ListView):
    model = InventarioProducto
    template_name = 'lista_productos.html'
    context_object_name = 'productos'

class DetallesProductoView(FormView):
    template_name = 'detalles_producto.html'
    form_class = forms.DetallesProductoForm
    success_url = reverse_lazy('lista_productos')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        id = self.kwargs.get('id')
        receta = get_object_or_404(Receta, id=id)
        kwargs['initial'] = {'receta': receta}
        return kwargs
    
    def form_valid(self, form):
        nueva_venta = Venta.objects.create() # Creamos la relacion con la venta.

        detalle_venta = form.save(commit=False)
        detalle_venta.venta = nueva_venta

        inventario = InventarioProducto.objects.get(galleta=detalle_venta.receta)
        inventario.disminuir_cantidad(detalle_venta.cantidad)
        
        detalle_venta.save()

        return super().form_valid(form)