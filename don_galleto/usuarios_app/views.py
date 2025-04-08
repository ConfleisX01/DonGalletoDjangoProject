from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from clientes.models import Cliente
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import PermissionRequiredMixin
from usuarios_app.forms import UsuarioForm, EditarUsuarioForm
from django.contrib.auth.models import Group
from django.urls import reverse_lazy
from .models import Usuario
from django.contrib.auth.mixins import LoginRequiredMixin


class listaUsuariosAdmin(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'lista_usuarios.html'
    permission_required = 'usuarios_app.admin_permissions'
    
    
    def handle_no_permission(self):
        return super().has_permission() and self.request.user.is_active
    
    def get_context_data(self):
        users = Usuario.objects.filter(user_type='user')
        print(users)
        clientes = Cliente.objects.filter(user_type='cliente')
        admin = Usuario.objects.filter(user_type='admin')         
        return {'usuarios': users,
                'admins': admin,
                'clientes': clientes,}

class CrearUsuario(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    template_name = "crear_usuarios.html"
    form_class = UsuarioForm
    success_url = reverse_lazy("lista_usuarios")
    permission_required = 'usuarios_app.admin_permissions'
    
    def handle_no_permission(self):
        return super().has_permission() and self.request.user.is_active

    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

class editarUsuario(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    template_name = "editar_usuarios.html"
    form_class = EditarUsuarioForm
    success_url = reverse_lazy("lista_usuarios")
    permission_required = 'usuarios_app.admin_permissions'
    
    def handle_no_permission(self):
        return super().has_permission() and self.request.user.is_active
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user_id = self.kwargs.get('id')
        user = get_object_or_404(User, id=user_id)
        usuario = get_object_or_404(Usuario, user=user)
        kwargs['instance'] = user 
        kwargs['initial'] = {'telefono': usuario.telefono}
        return kwargs
    
    def form_valid(self, form):
        
        user = form.save()
        usuario = Usuario.objects.get(user=user)
        usuario.telefono = form.cleaned_data["telefono"]
        usuario.user_type = form.cleaned_data["rol"]
        usuario.save() 
        return super().form_valid(form)
