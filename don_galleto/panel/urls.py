from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from panel.views import panelIndex

urlpatterns = [
    path('', panelIndex, name='panel'),
    path('administracion/', include('clientes.urls')),
    path('inventarios/', include('inventarios.urls')),
]