from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import PermissionRequiredMixin
from usuarios_app.forms import crearUsuariosForm
from django.contrib.auth.models import Group


# vistas admin

#ver usuers
class listaUsuariosAdmin(TemplateView):
    template_name = 'lista_usuarios.html'
    # permission_required = 'usuarios_app.view_user'
    def handle_no_permission(self):
        return redirect('home')
    def get_context_data(self):
        users = User.objects.all()
        return {'usuarios': users}

# crear usuarios
class crearUsuario(FormView):
    template_name = 'crear_usuarios.html'
    form_class = crearUsuariosForm

    def form_valid(self, form):
        user = form.save()
        grupo, created = Group.objects.get_or_create(name='usuario')
        user.groups.add(grupo)
        user.save()
        return redirect('lista_usuarios')

# editar usuarios
class editarUsuario(FormView):
    model = User
    template_name = 'editar_usuarios.html'
    context_object_name = 'usuarios'


