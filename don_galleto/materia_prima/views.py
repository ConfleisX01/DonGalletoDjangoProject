from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateView
from django.views.generic.base import View
from django.views.generic import FormView
from django.urls import reverse_lazy
from . import forms
from materia_prima.models import MateriaPrima

# Create your views here.
class ListaMateriaPrimaView(TemplateView):
    template_name = 'lista_materia_prima.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lista = MateriaPrima.objects.all()
        context['lista']=lista
        return context
    
class CrearMateriaPrimaView(FormView):
    template_name = 'crear_materia_prima.html'
    form_class = forms.CrearMateriaPrimaForm
    success_url = reverse_lazy('lista_materia_prima')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)