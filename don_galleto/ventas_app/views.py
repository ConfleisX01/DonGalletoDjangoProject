import pandas as pd
from django.db.models import F, Sum, Count
from django.shortcuts import get_object_or_404
from django.utils.timezone import now, localtime
import plotly.express as px
from datetime import datetime, timedelta
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView, TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from inventarios.models import InventarioProducto
from Recetas_app.models import Receta
from . import forms
from ventas_app.models import Venta, VentaDetalle, calcularPrecioGalleta, CarritoCompras

from django.views.generic import TemplateView
from django.db.models import Sum, F, Count
from datetime import datetime, time
from django.utils.timezone import localtime
from .models import Venta, VentaDetalle
import pandas as pd
import plotly.express as px

class DashboardVentasView(TemplateView):
    template_name = 'dashboard_ventas.html'

    def get_context_data(self, **kwargs):
        # Obtener la fecha de hoy
        fecha_hoy = localtime(now()).date()
        inicio_dia = datetime.combine(fecha_hoy, datetime.min.time())
        fin_dia  = datetime.combine(fecha_hoy, datetime.max.time())
        objetivo_ventas = 1000
        
        # Ventas diarias
        ventas_diarias = (
            VentaDetalle.objects
            .values('venta__fecha_venta')
            .annotate(total_vendido=Sum(F('cantidad') * F('total')))
            .order_by('venta__fecha_venta')
        )
        
        
        recetas_agrupadas = (
            VentaDetalle.objects
            .values('receta__nombre')
            .annotate(total_vendidas=Count('id'))
            .order_by('-total_vendidas')
        )

        # Total vendido hoy
        total_hoy = sum(
            venta['total_vendido'] or 0 for venta in ventas_diarias if venta['venta__fecha_venta'].date() == fecha_hoy
        )

        # Número de pedidos con estatus True
        num_pedidos = (
            Venta.objects
            .filter(estatus=True, fecha_venta__range=[inicio_dia, fin_dia])
            .count()
        )

        # Receta más pedida
        receta_mas_pedida = (
            VentaDetalle.objects
            .values('receta__nombre')
            .annotate(total_cantidad=Sum('cantidad'))
            .order_by('-total_cantidad')
            .first()
        )
        receta_mas_pedida = receta_mas_pedida['receta__nombre'] if receta_mas_pedida else "No hay datos"

        # Progreso de ventas
        progreso_ventas = (total_hoy / objetivo_ventas) * 100 if objetivo_ventas > 0 else 0

        # Datos para el gráfico de barras
        fechas = [venta['venta__fecha_venta'] for venta in ventas_diarias]
        totales = [venta['total_vendido'] for venta in ventas_diarias]
        df_barras = pd.DataFrame({'Fecha': fechas, 'Total Vendido': totales})

        # Crear el gráfico de barras con Plotly
        fig_barras = px.bar(df_barras, x='Fecha', y='Total Vendido', title='Ventas Diarias', color='Total Vendido')
        graph_html_barras = fig_barras.to_html(full_html=False)
        
        # Convertir el queryset en un DataFrame de Pandas
        df_recetas_agrupadas = pd.DataFrame(list(recetas_agrupadas))

        # Crear el gráfico de pie con Plotly
        fig_pie = px.pie(df_recetas_agrupadas, names='receta__nombre', values='total_vendidas', title='Recetas Vendidas')
        graph_html_pie = fig_pie.to_html(full_html=False)

        # Pasar todos los datos al contexto
        context = super().get_context_data(**kwargs)
        context.update({
            'graph_html_barras': graph_html_barras,
            'graph_html_pie': graph_html_pie,
            'total_hoy': total_hoy,
            'num_pedidos': num_pedidos,
            'receta_mas_pedida': receta_mas_pedida,
            'objetivo_ventas': objetivo_ventas,
            'progreso_ventas': progreso_ventas
        })

        return context
    
class VerListaPedidosView(ListView):
    model = CarritoCompras
    template_name = 'lista_pedidos_cliente.html'
    context_object_name = 'pedidos'
    def get_queryset(self):
        return CarritoCompras.objects.filter(usuario=self.request.user, detalles__venta__estatus=True).distinct()

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
        receta = get_object_or_404(Receta, id=self.kwargs.get('id'))
        kwargs['initial'] = {'receta': receta}
        return kwargs
    
    def form_valid(self, form):
        carrito, _ = CarritoCompras.objects.get_or_create(usuario=self.request.user)
        venta, _ = Venta.objects.get_or_create(id=carrito.id, defaults={"estatus": False})
        
        if venta.estatus:
            carrito = CarritoCompras.objects.create(usuario=self.request.user)
            venta = Venta.objects.create()
        
        detalle_venta = form.save(commit=False)
        detalle_venta.carrito = carrito
        detalle_venta.venta = venta
        
        inventario = InventarioProducto.objects.get(galleta=detalle_venta.receta)
        precio_total_calculado = calcularPrecioGalleta(detalle_venta.tipo_unidad, detalle_venta.cantidad, inventario.galleta.precio_galleta, inventario.galleta.peso_individual)
        
        if precio_total_calculado is False:
            form.add_error(None, "No se pudo calcular el precio")
            return self.form_invalid(form)
        
        detalle_venta.total = precio_total_calculado
        detalle_venta.save()
        
        return super().form_valid(form)
