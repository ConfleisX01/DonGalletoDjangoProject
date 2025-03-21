from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from clientes.views import clientesList, clientesRegistrarView, ClienteEditarView

urlpatterns = [
    path('clientes_crud/', clientesList.as_view(), name='clientes_crud'),
    path('crear_cliente/', clientesRegistrarView.as_view(), name='crear_cliente'),
    path('editar_cliente/<int:id>', ClienteEditarView.as_view(), name='editar_cliente'),
]