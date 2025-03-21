from django.contrib import admin
from django.urls import path, include
from usuarios_app.views import listaUsuariosAdmin,crearUsuario,editarUsuario
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('lista-usuarios/', listaUsuariosAdmin.as_view(), name='lista_usuarios'),
    path('crear-usuarios/', crearUsuario.as_view(), name='creaar_usuarios'),
    path('editar-usuarios/<int:usuario_id>', editarUsuario.as_view(), name='editar_usuarios'),
]
