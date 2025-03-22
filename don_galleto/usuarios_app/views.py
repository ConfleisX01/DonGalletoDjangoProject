from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import PermissionRequiredMixin
from usuarios_app.forms import UsuarioForm, EditarUsuarioForm
from django.contrib.auth.models import Group
from django.urls import reverse_lazy


# vistas admin

#ver usuers
class listaUsuariosAdmin(TemplateView):
    template_name = 'lista_usuarios.html'
    #permission_required = 'usuarios_app.view_user'
    def handle_no_permission(self):
        return redirect('home')
    def get_context_data(self):
        users = User.objects.filter(is_staff=False)
        admin = User.objects.filter(is_staff=True)
        return {'usuarios': users,
                'admin': admin}

#crear usuarios
class CrearUsuario(FormView):
    template_name = "crear_usuarios.html"
    form_class = UsuarioForm
    success_url = reverse_lazy("lista_usuarios")
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

# editar usuarios
class editarUsuario(FormView):
    template_name = "editar_usuarios.html"
    form_class = EditarUsuarioForm
    success_url = reverse_lazy("lista_usuarios")
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        id = self.kwargs.get('id')
        usuario = User.objects.get(id=id)
        kwargs['instance'] = usuario
        return kwargs
    
    def form_valid(self, form):
        form.save(self.kwargs.get('id'), user = self.request.user)
        return super().form_valid(form)
