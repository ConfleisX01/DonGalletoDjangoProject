# urls.py en produccion_app
from django.urls import path
from produccion_app.views import CrearProduccionView, ProduccionActivaView, EditarProduccionView

urlpatterns = [
    path('produccion_activa/', ProduccionActivaView.as_view(), name='produccion_activa'),
    path('crear_produccion/', CrearProduccionView.as_view(), name='crear_produccion'),
    path('editar_produccion/<int:id>/', EditarProduccionView.as_view(), name='editar_produccion'),
]
