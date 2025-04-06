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

# ver usuarios
class listaUsuariosAdmin(LoginRequiredMixin, TemplateView):
    template_name = 'lista_usuarios.html'
    permission_required = 'usuarios_app.view_user'
    
    def handle_no_permission(self):
        return redirect('home')
    
    def get_context_data(self):
        users = Usuario.objects.filter(user_type='user')
        clientes = Cliente.objects.filter(user_type='cliente')
        admin = Usuario.objects.filter(user_type='admin')            
        return {'usuarios': users,
                'admins': admin,
                'clientes': clientes,}

# crear usuarios
class CrearUsuario(LoginRequiredMixin, FormView):
    template_name = "crear_usuarios.html"
    form_class = UsuarioForm
    success_url = reverse_lazy("lista_usuarios")
    permission_required = 'usuarios_app.add_user'
    
    def handle_no_permission(self):
        return redirect('home')

    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

class editarUsuario(LoginRequiredMixin, FormView):
    template_name = "editar_usuarios.html"
    form_class = EditarUsuarioForm
    success_url = reverse_lazy("lista_usuarios")
    permission_required = 'usuarios_app.change_user'
    
    def handle_no_permission(self):
        return redirect('home')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user_id = self.kwargs.get('id')
        user = get_object_or_404(User, id=user_id)
        # Obtenemos la instancia del usuario
        usuario = get_object_or_404(Usuario, user=user)
        kwargs['instance'] = user  # Solo pasamos la instancia de User
        kwargs['initial'] = {'telefono': usuario.telefono}
        return kwargs
    
    def form_valid(self, form):
        
        user = form.save()
        # Ahora actualizamos la instancia de Usuario con los nuevos datos
        usuario = Usuario.objects.get(user=user)
        usuario.telefono = form.cleaned_data["telefono"]
        usuario.user_type = form.cleaned_data["rol"]
        usuario.save() 
        return super().form_valid(form)
