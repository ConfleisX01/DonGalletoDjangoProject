import pandas as pd
from django.db.models import F, Sum
from django.shortcuts import render
from .models import Venta, VentaDetalle
from django.utils.timezone import now
import plotly.express as px
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
from django.contrib.auth.mixins import LoginRequiredMixin

class VerListaPedidosView(LoginRequiredMixin, ListView):
    model = CarritoCompras
    template_name = 'lista_pedidos_cliente.html'
    context_object_name = 'pedidos'

    def get_queryset(self):
        return CarritoCompras.objects.filter(
            usuario=self.request.user,
            detalles__venta__estatus=True
        ).distinct()

class ListaProductosView(LoginRequiredMixin, ListView):
    model = InventarioProducto
    template_name = 'lista_productos.html'
    context_object_name = 'productos'

class DetallesProductoView(LoginRequiredMixin, FormView): #Literalmente agregar el producto al carrito (no se que estaba pensando al nombrar esta vista :/)
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
        carrito = CarritoCompras.objects.filter(usuario=self.request.user, estatus=False).first()

        if not carrito:
            carrito = CarritoCompras.objects.create(usuario=self.request.user)

        if carrito.estatus:
                form.add_error(None, "Este carrito está cerrado. No puedes agregar más productos.")
                return self.form_invalid(form)
        
        detalle_venta = form.save(commit=False)
        detalle_venta.carrito = carrito

        inventario = InventarioProducto.objects.get(galleta=detalle_venta.receta)
        tipo_compra = detalle_venta.tipo_unidad
        cantidad_galleta = detalle_venta.cantidad
        precio_galleta = inventario.galleta.precio_galleta
        peso_galleta = inventario.galleta.peso_individual

        precio_total_calculado = calcularPrecioGalleta(tipo_compra, cantidad_galleta, precio_galleta, peso_galleta)

        if not precio_total_calculado:
            form.add_error(None, "No se pudo calcular el precio correctamente.")
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
        extra=num_galletas, 
        can_delete=True
    )

class VentaCreateView(FormView):
    template_name = "crear_venta.html"
    form_class = VentaForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtener recetas disponibles
        recetas = Receta.objects.all()
        num_galletas = recetas.count()
        messages.info(self.request, f"Se están generando {num_galletas} formularios para las recetas disponibles.")
        
        # Crear formset
        VentaDetalleFormSet = get_venta_detalle_formset(num_galletas)

        if self.request.POST:
            context["formset"] = VentaDetalleFormSet(self.request.POST)
        else:
            initial_data = [{"receta": receta} for receta in recetas] if num_galletas > 0 else []
            context["formset"] = VentaDetalleFormSet(queryset=VentaDetalle.objects.none(), initial=initial_data)

        # Combinar formularios con recetas para mostrar en template
        context["forms_and_recipes"] = zip(context["formset"].forms, recetas)

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["formset"]
        errores_stock = []

        with transaction.atomic():
            # Guardar la venta principal
            venta = form.save(commit=False)
            venta.estatus = '0'  # Establecer estatus como 'hecho'
            venta.save()

            if formset.is_valid():
                for detalle_form in formset:
                    detalle_data = detalle_form.cleaned_data
                    
                    # Saltar formularios vacíos o sin cantidad
                    if not detalle_data.get("receta") or not detalle_data.get("cantidad") or detalle_data["cantidad"] <= 0:
                        continue

                    # Verificar inventario antes de procesar
                    try:
                        inventario = InventarioProducto.objects.get(galleta=detalle_data["receta"])
                        if inventario.cantidad < detalle_data["cantidad"]:
                            errores_stock.append(f"Stock insuficiente para {detalle_data['receta'].nombre}.")
                            continue
                    except InventarioProducto.DoesNotExist:
                        errores_stock.append(f"No hay inventario registrado para {detalle_data['receta'].nombre}.")
                        continue

                    # Crear detalle de venta
                    detalle = VentaDetalle(
                        venta=venta,
                        receta=detalle_data["receta"],
                        cantidad=detalle_data["cantidad"],
                        tipo_unidad=detalle_data.get("tipo_unidad", "ud"),
                        # Calcula el total según tu lógica de negocio
                        total=0  # Aquí deberías calcular el total basado en precio y cantidad
                    )
                    detalle.save()

                    # Actualizar inventario
                    inventario.disminuir_cantidad(detalle.cantidad)
                    inventario.save()

            # Manejar errores de stock después del procesamiento
            if errores_stock:
                for error in errores_stock:
                    messages.error(self.request, error)
                # Aún así redirigimos porque algunos productos pudieron haberse vendido
                return redirect("/corteVenta")

            messages.success(self.request, "Venta registrada con éxito.")
            return redirect("/ventas/corteVenta/")

        # Si llegamos aquí, hubo un error en el formset
        return self.form_invalid(form)
    
def dashboard(request):
    # Obtener todas las ventas sin filtrar por fecha
    ventas_query = Venta.objects.all()
    

    # Agrupar ventas por fecha y calcular el total vendido por día
    ventas_diarias = (
        ventas_query
        .values('fecha')  # Agrupación por fecha
        .annotate(total_vendido=Sum(F('VentaDetalle__cantidad') * F('VentaDetalle__precio_unitario')))  # Sumar totales
        .order_by('fecha')  # Ordenar por fecha
    )
    
    print(ventas_diarias)
    fecha_hoy = now().date()
    print(fecha_hoy)
    
    total_hoy = ventas_diarias.filter(fecha__date='2025-03-27').aggregate(total=Sum('total_vendido'))['total'] or 0
    num_pedidos = ventas_query.filter(fecha__date='2025-03-27').count()

    # Obtener la receta más pedida
    receta_mas_pedida = (
        VentaDetalle.objects
        .filter(id_venta__in=ventas_query)
        .values('id_receta__nombre')
        .annotate(total_cantidad=Sum('cantidad'))
        .order_by('-total_cantidad')
        .first()
    )
    receta_mas_pedida = receta_mas_pedida['id_receta__nombre'] if receta_mas_pedida else "No hay datos"

    objetivo_ventas = 100
    progreso_ventas = (total_hoy / objetivo_ventas) * 100 if objetivo_ventas > 0 else 0

    # Extraer fechas y totales para la gráfica
    fechas = [venta['fecha'] for venta in ventas_diarias]
    totales = [venta['total_vendido'] for venta in ventas_diarias]

    df = pd.DataFrame({'Fecha': fechas, 'Total Vendido': totales})

    # Crear la gráfica con una sola línea que represente los totales por día
    fig = px.line(df, x='Fecha', y='Total Vendido', labels={'x': 'Fecha', 'y': 'Total Vendido'}, title='Ventas Diarias')
    graph_html = fig.to_html(full_html=False)
    
    print(total_hoy)
    print(num_pedidos)
    print(receta_mas_pedida)
    print(progreso_ventas)


    return render(request, 'dashboard.html', {
        'graph_html': graph_html,
        'total_hoy': total_hoy,
        'num_pedidos': num_pedidos,
        'receta_mas_pedida': receta_mas_pedida,
        'objetivo_ventas': objetivo_ventas,
        'progreso_ventas': progreso_ventas
    }) 
    
    
def dashboard_view(request):
    return render(request, 'dashboardProductos.html')
