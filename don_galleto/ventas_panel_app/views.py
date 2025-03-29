from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import ListView, FormView
from ventas_app.models import CarritoCompras

class ListaPedidosView(TemplateView):
    template_name = 'lista_pedidos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        carritos = CarritoCompras.objects.prefetch_related("detalles").all()

        context["carritos"] = carritos
        context['numero_productos'] = carritos
        print(carritos)
        return context