from django.urls import path, include
from ventas_app.views import ListaProductosView, DetallesProductoView, VerListaPedidosView

urlpatterns = [
    path('lista_productos/', ListaProductosView.as_view(), name='lista_productos'),
    path('detalle_producto/<int:id>', DetallesProductoView.as_view(), name='detalle_producto'),
    path('lista_pedidos_cliente/', VerListaPedidosView.as_view(), name='lista_pedidos_cliente'),
]