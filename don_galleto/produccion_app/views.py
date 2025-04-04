from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, ListView
from produccion_app.models import LoteGalletas, SolicitudProduccion
from . import forms
from django.utils.timezone import now
from datetime import timedelta
<<<<<<< HEAD
from inventarios.models import  InventarioProducto

=======
from django.http import JsonResponse
from inventarios.models import InventarioProducto
>>>>>>> dbe1769c46235201b08c444271476005dd0056a8

class ListaLotesProduccionView(ListView):
    model = LoteGalletas
    template_name = 'lotes_Produccion.html'
    context_object_name = 'solicitudes_lote'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Excluir los lotes que ya están terminados
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
        lote.estado = nuevo_estado
        
        # Si el lote se marca como 'TERMINADO', podemos hacer más cosas si es necesario
        if lote.estado == 'TERMINADO':
<<<<<<< HEAD
            inventario_producto, creado = InventarioProducto.objects.get_or_create(
                galleta=lote.galleta,
                defaults={'cantidad': 0}
        )
            inventario_producto.cantidad += lote.cantidad  # sumamos lo producido
            inventario_producto.save()

        pass
=======
            print("Entrando a la funcion")
            inventario = InventarioProducto.objects.get(galleta=lote.galleta_id)
            print(inventario)
            if inventario:
                inventario.agregar_cantidad(lote.galleta.cantidad_galletas_producidas)
                print("Se agregaron las galletas al inventario")
            else:
                print(f"Error al agregar las cantidades al inventario")
>>>>>>> dbe1769c46235201b08c444271476005dd0056a8
        
        lote.save()

    return redirect('lotes_produccion')  # Redirige a la lista de lotes de producción


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