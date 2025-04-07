from django.urls import path
from django.urls import path, include
from ventas_app.views import ListaProductosView, DetallesProductoView,VentaCreateView,VerListaPedidosView, dashboard_view,DashboardVentasView

urlpatterns = [
    path('dashvoardventas/',DashboardVentasView.as_view(), name='dashboard_ventas'),
    path('lista_productos/', ListaProductosView.as_view(), name='lista_productos'),
    path('detalle_producto/<int:id>', DetallesProductoView.as_view(), name='detalle_producto'),
    path('corteVenta/', VentaCreateView.as_view(), name='corteVenta'),
    path('lista_pedidos_cliente/', VerListaPedidosView.as_view(), name='lista_pedidos_cliente'),
    path('dashboardProductos/', dashboard_view, name='dashboardProductos'),

]