from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.views.generic.edit import FormView

# vistas admin

#ver usuers
class listaUsuariosAdmin(TemplateView):
    model = User
    template_name = 'lista_usuarios.html'
    context_object_name = 'usuarios'

# crear usuarios
class crearUsuario(FormView):
    model = User
    template_name = 'crear_usuarios.html'
    context_object_name = 'usuarios'


# editar usuarios
class editarUsuario(FormView):
    model = User
    template_name = 'editar_usuarios.html'
    context_object_name = 'usuarios'


