from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class ListaSolicitudesProduccion(TemplateView):
    template_name = 'lista_solicitud_produccion.html'
