from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, ListView
from produccion_app.models import LoteGalletas, SolicitudProduccion
from . import forms
from django.contrib import messages
from django.utils.timezone import now
from datetime import timedelta
from inventarios.models import  InventarioProducto, InventarioMaterial
from Recetas_app.models import IngredienteReceta
from django.db import transaction

class ListaLotesProduccionView(ListView):
    model = LoteGalletas
    template_name = 'lotes_Produccion.html'
    context_object_name = 'solicitudes_lote'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # excluyo los lotes que ya tan terminados
        context['solicitudes_lote'] = LoteGalletas.objects.exclude(estado='TERMINADO')
        return context

class ListaSolicitudesProduccionView(ListView):
    model = SolicitudProduccion
    template_name = 'produccion_activa.html'
    context_object_name = 'solicitudes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['solicitudes_abiertas'] = SolicitudProduccion.objects.filter(estado='PENDIENTE')
        context['solicitudes_lote'] = LoteGalletas.objects.all()
        return context
    
def aprobar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudProduccion, id=solicitud_id)
    
    if solicitud.estado == 'PENDIENTE':
        # Crear un lote nuevo y asociarlo a la solicitud
        lote = LoteGalletas.objects.create(
            galleta=solicitud.galleta,
            fecha_produccion=now().date(),
            fecha_caducidad=now().date() + timedelta(days=15),  # 15 días de caducidad
            estado='CREADO'
        )
        solicitud.lote_generado = lote
        solicitud.estado = 'APROBADA'
        solicitud.save()

    return redirect('lotes_produccion')


def rechazar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudProduccion, id=solicitud_id)

    if solicitud.estado == 'PENDIENTE':
        solicitud.estado = 'RECHAZADA'
        solicitud.save()
    return redirect('lotes_produccion')


def actualizar_estado(request, lote_id):
    lote = get_object_or_404(LoteGalletas, id=lote_id)

    if request.method == "POST":
        nuevo_estado = request.POST.get("estado")
        lote.estado = nuevo_estado  # Se actualiza el estado según la selección del usuario

        # Validación de insumos si pasa a "PREPARANDO"
        if lote.estado in ['PREPARANDO', 'COCINANDO', 'TERMINADO']:
            receta = lote.galleta
            ingredientes = IngredienteReceta.objects.filter(receta=receta)

            inventario_insuficiente = False
            mensajes_error = []

            for ingrediente in ingredientes:
                total_necesario = ingrediente.cantidad_necesaria * lote.cantidad_lotes
                try:
                    inventario = InventarioMaterial.objects.get(insumo=ingrediente.insumo)
                    if inventario.cantidad < total_necesario:
                        inventario_insuficiente = True
                        mensajes_error.append(
                            f"No hay suficiente {ingrediente.insumo.nombre_insumo}. "
                            f"Disponible: {inventario.cantidad}, Necesario: {total_necesario}"
                        )
                except InventarioMaterial.DoesNotExist:
                    inventario_insuficiente = True
                    mensajes_error.append(
                        f"No existe inventario para {ingrediente.insumo.nombre_insumo}"
                    )

            if inventario_insuficiente:
                return render(request, 'lotes_error.html', {
                    'lote': lote,
                    'errores': mensajes_error
                })

        # Si pasa validación, intentamos guardar cambios
        try:
            with transaction.atomic():
                lote.save()

                if lote.estado == 'TERMINADO':
                    receta = lote.galleta
                    ingredientes = IngredienteReceta.objects.filter(receta=receta)

                    for ingrediente in ingredientes:
                        total_necesario = ingrediente.cantidad_necesaria * lote.cantidad_lotes
                        inventario = InventarioMaterial.objects.get(insumo=ingrediente.insumo)
                        inventario.disminuir_cantidad(total_necesario)


                    inventario_producto = InventarioProducto.objects.get(galleta=lote.galleta)
                    if inventario_producto:
                        inventario_producto.agregar_cantidad(lote.galleta.cantidad_galletas_producidas)
                        
                    else:
                        print("Error al agregar las cantidades al inventario de productos")

            messages.success(request, 'Estado actualizado correctamente.')
            return redirect('lotes_produccion')

        except Exception:
            # Mensaje amigable si ocurre un error
            return render(request, 'lotes_error.html', {
                'lote': lote,
                'errores': [
                    "No se pudo actualizar el estado del lote. "
                    "Revisa que los datos sean válidos y que haya suficiente inventario disponible."
                ]
            })

    return redirect('lotes_produccion')


class CrearSolicitudProduccionView(FormView): ## esta sirve para crear la solicitud para luego pedir ser aceptada
    template_name = 'agregar_solicitud_produccion.html'
    form_class = forms.AgregarSolicitudForm
    success_url = reverse_lazy('lista_solicitudes')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
class CreacionProduccionGalletasView(TemplateView): ##solo para para mostrarla en la zona de
    template_name = 'produccion_activa.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['solicitudes_abiertas'] = SolicitudProduccion.objects.filter(estado='PENDIENTE')
        return context