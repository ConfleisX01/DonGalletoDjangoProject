from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView,UpdateView
from .forms import RecetaEditarForm
from .forms import RecetaRegistrarForm, IngredienteRecetaFormSet,AgregarIngredienteForm
from .models import Receta, IngredienteReceta
from materia_prima.models import MateriaPrima
from django.views.generic import DetailView
from inventarios.models import InventarioProducto

class CrearReceta( FormView):
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
            InventarioProducto.objects.create(galleta=receta, cantidad=0);
            
            for ingrediente in ingredientes:
                ingrediente.receta = receta
                ingrediente.save()

            return super().form_valid(form)
        else:
            # Mostrar errores de validación del formset
            print("Formset no válido")
            for form in ingrediente_formset:
                print(form.errors)  # Imprime los errores de cada formulario en el formset

        return self.form_invalid(form)


class ListaRecetasView( TemplateView):
    template_name = 'lista_receta.html'
    def get_context_data(self):
        lista = Receta.objects.all()
        return {'lista':lista}

class EditarRecetaView(UpdateView):
    model = Receta
    form_class = RecetaEditarForm
    template_name = 'editar_receta.html'
    context_object_name = 'form'
    success_url = reverse_lazy('lista_receta')  # Redirige a la lista de recetas después de guardar

    def get_object(self, queryset=None):
        
        # Aquí usaremos 'pk' que es el identificador por defecto en UpdateView
        return Receta.objects.get(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        receta = self.get_object()
        context['receta'] = receta  # Asegúrate de que 'receta' esté en el contexto
        ingredientes = IngredienteReceta.objects.filter(receta=receta)
        context['ingredientes'] = ingredientes
        return context

class VerRecetaView(DetailView): #CHECAR SI NO HAY PROBLEMA EN USAR EL DETAILVIEW , YO CREO QUE NO
    model = Receta
    template_name = 'ver_receta.html'
    context_object_name = 'receta'
    
class DefinirInsumoView(FormView):
    template_name = 'definir_insumos.html'
    form_class = AgregarIngredienteForm

    def get_context_data(self, **kwargs):
        """Cargar la receta y sus ingredientes para mostrarlos en la plantilla."""
        context = super().get_context_data(**kwargs)
        receta_id = self.kwargs.get('pk')
        receta = get_object_or_404(Receta, id=receta_id)

        ingredientes = IngredienteReceta.objects.filter(receta=receta)
        insumos = MateriaPrima.objects.all()  # Obtener todos los insumos disponibles

        context['receta'] = receta
        context['ingredientes'] = ingredientes
        context['insumos'] = insumos  # Pasamos los insumos para el formulario
        return context

    def post(self, request, *args, **kwargs):
        receta_id = self.kwargs.get('pk')
        receta = get_object_or_404(Receta, id=receta_id)

        # Verificar si el formulario de agregar ingrediente es válido
        if 'agregar_ingrediente' in request.POST:
            insumo_id = request.POST.get('nuevo_insumo')
            cantidad_nueva = request.POST.get('cantidad_nueva')

            if insumo_id and cantidad_nueva:  # Verificar que el insumo esté seleccionado
                insumo = get_object_or_404(MateriaPrima, id=insumo_id)
                ingrediente = IngredienteReceta(
                    receta=receta,
                    insumo=insumo,
                    cantidad_necesaria=cantidad_nueva
                )
                ingrediente.save()
                return redirect('definir_insumos', pk=receta.id)

        # Actualizar la cantidad de ingredientes existentes
        for ingrediente in IngredienteReceta.objects.filter(receta=receta):
            cantidad = request.POST.get(f'cantidad_{ingrediente.id}')
            # Si cantidad no está vacía o ha cambiado, actualizamos
            if cantidad != "" and cantidad is not None:
                ingrediente.cantidad_necesaria = cantidad
                ingrediente.save()

        # Eliminar un ingrediente si se ha solicitado
        if 'eliminar_ingrediente' in request.POST:
            ingrediente_id = request.POST.get('eliminar_ingrediente')
            ingrediente = get_object_or_404(IngredienteReceta, id=ingrediente_id)
            ingrediente.delete()
            return redirect('definir_insumos', pk=receta.id)

        return redirect('editar_receta', pk=receta.id)
