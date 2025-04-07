import pandas as pd
from django.utils.timezone import now, localtime
from django.db.models import F, Sum
from django.shortcuts import render, get_object_or_404, redirect
from .models import Venta, VentaDetalle
import plotly.express as px
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView, TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from inventarios.models import InventarioProducto, InventarioMaterial
from materia_prima.models import LoteMateriaPrima
from Recetas_app.models import Receta
from django.contrib import messages
from .forms import VentaForm, VentaDetalleForm, VentaDetalleFormSet
from django.db import transaction
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect, FileResponse, HttpResponse
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.lib.pagesizes import letter
from ventas_app.models import Venta, VentaDetalle, calcularPrecioGalleta, CarritoCompras
from django.utils import timezone
from datetime import datetime
from django.utils.dateparse import parse_date
from . import forms  
class DashboardVentasView(TemplateView):
    template_name = 'dashboard_ventas.html'

    def get_context_data(self, **kwargs):
        # Obtener la fecha de hoy
        fecha_hoy = localtime(now()).date()

        
        # Obtener las fechas desde los parámetros GET
        fecha_inicio = self.request.GET.get('fecha_inicio', fecha_hoy)
        fecha_fin = self.request.GET.get('fecha_fin', fecha_hoy)

        # Si las fechas son cadenas de texto, las convertimos en objetos datetime.date
        if isinstance(fecha_inicio, str):
            fecha_inicio = parse_date(fecha_inicio) or fecha_hoy
        if isinstance(fecha_fin, str):
            fecha_fin = parse_date(fecha_fin) or fecha_hoy
        
        # Calcular el inicio y fin del rango de fechas
        inicio_dia = datetime.combine(fecha_inicio, datetime.min.time())
        fin_dia = datetime.combine(fecha_fin, datetime.max.time())
        inventarios = InventarioMaterial.objects.annotate(
            costo_total=Sum(
                F('insumo__lotes__costo_uniario') * F('cantidad')
            )
        )
        
        # Sumar todos los costos totales de los inventarios
        total_costo_inventario = inventarios.aggregate(total_costo=Sum('costo_total'))['total_costo'] or DetallesProductoView
            
        # Ventas diarias filtradas por el rango de fechas
        ventas_diarias = (
            VentaDetalle.objects
            .filter(venta__fecha_venta__range=[inicio_dia, fin_dia])
            .values('venta__fecha_venta')
            .annotate(total_vendido=Sum(F('total')))
            .order_by('venta__fecha_venta')
        )
        
        # Recetas agrupadas filtradas por el rango de fechas
        recetas_agrupadas = (
            VentaDetalle.objects
            .filter(venta__fecha_venta__range=[inicio_dia, fin_dia])
            .values('receta__nombre')
            .annotate(total_vendidas=Count('id'))
            .order_by('-total_vendidas')
        )

        # Total vendido en el rango de fechas
        total_vendido = sum(
            venta['total_vendido'] or 0 for venta in ventas_diarias
        )

        # Número de pedidos realizados en el rango de fechas
        num_pedidos = (
            Venta.objects
            .filter(estatus=True, fecha_venta__range=[inicio_dia, fin_dia])
            .count()
        )
        
        # Consulta para calcular el costo de los ingredientes por receta
        inventarios_productos = InventarioProducto.objects.annotate(
            costo_produccion=Sum(
                (F('galleta__ingredientes__cantidad_necesaria') / 1000) * F('galleta__ingredientes__insumo__lotes__costo_uniario'),
                output_field=DecimalField(decimal_places=2)
            )
        ).annotate(
            ganancia_total=F('galleta__precio_galleta') * F('cantidad') - F('costo_produccion')
        )

        # Ahora obtenemos la ganancia máxima total sumando las ganancias individuales
        ganancia_maxima_total = inventarios_productos.aggregate(
            total_ganancia_maxima=Sum('ganancia_total')
        )

        print(ganancia_maxima_total)
        
        # Receta más pedida en el rango de fechas
        receta_mas_pedida = (
            VentaDetalle.objects
            .filter(venta__fecha_venta__range=[inicio_dia, fin_dia])
            .values('receta__nombre')
            .annotate(total_cantidad=Sum('cantidad'))
            .order_by('-total_cantidad')
            .first()
        )
        receta_mas_pedida = receta_mas_pedida['receta__nombre'] if receta_mas_pedida else "No hay datos"

        objetivo_ventas = ganancia_maxima_total['total_ganancia_maxima']
        # Progreso de ventas
        progreso_ventas = (total_vendido / objetivo_ventas) * 100 if objetivo_ventas > 0 else 0

        # Datos para los gráficos
        fechas = [venta['venta__fecha_venta'] for venta in ventas_diarias]
        totales = [venta['total_vendido'] for venta in ventas_diarias]
        df_barras = pd.DataFrame({'Fecha': fechas, 'Total Vendido': totales})

        fig_barras = px.bar(df_barras, x='Fecha', y='Total Vendido', title= f'Ventas Diarias: {fecha_inicio} - {fecha_fin}', color='Total Vendido')
        graph_html_barras = fig_barras.to_html(full_html=False)

        df_recetas_agrupadas = pd.DataFrame(list(recetas_agrupadas))
        fig_pie = px.pie(df_recetas_agrupadas, names='receta__nombre', values='total_vendidas', title=f'Recetas vendidas en: {fecha_inicio} - {fecha_fin}')
        graph_html_pie = fig_pie.to_html(full_html=False)

        context = super().get_context_data(**kwargs)
        context.update({
            'graph_html_barras': graph_html_barras,
            'graph_html_pie': graph_html_pie,
            'total_vendido': total_vendido,
            "gagancia_maxima_galletas": ganancia_maxima_total['total_ganancia_maxima'],
            'total_costo_inventario': total_costo_inventario,
            'num_pedidos': num_pedidos,
            'receta_mas_pedida': receta_mas_pedida,
            'objetivo_ventas': objetivo_ventas,
            'progreso_ventas': progreso_ventas,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin
        })

        return context


