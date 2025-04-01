from django.urls import path, include
from ventas_panel_app.views import ListaPedidosView

urlpatterns = [
    path('lista_pedidos/', ListaPedidosView.as_view(), name='lista_pedidos')
]