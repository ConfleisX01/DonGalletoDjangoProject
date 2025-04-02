from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic import ListView, FormView
from inventarios.models import InventarioProducto
from Recetas_app.models import Receta
from django.contrib import messages
from .forms import VentaForm, VentaDetalleForm
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .forms import VentaForm, VentaDetalleFormSet
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.db import transaction
from .models import Venta, VentaDetalle
from .forms import VentaForm, VentaDetalleFormSet
from django.http import HttpResponseRedirect
from django.forms import inlineformset_factory

from . import forms
from django.shortcuts import get_object_or_404
from ventas_app.models import Venta, calcularPrecioGalleta, CarritoCompras

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

        detalle_venta = form.save(commit=False)
        detalle_venta.carrito = carrito
        detalle_venta.venta = None

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
    
    
    
    
recetas = Receta.objects.all()

def get_venta_detalle_formset(num_galletas):
    return inlineformset_factory(
        Venta,
        VentaDetalle,
        form=VentaDetalleForm,
        extra=num_galletas,  # Se genera un formulario por cada receta disponible
        can_delete=True
    )

class VentaCreateView(FormView):
    template_name = "crear_venta.html"
    form_class = VentaForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Contar cuántas recetas hay en la base de datos
        recetas = Receta.objects.all()
        num_galletas = recetas.count()
        messages.info(self.request, f"Se están generando {num_galletas} formularios para las recetas disponibles.")
        VentaDetalleFormSet = get_venta_detalle_formset(num_galletas)

        if self.request.POST:
            context["formset"] = VentaDetalleFormSet(self.request.POST)
        else:
            # Generar datos iniciales solo si hay recetas
            initial_data = [{"receta": receta} for receta in recetas] if num_galletas > 0 else []
            context["formset"] = VentaDetalleFormSet(queryset=VentaDetalle.objects.none(), initial=initial_data)

        # Combinamos las recetas con los formularios
        forms_and_recipes = zip(context["formset"].forms, recetas)
        context["forms_and_recipes"] = forms_and_recipes

        # Verificar cuántos formularios se generan realmente
        print(f"Formularios generados: {len(context['formset'].forms)}")

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["formset"]
        errores_stock = []  # Lista para errores de stock

        with transaction.atomic():
            venta = form.save(commit=False)
            venta.save()

            if formset.is_valid():
                for detalle_form in formset:
                    if not detalle_form.cleaned_data.get("receta") or not detalle_form.cleaned_data.get("cantidad"):
                        continue  # Ignorar formularios vacíos

                    detalle = detalle_form.save(commit=False)
                    detalle.venta = venta  

                    try:
                        inventario = InventarioProducto.objects.get(galleta=detalle.receta)
                        if inventario.cantidad >= detalle.cantidad:
                            inventario.disminuir_cantidad(detalle.cantidad)
                            detalle.save()
                        else:
                            errores_stock.append(f"Stock insuficiente para {detalle.receta.nombre}.")
                    except InventarioProducto.DoesNotExist:
                        errores_stock.append(f"No hay inventario registrado para {detalle.receta.nombre}.")

                # Si hubo errores de stock, mostrar los mensajes pero seguir con la venta de los demás productos
                if errores_stock:
                    for error in errores_stock:
                        messages.error(self.request, error)
                    return redirect("crear_venta")

                messages.success(self.request, "Venta registrada con éxito.")
                return redirect("crear_venta")

        return self.form_invalid(form)