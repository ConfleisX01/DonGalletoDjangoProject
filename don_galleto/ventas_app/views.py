import pandas as pd
from django.db.models import F, Sum, Count
from django.shortcuts import get_object_or_404
from django.utils.timezone import now, localtime
import plotly.express as px
from datetime import datetime
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView, TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin,LoginRequiredMixin
from inventarios.models import InventarioProducto
from Recetas_app.models import Receta
from django.contrib import messages
from .forms import VentaForm, VentaDetalleForm
from django.views.generic.edit import FormView
from django.db import transaction
from django.contrib import messages
from .forms import VentaForm
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.db import transaction
from .models import Venta, VentaDetalle
from django.forms import inlineformset_factory
from . import forms
from ventas_app.models import Venta, VentaDetalle, calcularPrecioGalleta, CarritoCompras

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
            .annotate(total_vendido=Sum(F('total')))
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
        return CarritoCompras.objects.filter(usuario=self.request.user, detalles__venta__estatus='1').distinct()

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
        receta = get_object_or_404(Receta, id=self.kwargs.get('id'))
        kwargs['initial'] = {'receta': receta}
        return kwargs
    
    def form_valid(self, form):
        try:
            carrito, created = CarritoCompras.objects.get_or_create(
                usuario=self.request.user,
                estatus='0'
            )

            if carrito:
                detalle_venta = form.save(commit=False)
                detalle_venta.carrito = carrito
                detalle_venta.venta = None

                inventario = InventarioProducto.objects.get(galleta=detalle_venta.receta)

                precio_total_calculado = calcularPrecioGalleta(
                    detalle_venta.tipo_unidad, 
                    detalle_venta.cantidad, 
                    inventario.galleta.precio_galleta, 
                    inventario.galleta.peso_individual
                )
                
                if precio_total_calculado is False:
                    form.add_error(None, "No se pudo calcular el precio")
                    return self.form_invalid(form)
                
                detalle_venta.total = precio_total_calculado
                detalle_venta.save()
            elif created:
                print('Se creo un nuevo carrito')
            else:
                form.add_error(None, "Hubo un error en el producto")
                return self.form_invalid(form)
            
        except Exception as e:
            print(f"Error al manejar el carrito: {e}")
            form.add_error(None, "Hubo un error al agregar el producto al carrito")
            return self.form_invalid(form)
        
        return super().form_valid(form)

def calcularGalletas(cantidad, tipo_compra, peso_galleta):
    if tipo_compra == 'ud':
        return cantidad
    elif tipo_compra == 'gr':
        return peso_galleta / cantidad
    elif tipo_compra == 'pq':
        return cantidad * 12
    else: return False
    

def get_venta_detalle_formset(num_galletas):
    return inlineformset_factory(
        Venta,
        VentaDetalle,
        form=VentaDetalleForm,
        extra=num_galletas, 
        can_delete=True
    )

class VentaCreateView(FormView):
    recetas = Receta.objects.all()
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
    
def dashboard_view(request):
    return render(request, 'dashboardProductos.html')

class ListaVentasView(ListView):
    model = Venta
    template_name = "lista_ventas.html"
    context_object_name = "ventas"

    def get_queryset(self):
        # Filtrar las ventas por el estatus que sea igual a '1'
        ventas = Venta.objects.filter(estatus='1').prefetch_related('detalles_venta').annotate(
            total_venta=Sum('detalles_venta__total')
        ).order_by('-fecha_venta')

        # Calcular el precio unitario y pasarlo al contexto de la plantilla
        for venta in ventas:
            for detalle in venta.detalles_venta.all():
                if detalle.cantidad > 0:
                    detalle.precio_unitario = detalle.total / detalle.cantidad
                else:
                    detalle.precio_unitario = 0
        return ventas

