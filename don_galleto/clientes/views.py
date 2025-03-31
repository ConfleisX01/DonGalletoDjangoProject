from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.views.generic.base import View
from django.views.generic import FormView
from django.urls import reverse_lazy
from . import forms
from clientes.models import Cliente
from django.contrib.auth.models import User
from ventas_app.models import CarritoCompras
from ventas_app.models import Venta

class ConfirmarCarritoView(FormView):
    template_name = 'confirmar_pedido.html'
    form_class = forms.ConfirmarCarritoForm
    success_url = reverse_lazy('lista_productos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        venta_id = self.kwargs['venta_id'] 
        venta = get_object_or_404(Venta, id=venta_id)
        context['venta'] = venta
        return context

    def form_valid(self, form):
        venta_id = self.kwargs['venta_id']
        venta = get_object_or_404(Venta, id=venta_id)

        venta.fecha_recoleccion = form.cleaned_data['fecha_recoleccion']

        venta.confirmar_pedido()

        venta.save()

        return super().form_valid(form)

class ListaCarritoComprasView(TemplateView):
    template_name = 'lista_carrito_compras.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        carrito = CarritoCompras.objects.filter(usuario=self.request.user).first()

        if carrito:
            context['carrito'] = carrito
            detalles = carrito.detalles.all()

            if detalles.exists():
                context['detalles'] = detalles
                context['numero_venta'] = detalles.first().venta.id
                context['numero_productos'] = detalles.count()
            else:
                context['detalles'] = []
        else:
            context['carrito'] = None
            context['detalles'] = []

        return context

class ClientesList(TemplateView):
    template_name = 'dashboard_clientes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lista = Cliente.objects.filter(user_type='cliente')
        context['lista']=lista
        return context

class ClientesRegistrarView(FormView):
    template_name = 'crear_cliente.html'
    form_class = forms.ClienteCrearForm
    success_url = reverse_lazy('clientes_crud')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
class ClienteEditarView(FormView):
    template_name = 'editar_cliente.html'
    form_class = forms.ClienteEditarForm
    success_url = reverse_lazy('clientes_crud')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        id = self.kwargs.get('id')
        usuario = get_object_or_404(User, id=id)
        kwargs['instance'] = usuario
        return kwargs
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
class ClienteEliminarView(View):
    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=self.kwargs['id'])

        user.is_active = False
        user.save()
        
        return redirect('clientes_crud')

class ClienteActivarView(View):
    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=self.kwargs['id'])

        user.is_active = True
        user.save()
        
        return redirect('clientes_crud')