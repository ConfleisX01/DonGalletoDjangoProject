from django.shortcuts import render, get_object_or_404, redirect
from provedores.models import Provedor
from django.views.generic.base import TemplateView
from django.views.generic import FormView
from . import forms
from django.urls import reverse_lazy
from django.contrib import messages

class lista_provedoresView(TemplateView):
    template_name = "lista_provedores.html"
    def get_context_data(self):
        lista = Provedor.objects.all()
        return{
            "lista": lista
        }
    
class CrearProvedorView(FormView):
    template_name = "crear_provedor.html"
    form_class = forms.ProvedorRegistrarForm
    success_url = reverse_lazy('lista_provedores')
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
class EditarProvedorView(FormView):
    template_name = "editar_provedor.html"
    form_class = forms.ProvedorEditarForm
    success_url = reverse_lazy('lista_provedores')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        id = self.kwargs.get('id')
        provedor = get_object_or_404(Provedor, id = id)
        kwargs['instance'] = provedor
        return kwargs
    
    def form_valid(self, form):
        form.save(self.kwargs.get('id'))
        return super().form_valid(form)
    
def eliminar_provedor(request, id):
    proveedor = get_object_or_404(Provedor, id=id)
    proveedor.delete()
    messages.success(request, "Proveedor eliminado correctamente.")
    return redirect('lista_provedores')