from django import forms
from .models import Receta, InsumoTemporal, IngredienteReceta

class SelectInsumos(forms.ModelMultipleChoiceField):  
    def label_from_instance(self, obj):
        return obj.nombreIn 

class RecetaRegistrarForm(forms.ModelForm):
    ingredientes = SelectInsumos(
        queryset=InsumoTemporal.objects.all(),
        widget=forms.CheckboxSelectMultiple(),  # Casillas de verificación para elegir ingredientes
        required=True,
        label="Ingredientes"
    )

    class Meta:
        model = Receta
        fields = ['nombre', 'cantidad_galletas_producidas', 'peso_individual', 'ingredientes']
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "cantidad_galletas_producidas": forms.NumberInput(attrs={"class": "form-control"}),
            "peso_individual": forms.NumberInput(attrs={"class": "form-control"}),
        }

    def save(self, commit=True):
        receta = super().save(commit=False)  # Guarda la receta sin enviarla a la BD aún
        if commit:
            receta.save()  # Guarda la receta en la BD
            ingredientes = self.cleaned_data["ingredientes"]  # Obtiene los ingredientes seleccionados

            # Crear la relación en IngredienteReceta
            for insumo in ingredientes:
                IngredienteReceta.objects.create(
                    receta=receta,
                    insumo=insumo,
                    cantidad_necesaria=0  # Puedes modificar esto para capturar la cantidad real
                )

        return receta


class RecetaEditarForm(forms.ModelForm):
    nombre = forms.CharField(label='Nombre', max_length=100)
    cantidad_galletas_producidas = forms.IntegerField(label='Cantidad de galletas producidas')
    peso_individual = forms.DecimalField(label='Peso individual', max_digits=10, decimal_places=2)
    ingredientes = forms.ModelMultipleChoiceField(
        queryset=InsumoTemporal.objects.all(),
        label='Ingredientes',
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Receta
        fields = ['nombre', 'cantidad_galletas_producidas', 'peso_individual', 'ingredientes']

    def save(self, id):
        # Obtener la receta existente
        receta = Receta.objects.filter(id=id).first()
        # Actualizar los campos de la receta
        receta.nombre = self.cleaned_data["nombre"]
        receta.cantidad_galletas_producidas = self.cleaned_data["cantidad_galletas_producidas"]
        receta.peso_individual = self.cleaned_data["peso_individual"]
        receta.save()

        # Limpiar los ingredientes actuales de la receta
        IngredienteReceta.objects.filter(receta=receta).delete()

        # Asociar los nuevos ingredientes a la receta
        ingredientes = self.cleaned_data["ingredientes"]
        for insumo in ingredientes:
            IngredienteReceta.objects.create(
                receta=receta,
                insumo=insumo,
                cantidad_necesaria=1  # !!!CHECAR ESTO CUANDO EL INVENTARIO DE INSUMOS ESTE!!!
            )
            
