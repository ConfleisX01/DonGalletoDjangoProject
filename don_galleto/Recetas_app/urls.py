from django.urls import path
from Recetas_app.views import CrearReceta,ListaRecetasView,EditarRecetaView, VerRecetaView, DefinirInsumoView

# AUN FALTA LA PARTE DE LA AUTENTIFICACION
urlpatterns = [
    path('lista_receta/', ListaRecetasView.as_view(), name='lista_receta'), 
    path('crear_receta/', CrearReceta.as_view(), name='crear_receta'), 
    path('editar-receta/<int:pk>/', EditarRecetaView.as_view(), name='editar_receta'),
    path('ver-receta/<int:pk>/', VerRecetaView.as_view(), name='ver_receta'),
    path('definir_insumos/<int:pk>/', DefinirInsumoView.as_view(), name='definir_insumos'),
    
]
