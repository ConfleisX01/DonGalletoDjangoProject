from django.urls import path, include
from ventas_app.views import ListaProductosView

urlpatterns = [
    path('lista_productos/', ListaProductosView.as_view(), name='lista_productos')
]