from django.shortcuts import get_object_or_404
from ventas_app.models import Venta, calcularPrecioGalleta, CarritoCompras
from django.contrib.auth.mixins import LoginRequiredMixin

#Generacion de ticket:
from reportlab.lib import colors    
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from django.http import HttpResponse

def generar_ticket_pdf(venta, detalles_guardados):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    margen_izq = 50
    y = height - 50

    # Encabezado
    p.setFont("Helvetica-Bold", 18)
    p.drawCentredString(width / 2, y, "🍪 Don Galleto - Ticket de Venta")
    y -= 30

    p.setFont("Helvetica", 10)
    p.drawCentredString(width / 2, y, "¡Gracias por tu compra!")
    y -= 30

    # Información general
    p.setFont("Helvetica-Bold", 12)
    p.drawString(margen_izq, y, "Fecha: ")
    p.setFont("Helvetica", 12)
    p.drawString(margen_izq + 50, y, venta.fecha_venta.strftime('%d/%m/%Y %H:%M'))
    y -= 20

    p.setFont("Helvetica-Bold", 12)
    p.drawString(margen_izq, y, "Número de venta:")
    p.setFont("Helvetica", 12)
    p.drawString(margen_izq + 110, y, str(venta.id))
    y -= 30

    # Línea separadora
    p.line(margen_izq, y, width - margen_izq, y)
    y -= 20

    # Encabezados de tabla
    p.setFont("Helvetica-Bold", 12)
    p.drawString(margen_izq, y, "Producto")
    p.drawString(margen_izq + 200, y, "Cantidad")
    p.drawString(margen_izq + 300, y, "Precio Unit.")
    p.drawString(margen_izq + 400, y, "Subtotal")
    y -= 20

    total_galletas = 0
    total_precio = 0

    p.setFont("Helvetica", 11)
    for detalle in detalles_guardados:
        # Obtenemos los datos específicos de cada detalle
        receta = detalle.receta  # Accedemos a la receta relacionada
        nombre = receta.nombre
        cantidad = detalle.cantidad
        precio_unitario = receta.precio_galleta  # Precio exacto de ESA receta
        subtotal = cantidad * precio_unitario

        # Mostramos los datos en columnas alineadas
        p.drawString(margen_izq, y, f"{nombre}")
        p.drawString(margen_izq + 200, y, f"{cantidad}")
        p.drawString(margen_izq + 300, y, f"${precio_unitario:.2f}")
        p.drawString(margen_izq + 400, y, f"${subtotal:.2f}")
        y -= 20

        total_galletas += cantidad
        total_precio += subtotal

        if y < 100:  # Salto de página si nos quedamos sin espacio
            p.showPage()
            y = height - 50
            p.setFont("Helvetica", 11)  # Restablecemos la fuente después del salto

    # Totales
    p.setFont("Helvetica-Bold", 12)
    p.drawString(margen_izq, y, "Total Galletas:")
    p.drawString(margen_izq + 400, y, f"{total_galletas}")
    y -= 20

    p.drawString(margen_izq, y, "Total a Pagar:")
    p.drawString(margen_izq + 400, y, f"${total_precio:.2f}")
    y -= 30

    # Pie de página
    p.setFont("Helvetica-Oblique", 10)
    p.drawCentredString(width / 2, y, "¡Vuelva pronto! 🍪")

    p.showPage()
    p.save()
    buffer.seek(0)

    return HttpResponse(buffer, content_type="application/pdf", headers={
        "Content-Disposition": f'attachment; filename="ticket_venta_{venta.id}.pdf"'
    })

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

