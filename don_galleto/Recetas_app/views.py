from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView,UpdateView
from .models import Receta
from .forms import RecetaEditarForm
from django.urls import reverse_lazy
from django.views.generic import FormView
from .forms import RecetaRegistrarForm, IngredienteRecetaFormSet, IngredienteRecetaForm
from django.forms.models import modelformset_factory
from .models import Receta, IngredienteReceta
from django.views.generic import DetailView

class CrearReceta(FormView):
    template_name = 'crear_receta.html'
    form_class = RecetaRegistrarForm
    success_url = reverse_lazy('lista_receta')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["ingrediente_formset"] = IngredienteRecetaFormSet(self.request.POST)
        else:
            context["ingrediente_formset"] = IngredienteRecetaFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        ingrediente_formset = context["ingrediente_formset"]

        if ingrediente_formset.is_valid():
            receta = form.save()
            ingredientes = ingrediente_formset.save(commit=False)

            for ingrediente in ingredientes:
                ingrediente.receta = receta
                ingrediente.save()

            return super().form_valid(form)

        return self.form_invalid(form)


class ListaRecetasView(TemplateView):
    template_name = 'lista_receta.html'
    def get_context_data(self):
        lista = Receta.objects.all()
        return {'lista':lista}

class EditarRecetaView( UpdateView):
    model = Receta
    form_class = RecetaEditarForm
    template_name = 'editar_receta.html'
    context_object_name = 'form'
    success_url = reverse_lazy('lista_receta')  # Redirige a la lista de recetas después de guardar

    def get_object(self, queryset=None):
        return Receta.objects.get(id=self.kwargs['id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtenemos la receta y sus ingredientes asociados
        receta = self.get_object()
        
        # Agregamos los ingredientes al contexto para solo visualizarlos
        ingredientes = IngredienteReceta.objects.filter(receta=receta)
        print(f"ingredientes {ingredientes}")
        
        context['ingredientes'] = ingredientes  # Pasamos los ingredientes al contexto
        
        return context

class VerRecetaView(DetailView): #CHECAR SI NO HAY PROBLEMA EN USAR EL DETAILVIEW , YO CREO QUE NO
    model = Receta
    template_name = 'ver_receta.html'
    context_object_name = 'receta'
    
class DefinirInsumoView(TemplateView):
    template_name = 'definir_insumos.html'

    def get_context_data(self, **kwargs):
        """Cargar la receta y sus ingredientes para mostrarlos en la plantilla."""
        context = super().get_context_data(**kwargs)
        receta_id = self.kwargs.get('id')
        receta = get_object_or_404(Receta, id=receta_id)

        ingredientes = IngredienteReceta.objects.filter(receta=receta)

        context['receta'] = receta
        context['ingredientes'] = ingredientes
        return context

    def post(self, request, *args, **kwargs):
        receta_id = self.kwargs.get('id')
        receta = get_object_or_404(Receta, id=receta_id)
        
        ingredientes = IngredienteReceta.objects.filter(receta=receta)
        
        for ingrediente in ingredientes:
            cantidad = request.POST.get(f'cantidad_{ingrediente.id}')
            if cantidad:
                ingrediente.cantidad_necesaria = cantidad
                ingrediente.save()
        
        return redirect('lista_receta')