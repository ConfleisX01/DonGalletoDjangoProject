# urls.py en produccion_app
from django.urls import path
from produccion_app.views import ListaSolicitudesProduccionView, CrearProductoView, EditarProductoView, CrearSolicitudProduccionView

urlpatterns = [
    path('lista_solicitudes/', ListaSolicitudesProduccionView.as_view(), name='lista_solicitudes'),
    path('crear_producto/', CrearProductoView.as_view(), name='crear_producto'),
    path('editar_producto/<int:id>/', EditarProductoView.as_view(), name='editar_producto'),
    path('crear_solicitud_produccion/', CrearSolicitudProduccionView.as_view(), name='crear_solicitud_produccion'),
]
