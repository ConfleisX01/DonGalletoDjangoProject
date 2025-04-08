from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from inventarios.views import inventarioProductoView, inventrioMateriaView, RegistrarMermaView, ListaMermaView, ListaMermaView

urlpatterns = [
    path('productos/', inventarioProductoView.as_view(), name='inventario_productos'),    
    path('materia_prima/', inventrioMateriaView.as_view(), name='inventario_materia'), 
    path('lote/<int:lote_id>/merma/', RegistrarMermaView.as_view(), name='registrar_merma'),
    path('lista_mermas/', ListaMermaView.as_view(), name='lista_mermas'),
]