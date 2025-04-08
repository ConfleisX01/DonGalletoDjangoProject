from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.views.generic.base import View
from django.views.generic import FormView
from django.urls import reverse_lazy
from . import forms
from materia_prima.models import MateriaPrima
from inventarios.models import InventarioMaterial
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

# Create your views here.
class ComprarInsumoView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    template_name = 'compra_insumo.html'
    form_class = forms.ComprarInsumoForm
    success_url = reverse_lazy('inventario_materia')
    permission_required = 'usuarios_app.user_permissions'

    def form_valid(self, form):
        lote = form.save()
        inventraio = InventarioMaterial.objects.get(insumo=lote.insumo)
        inventraio.agregar_cantidad(lote.cantidad)
        inventraio.save()
        return super().form_valid(form)

class ListaMateriaPrimaView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'lista_materia_prima.html'
    permission_required = 'usuarios_app.admin_permissions'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lista = MateriaPrima.objects.all()
        context['lista']=lista
        return context
    
class CrearMateriaPrimaView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    template_name = 'crear_materia_prima.html'
    form_class = forms.CrearMateriaPrimaForm
    success_url = reverse_lazy('lista_materia_prima')
    permission_required = 'usuarios_app.admin_permissions'

    def form_valid(self, form):
        materia_prima = form.save()
        InventarioMaterial.objects.create(insumo=materia_prima, cantidad=0)
        return super().form_valid(form)
    
class EditarMateriaPrima(LoginRequiredMixin, PermissionRequiredMixin,FormView):
    template_name = 'editar_materia_prima.html'
    form_class = forms.EditarMateriaPrimaForm
    success_url = reverse_lazy('lista_materia_prima')
    permission_required = 'usuarios_app.admin_permissions'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        id = self.kwargs.get('id')
        materiaPrima = get_object_or_404(MateriaPrima, id=id)
        kwargs['instance']=materiaPrima
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)