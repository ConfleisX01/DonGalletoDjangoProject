from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView
from .models import Receta
from .forms import RecetaEditarForm
from django.urls import reverse_lazy
from django.views.generic import FormView
from .forms import RecetaRegistrarForm
from .models import Receta, IngredienteReceta
from django.views.generic import DetailView

class CrearReceta(FormView):
    template_name = 'crear_receta.html'
    form_class = RecetaRegistrarForm
    success_url = reverse_lazy('lista_receta')

    def form_valid(self, form):
        # Guardar la receta
        receta = Receta.objects.create(
            nombre=form.cleaned_data["nombre"],
            cantidad_galletas_producidas=form.cleaned_data["cantidad_galletas_producidas"],
            peso_individual=form.cleaned_data["peso_individual"],
        )

        # Asociar ingredientes a la receta
        ingredientes = form.cleaned_data["ingredientes"]
        for insumo in ingredientes:
            IngredienteReceta.objects.create(
                receta=receta,
                insumo=insumo,
                cantidad_necesaria=1  # Puedes personalizar esto si el formulario lo permite
            )

        return super().form_valid(form)


class ListaRecetasView(TemplateView):
    template_name = 'lista_receta.html'
    def get_context_data(self):
        lista = Receta.objects.all()
        return {'lista':lista}
    


class EditarRecetaView(FormView):
    template_name = 'editar_receta.html'
    form_class = RecetaEditarForm
    success_url = reverse_lazy('lista_receta')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        id = self.kwargs.get('id')
        receta = get_object_or_404(Receta, id=id)
        kwargs['instance'] = receta
        return kwargs

    def form_valid(self, form):
        # Guardar los cambios en la receta
        id = self.kwargs.get('id')
        form.save(id)
        return super().form_valid(form)
                
class VerRecetaView(DetailView): #CHECAR SI NO HAY PROBLEMA EN USAR EL DETAILVIEW , YO CREO QUE NO
    model = Receta
    template_name = 'ver_receta.html'
    context_object_name = 'receta'