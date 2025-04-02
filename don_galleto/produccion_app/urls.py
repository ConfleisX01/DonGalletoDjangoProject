# urls.py en produccion_app
from django.urls import path
from produccion_app.views import ListaSolicitudesProduccionView

urlpatterns = [
    path('lista_solicitudes/', ListaSolicitudesProduccionView.as_view(), name='lista_solicitudes'),
]
