from django.urls import path
from django.urls import path, include
from ventas_app.views import ListaProductosView, DetallesProductoView,VentaCreateView,VerListaPedidosView, dashboard_view,DashboardVentasView,DashboardPresentacionesView,  ListaVentasView 
from ventas_app.views import VerListaPedidosClientesView, DetallesPedidoClienteView

urlpatterns = [
    path('dashvoardventas/',DashboardVentasView.as_view(), name='dashboard_ventas'),
    path('lista_ventas/', ListaVentasView.as_view(), name='lista_ventas'),
    path('lista_productos/', ListaProductosView.as_view(), name='lista_productos'),
    path('detalle_producto/<int:id>', DetallesProductoView.as_view(), name='detalle_producto'),
    path('corteVenta/', VentaCreateView.as_view(), name='corteVenta'),
    path('lista_pedidos_cliente/', VerListaPedidosClientesView.as_view(), name='lista_pedidos_cliente'),
    path('dashboardProductos/', dashboard_view, name='dashboardProductos'),
    path('dashboardPresentaciones/',DashboardPresentacionesView.as_view(), name='dashboardPresentaciones'),
    path('detalles_pedido/<int:id>', DetallesPedidoClienteView.as_view(), name='detalles_pedido'),
]