from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateView
from django.views.generic.base import View
from django.views.generic import FormView
from django.urls import reverse_lazy
from . import forms
from clientes.models import Cliente
from django.contrib.auth.models import User

# Create your views here.
class clientesList(TemplateView):
    template_name = 'dashboard_clientes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lista = Cliente.objects.filter(user_type='cliente')
        context['lista']=lista
        return context

class clientesRegistrarView(FormView):
    template_name = 'crear_cliente.html'
    form_class = forms.ClienteCrearForm
    success_url = reverse_lazy('clientes_crud')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
class ClienteEditarView(FormView):
    template_name = 'editar_cliente.html'
    form_class = forms.ClienteEditarForm
    success_url = reverse_lazy('clientes_crud')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        id = self.kwargs.get('id')
        cliente = get_object_or_404(Cliente, id=id)
        kwargs['instance'] = cliente
        return kwargs
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
class ClienteEliminarView(View):
    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=self.kwargs['id'])

        user.is_active = False
        user.save()
        
        return redirect('clientes_crud')

class ClienteActivarView(View):
    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=self.kwargs['id'])

        user.is_active = True
        user.save()
        
        return redirect('clientes_crud')