# urls.py en produccion_app
from django.urls import path
from produccion_app.views import ListaSolicitudesProduccionView, CrearSolicitudProduccionView, CreacionProduccionGalletasView, aprobar_solicitud, ListaLotesProduccionView, rechazar_solicitud, actualizar_estado



urlpatterns = [
    path('lista_solicitudes/', ListaSolicitudesProduccionView.as_view(), name='lista_solicitudes'),
    path('agregar_solicitud/', CrearSolicitudProduccionView.as_view(), name='agregar_solicitud'), ##sirve para mandarme a la solicitud
    path('produccion_galletas/', CreacionProduccionGalletasView.as_view(), name='creacion_produccion'),
    path('lotes_produccion/', ListaLotesProduccionView.as_view(), name='lotes_produccion'),
    path('aprobar_solicitud/<int:solicitud_id>/', aprobar_solicitud, name='aprobar_solicitud'),
    path('rechazar_solicitud/<int:solicitud_id>', rechazar_solicitud, name="rechazar_solicitud"),

    path('actualizar_estado/<int:lote_id>/', actualizar_estado, name='actualizar_estado'),

]