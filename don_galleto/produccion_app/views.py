from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView

class ListaSolicitudesProduccionView(TemplateView):
    template_name = 'lista_solicitud_produccion.html'
