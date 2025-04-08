from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from materia_prima.views import ListaMateriaPrimaView, CrearMateriaPrimaView, EditarMateriaPrima, ComprarInsumoView

urlpatterns = [
    path('lista_materia_prima/', ListaMateriaPrimaView.as_view(), name='lista_materia_prima'),
    path('agregar_materia_prima/', CrearMateriaPrimaView.as_view(), name='agregar_materia_prima'),
    path('editar_materia_prima/<int:id>/', EditarMateriaPrima.as_view(), name='editar_materia_prima'),
    path('comprar_insumo/', ComprarInsumoView.as_view(), name="comprar_insumo"),
]