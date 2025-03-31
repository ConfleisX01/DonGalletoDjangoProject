import pandas as pd
from django.db.models import F, Sum
from django.shortcuts import render
from .models import Venta, VentaDetalle
from django.utils.timezone import now, get_current_timezone
import plotly.express as px



def dashboard(request):
    # Obtener la fecha actual en la zona horaria configurada
    fecha_hoy = localtime(now()).date()  # Obtener solo la fecha sin la hora
    print(f"Fecha de hoy: {fecha_hoy}")
    
    objetivo_ventas = 1000
    
    # Obtener todas las ventas
    ventas_query = Venta.objects.all()

    # Agrupar ventas por fecha y calcular el total vendido por día
    ventas_diarias = (
        ventas_query
        .values('fecha')  # Agrupación por fecha
        .annotate(total_vendido=Sum(F('VentaDetalle__cantidad') * F('VentaDetalle__precio_unitario')))  # Sumar totales
        .order_by('fecha')  # Ordenar por fecha
    )
    # Filtrar las ventas del día actual y sumar los totales
    total_hoy = sum(
        venta['total_vendido'] or 0 for venta in ventas_diarias if venta['fecha'].date() == fecha_hoy
    )
    # Número de pedidos del día actual
    num_pedidos = sum(
        1 for venta in ventas_diarias if venta['fecha'].date() == fecha_hoy
    )
    
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

    progreso_ventas = (total_hoy / objetivo_ventas) * 100 if objetivo_ventas > 0 else 0

    # Extraer fechas y totales para la gráfica de barras
    fechas = [venta['fecha'] for venta in ventas_diarias]
    totales = [venta['total_vendido'] for venta in ventas_diarias]
    df_barras = pd.DataFrame({'Fecha': fechas, 'Total Vendido': totales})

    # Crear la gráfica de barras
    fig_barras = px.bar(df_barras, x='Fecha', y='Total Vendido', labels={'x': 'Fecha', 'y': 'Total Vendido'}, 
                        title='Ventas Diarias', color='Total Vendido', color_continuous_scale='Viridis')
    graph_html_barras = fig_barras.to_html(full_html=False)


    inicio_dia = datetime.combine(fecha_hoy, datetime.min.time())
    fin_dia = datetime.combine(fecha_hoy, datetime.max.time())
    
    recetas_agrupadas = (
        DetalleVenta.objects
        .filter(id_venta__fecha__range=(inicio_dia, fin_dia)) 
        .values('id_receta__nombre')  
        .annotate(total_vendidas=Count('id'))  
        .order_by('-total_vendidas')  
    )
    
    
    fig_pie = px.pie(
    recetas_agrupadas, 
    names='id_receta__nombre',  
    values='total_vendidas',  
    title='Distribución de Recetas Vendidas Hoy',
    color='id_receta__nombre',  
    color_discrete_sequence=px.colors.qualitative.Set1
)

# Personalizar el texto que aparece al pasar el ratón (tooltip)
    fig_pie.update_traces(
        hovertemplate='<b>Receta:</b> %{label}<br><b>Cantidad Vendida:</b> %{value}<extra></extra>'
    )

    # Convertir el gráfico a HTML
    graph_html_pie = fig_pie.to_html(full_html=False)


    
    return render(request, 'dashboard_ventas.html', {
        'graph_html_barras': graph_html_barras,
        'graph_html_pie': graph_html_pie,
        'total_hoy': total_hoy,
        'num_pedidos': num_pedidos,
        'receta_mas_pedida': receta_mas_pedida,
        'objetivo_ventas': objetivo_ventas,
        'progreso_ventas': progreso_ventas
    })
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