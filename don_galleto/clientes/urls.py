from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from clientes.views import ClientesList, ClientesRegistrarView, ClienteEditarView, ClienteEliminarView, ClienteActivarView

urlpatterns = [
    path('clientes_crud/', ClientesList.as_view(), name='clientes_crud'),
    path('crear_cliente/', ClientesRegistrarView.as_view(), name='crear_cliente'),
    path('editar_cliente/<int:id>', ClienteEditarView.as_view(), name='editar_cliente'),
    path('eliminar_cliente/<int:id>', ClienteEliminarView.as_view(), name='eliminar_cliente'),
    path('activar_cliente/<int:id>', ClienteActivarView.as_view(), name='activar_cliente'),
]