class DetallesProductoView(LoginRequiredMixin, FormView):
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

        # Obtener las recetas
        recetas = Receta.objects.all()
        num_galletas = recetas.count()
        messages.info(self.request, f"Se están generando {num_galletas} formularios para las recetas disponibles.")
        
        # Crear formset con el número adecuado de formularios
        VentaDetalleFormSet = get_venta_detalle_formset(num_galletas)

        # Si hay un POST, usar los datos enviados, si no, crear formularios iniciales
        if self.request.POST:
            context["formset"] = VentaDetalleFormSet(self.request.POST)
        else:
            initial_data = [{"receta": receta} for receta in recetas] if num_galletas > 0 else []
            context["formset"] = VentaDetalleFormSet(queryset=VentaDetalle.objects.none(), initial=initial_data)

        # Emparejar los formularios con las recetas
        forms_and_recipes = zip(context["formset"].forms, recetas)
        context["forms_and_recipes"] = forms_and_recipes

        print(f"Formularios generados: {len(context['formset'].forms)}")

        return context
    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["formset"]
        errores_stock = []

        with transaction.atomic():
            venta = form.save(commit=False)
            venta.save()

            if formset.is_valid():
                detalles_guardados = []
                for detalle_form in formset:
                    if not detalle_form.cleaned_data.get("receta") or not detalle_form.cleaned_data.get("cantidad"):
                        continue

                    detalle = detalle_form.save(commit=False)
                    detalle.venta = venta

                    try:
                        inventario = InventarioProducto.objects.get(galleta=detalle.receta)
                        if inventario.cantidad >= detalle.cantidad:
                            inventario.disminuir_cantidad(detalle.cantidad)
                            detalle.save()
                            detalles_guardados.append(detalle)
                        else:
                            errores_stock.append(f"Stock insuficiente para {detalle.receta.nombre}.")
                    except InventarioProducto.DoesNotExist:
                        errores_stock.append(f"No hay inventario registrado para {detalle.receta.nombre}.")

                if errores_stock:
                    for error in errores_stock:
                        messages.error(self.request, error)
                    return redirect("/corteVenta")

                if self.request.POST.get("generar_pdf") == "true":
                    return generar_ticket_pdf(venta, detalles_guardados)

                messages.success(self.request, "Venta registrada con éxito.")
                return redirect("/ventas/corteVenta/")

        return self.form_invalid(form)
    
def dashboard_view(request):
    return render(request, 'dashboardProductos.html')

