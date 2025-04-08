from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateView
from django.views.generic.base import View
from django.views.generic import FormView
from django.urls import reverse_lazy
from inventarios.models import InventarioProducto, InventarioMaterial
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from produccion_app.models import LoteGalletas
from Recetas_app.models import IngredienteReceta
from django.contrib import messages
from django.db import transaction

from django.views.generic import ListView
from .models import Merma


class RegistrarMermaView(LoginRequiredMixin, PermissionRequiredMixin,View):
    permission_required ='usuarios_app.user_permissions'
    template_name = 'merma_formulario.html'

    def get(self, request, lote_id):
        lote = get_object_or_404(LoteGalletas, id=lote_id)
        receta = lote.galleta
        ingredientes = IngredienteReceta.objects.filter(receta=receta)

        return render(request, self.template_name, {
            'lote': lote,
            'ingredientes': ingredientes
        })

    def post(self, request, lote_id):
        lote = get_object_or_404(LoteGalletas, id=lote_id)
        receta = lote.galleta
        ingredientes = IngredienteReceta.objects.filter(receta=receta)
        justificacion = request.POST.get("justificacion")

        if not justificacion:
            messages.error(request, "Debes ingresar una justificación para la merma.")
            return render(request, self.template_name, {
                'lote': lote,
                'ingredientes': ingredientes
            })

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
                    f"No existe inventario registrado para {ingrediente.insumo.nombre_insumo}."
                )

        if inventario_insuficiente:
            for error in mensajes_error:
                messages.error(request, error)
            return render(request, self.template_name, {
                'lote': lote,
                'ingredientes': ingredientes
            })

        try:
            with transaction.atomic():
                for ingrediente in ingredientes:
                    total_necesario = ingrediente.cantidad_necesaria * lote.cantidad_lotes
                    inventario = InventarioMaterial.objects.get(insumo=ingrediente.insumo)
                    inventario.cantidad -= total_necesario
                    inventario.save()

                Merma.objects.create(
                    lote=lote,
                    cantidad=lote.cantidad_lotes,
                    justificacion=justificacion
                )

                lote.estado = 'TERMINADO'
                lote.save()

            messages.success(request, "La merma fue registrada exitosamente.")
            return redirect('lotes_produccion')

<<<<<<< HEAD
        except Exception:
            # Error genérico si ocurre algo inesperado
            messages.error(
                request,
                "Ocurrió un error al procesar la merma. Por favor, verifica la información e intenta de nuevo."
            )
            return render(request, self.template_name, {
                'lote': lote,
                'ingredientes': ingredientes
            })

        
class inventarioProductoView(LoginRequiredMixin, TemplateView):
=======
class inventarioProductoView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
>>>>>>> 46339a6db870ecd5a5e43f619051a278544119d9
    template_name = 'inventario_productos.html'
    permission_required ='usuarios_app.user_permissions'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        listaGalletas = InventarioProducto.objects.all()
        context['lista']=listaGalletas
        return context
    
class inventrioMateriaView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'inventario_materia.html'
    permission_required ='usuarios_app.user_permissions'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        listaInsumos = InventarioMaterial.objects.all()
        context['lista']=listaInsumos
        return context
    
class ListaMermaView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required ='usuarios_app.user_permissions'
    model = Merma
    template_name = 'merma_lista.html'
    context_object_name = 'mermas'
    ordering = ['-fecha']