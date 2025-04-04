from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from panel.views import panelIndex

urlpatterns = [
    path('', panelIndex, name='panel'),
    path('administracion/', include([
        path('clientes/', include('clientes.urls')),
        path('usuarios/', include('usuarios_app.urls')),
        path('recetas/', include('Recetas_app.urls')),
        path('materia_prima/', include('materia_prima.urls')),
        path('ventas/', include('ventas_panel_app.urls')),
        path('ventas/', include('ventas_app.urls')),
        path('produccion/', include('produccion_app.urls')),
    ])),
    path('inventarios/', include('inventarios.urls')),
]