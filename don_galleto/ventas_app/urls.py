from django.urls import path
from .views import dashboard
from django.urls import path, include
from ventas_app.views import ListaProductosView, DetallesProductoView,VentaCreateView,VerListaPedidosView

urlpatterns = [
    path('lista_productos/', ListaProductosView.as_view(), name='lista_productos'),
    path('detalle_producto/<int:id>', DetallesProductoView.as_view(), name='detalle_producto'),
    path('corteVenta/', VentaCreateView.as_view(), name='corteVenta'),
    path('lista_pedidos_cliente/', VerListaPedidosView.as_view(), name='lista_pedidos_cliente'),
    path('dashboardProductos/', dashboard, name='dashboardProductos'),
]