# urls.py en produccion_app
from django.urls import path
from produccion_app.views import ListaSolicitudesProduccionView, CrearSolicitudProduccionView, CreacionProduccionGalletasView

urlpatterns = [
    path('lista_solicitudes/', ListaSolicitudesProduccionView.as_view(), name='lista_solicitudes'),
    path('agregar_solicitud/', CrearSolicitudProduccionView.as_view(), name='agregar_solicitud'),
    path('produccion_galletas/', CreacionProduccionGalletasView.as_view(), name='creacion_produccion'),
]
    