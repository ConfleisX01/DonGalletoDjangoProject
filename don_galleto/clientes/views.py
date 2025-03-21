from django.shortcuts import render
from django.views.generic.base import TemplateView

# Create your views here.
def clientesList(request):
    return render(request, 'dashboard_clientes.html')