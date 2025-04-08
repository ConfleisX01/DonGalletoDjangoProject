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
from ventas_app.models import Venta, VentaDetalle
from inventarios.models import InventarioProducto
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

def convertir_unidades(cantidad, tipo_unidad, peso_galleta):
    if tipo_unidad == 'ud':
        return cantidad
    elif tipo_unidad == 'pq':
        return cantidad * 12
    elif tipo_unidad == 'g':
        return cantidad / peso_galleta

class ConfirmarCarritoView(LoginRequiredMixin, FormView):
    template_name = 'confirmar_pedido.html'
    form_class = forms.ConfirmarCarritoForm
    success_url = reverse_lazy('lista_productos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        carrito_id = self.kwargs['carrito_id']
        carrito = get_object_or_404(CarritoCompras, id=carrito_id)
        context['carrito'] = carrito
        return context

    def form_valid(self, form):
        carrito_id = self.kwargs['carrito_id']
        carrito = get_object_or_404(CarritoCompras, id=carrito_id)

        detalles = carrito.detalles.all()

        try:
            for detalle in detalles:
                inventario = get_object_or_404(InventarioProducto, galleta=detalle.receta)
                cantidad_requerida = convertir_unidades(detalle.cantidad, detalle.tipo_unidad, detalle.receta.peso_individual)

                if not inventario.verificar_stock(cantidad_requerida):
                    form.add_error(None, f"No hay suficiente stock para {detalle.receta.nombre}.")
                    return self.form_invalid(form)
                
            # Si paso el desmadre de arriba pues crea la compra.
            venta = Venta.objects.create(estatus='0')
            venta.fecha_recoleccion = form.cleaned_data['fecha_recoleccion']
            venta.confirmar_pedido()

            for detalle in detalles:
                inventario = get_object_or_404(InventarioProducto, galleta=detalle.receta)
                cantidad_requerida = convertir_unidades(detalle.cantidad, detalle.tipo_unidad, detalle.receta.peso_individual)

                inventario.disminuir_cantidad(cantidad_requerida)

                detalle.venta = venta
                detalle.save()

            carrito.estatus = '1'
            carrito.save()
            venta.save()

            return super().form_valid(form)
        except Exception as e:
            print(f"Error al confirmar el pedido: {e}")
            form.add_error(None, "Hubo un error al agregar confirmar el pedido")
            return self.form_invalid(form)

class ListaCarritoComprasView(LoginRequiredMixin, TemplateView):
    template_name = 'lista_carrito_compras.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        carrito = CarritoCompras.objects.filter(usuario=self.request.user, estatus='0').order_by('-id').first()

        if not carrito:
            context['carrito_vacio'] = True
            context['carrito'] = None
        else:
            detalles = carrito.detalles.all()
            
            if detalles.exists():
                context['carrito_vacio'] = False
                context['carrito'] = carrito
                context['detalles'] = detalles
                context['numero_productos'] = detalles.count()
            else:
                context['carrito_vacio'] = True
                context['carrito'] = carrito
                context['detalles'] = []
        return context

class VaciarCarritoView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        carrito = CarritoCompras.objects.filter(usuario=request.user, estatus=False).first()

        if carrito:
            carrito.vaciar_carrito()
            
        return redirect('lista_productos')

class EliminarProductoCarritoView(LoginRequiredMixin, View):
    def get(self, request, detalle_id, *args, **kwargs):
        detalle_venta = get_object_or_404(VentaDetalle, id=detalle_id)

        detalle_venta.delete()

        return redirect('lista_productos')


class ClientesList(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'dashboard_clientes.html'
    permission_required = 'usuarios_app.admin_permissions'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lista = Cliente.objects.filter(user_type='cliente')
        context['lista']=lista
        return context

class ClientesRegistrarView(LoginRequiredMixin, PermissionRequiredMixin,  FormView):
    template_name = 'crear_cliente.html'
    form_class = forms.ClienteCrearForm
    success_url = reverse_lazy('clientes_crud')
    permission_required = 'usuarios_app.admin_permissions'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
class ClienteEditarView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    template_name = 'editar_cliente.html'
    form_class = forms.ClienteEditarForm
    success_url = reverse_lazy('clientes_crud')
    permission_required = 'usuarios_app.admin_permissions'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        id = self.kwargs.get('id')
        usuario = get_object_or_404(Cliente, user_id=id)
        kwargs['instance'] = usuario
        return kwargs
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
class ClienteEliminarView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=self.kwargs['id'])

        user.is_active = False
        user.save()
        
        return redirect('clientes_crud')

class ClienteActivarView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=self.kwargs['id'])

        user.is_active = True
        user.save()
        
        return redirect('clientes_crud')