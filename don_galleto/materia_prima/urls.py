from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from materia_prima.views import ListaMateriaPrimaView, CrearMateriaPrimaView

urlpatterns = [
    path('lista_materia_prima/', ListaMateriaPrimaView.as_view(), name='lista_materia_prima'),
    path('agregar_materia_prima/', CrearMateriaPrimaView.as_view(), name='agregar_materia_prima'),
]