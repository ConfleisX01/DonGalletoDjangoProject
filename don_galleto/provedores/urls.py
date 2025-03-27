from django.contrib import admin
from django.urls import path
from provedores.views import lista_provedoresView, CrearProvedorView, EditarProvedorView, eliminar_provedor

urlpatterns = [
    path('Lista-provedores/', lista_provedoresView.as_view(), name="lista_provedores"),
    path('Crear-provedor/', CrearProvedorView.as_view(), name="crear_provedores"),
    path('Editar-provedor/<int:id>', EditarProvedorView.as_view(), name="editar_provedores"),
    path('Eliminar-provedor/<int:id>', eliminar_provedor, name="eliminar_provedores"),
]