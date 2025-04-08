from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateView
from django.views.generic.base import View
from django.views.generic import FormView
from django.urls import reverse_lazy
from inventarios.models import InventarioProducto, InventarioMaterial
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from produccion_app.models import LoteGalletas
from Recetas_app.models import IngredienteReceta
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

        errores = []

        # Verificar que hay suficiente inventario
        for ingrediente in ingredientes:
            total_necesario = ingrediente.cantidad_necesaria * lote.cantidad_lotes
            inventario = InventarioMaterial.objects.get(insumo=ingrediente.insumo)

            if inventario.cantidad < total_necesario:
                errores.append(f"No hay suficiente {inventario.insumo.nombre} en inventario.")

        if errores:
            for error in errores:
                #
                return redirect('inventario_materia')

        # Descontar inventario
        for ingrediente in ingredientes:
            total_necesario = ingrediente.cantidad_necesaria * lote.cantidad_lotes
            inventario = InventarioMaterial.objects.get(insumo=ingrediente.insumo)
            inventario.cantidad -= total_necesario
            inventario.save()

        # Registrar la merma (¡esto faltaba!)
        Merma.objects.create(
            lote=lote,
            cantidad=sum(ingrediente.cantidad_necesaria * lote.cantidad_lotes for ingrediente in ingredientes),
            justificacion=justificacion
        )

        #
        return redirect('inventario_materia')

class inventarioProductoView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
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