from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateView
from django.views.generic.base import View
from django.views.generic import FormView
from django.urls import reverse_lazy

class inventarioProductoView(TemplateView):
    template_name = 'inventario_productos.html'