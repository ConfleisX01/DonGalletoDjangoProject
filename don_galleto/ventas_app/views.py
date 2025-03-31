from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic import ListView, FormView
from inventarios.models import InventarioProducto
from Recetas_app.models import Receta
from . import forms
from ventas_app.models import Venta, calcularPrecioGalleta, CarritoCompras

class VerListaPedidosView(ListView):
    model = CarritoCompras
    template_name = 'lista_pedidos_cliente.html'
    context_object_name = 'pedidos'

    def get_queryset(self):
        return CarritoCompras.objects.filter(
            usuario=self.request.user,
            detalles__venta__estatus=True
        ).distinct()

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
        carrito, created = CarritoCompras.objects.get_or_create(
            usuario=self.request.user
        )

        venta, created = Venta.objects.get_or_create(
            id=carrito.id,
            defaults={"estatus": False}
        )

        if venta.estatus:
            carrito = CarritoCompras.objects.create(usuario=self.request.user)
            venta = Venta.objects.create()

        detalle_venta = form.save(commit=False)
        detalle_venta.carrito = carrito
        detalle_venta.venta = venta

        inventario = InventarioProducto.objects.get(galleta=detalle_venta.receta)
        tipo_compra = detalle_venta.tipo_unidad
        cantidad_galleta = detalle_venta.cantidad
        precio_galleta = inventario.galleta.precio_galleta
        peso_galleta = inventario.galleta.peso_individual

        precio_total_calculado = calcularPrecioGalleta(
            tipo_compra, cantidad_galleta, precio_galleta, peso_galleta
        )

        if precio_total_calculado is False:
            form.add_error(None, "No se pudo calcular el precio")
            return self.form_invalid(form)
        
        detalle_venta.total = precio_total_calculado
        detalle_venta.save()

        return super().form_valid(form)