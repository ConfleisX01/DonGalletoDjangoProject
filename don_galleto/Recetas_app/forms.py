from django import forms
from .models import Receta, IngredienteReceta
from materia_prima.models import MateriaPrima

class SelectInsumos(forms.ModelMultipleChoiceField):  
    def label_from_instance(self, obj):
        return obj.nombre_insumo

class RecetaRegistrarForm(forms.ModelForm):
    precio_galleta = forms.DecimalField(
        label='Precio Galleta',
        max_digits=10,
        decimal_places=5,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Precio galleta'})
    )

    class Meta:
        model = Receta
        fields = ['nombre', 'cantidad_galletas_producidas', 'peso_individual', 'precio_galleta']
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


class IngredienteForm(forms.ModelForm):
    class Meta:
        model = IngredienteReceta
        fields = ['insumo', 'cantidad_necesaria']
        widgets = {
            'insumo': forms.Select(attrs={'class': 'form-control'}),
            'cantidad_necesaria': forms.NumberInput(attrs={'class': 'form-control'})
        }

# Formset para los ingredientes
IngredienteFormSet = forms.inlineformset_factory(
    Receta,
    IngredienteReceta,
    form=IngredienteForm,
    extra=1,
    can_delete=True,
    fields=['insumo', 'cantidad_necesaria']
)

class RecetaRegistrarForm(forms.ModelForm):
    precio_galleta = forms.DecimalField(
        label='Precio Galleta', 
        max_digits=10, 
        decimal_places=5,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Precio galleta'
        })
    )

    class Meta:
        model = Receta
        fields = ['nombre', 'cantidad_galletas_producidas', 'peso_individual', 'precio_galleta']
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "cantidad_galletas_producidas": forms.NumberInput(attrs={"class": "form-control"}),
            "peso_individual": forms.NumberInput(attrs={"class": "form-control"}),
        }

class RecetaEditarForm(forms.ModelForm):
    class Meta:
        model = Receta
        fields = ['nombre', 'cantidad_galletas_producidas', 'peso_individual', 'precio_galleta']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad_galletas_producidas': forms.NumberInput(attrs={'class': 'form-control'}),
            'peso_individual': forms.NumberInput(attrs={'class': 'form-control'}),
            'precio_galleta': forms.NumberInput(attrs={'class': 'form-control'})
        }

    def save(self, commit=True):
        receta = super().save(commit=False)

        if commit:
            receta.save()  # Guardamos la receta

        return receta

            
class IngredienteRecetaForm(forms.ModelForm):
    class Meta:
        model = IngredienteReceta
        fields = ['insumo']
