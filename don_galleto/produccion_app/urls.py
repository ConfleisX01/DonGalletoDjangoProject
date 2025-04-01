from django.urls import path, include
from produccion_app.views import ListaSolicitudesProduccion

urlpatterns = [
    path('lista_solicitudes', ListaSolicitudesProduccion.as_view(), name='lista_solicitudes')
]