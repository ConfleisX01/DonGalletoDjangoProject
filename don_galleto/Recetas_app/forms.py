from django import forms
from .models import Receta, IngredienteReceta
from django.forms import inlineformset_factory
from materia_prima.models import MateriaPrima 


class AgregarIngredienteForm(forms.Form):
    nuevo_insumo = forms.ModelChoiceField(
        queryset=MateriaPrima.objects.all(), 
        label="Insumo",
        empty_label="Seleccione un insumo",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    cantidad_nueva = forms.DecimalField(
        label="Cantidad",
        decimal_places=2,
        max_digits=10,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad'})
    )


class IngredienteRecetaForm(forms.ModelForm):
    cantidad_necesaria = forms.DecimalField(
        max_digits=5,
        decimal_places=2,  # Usualmente dos decimales son suficientes
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Cantidad necesaria',
            'min': 0,  # Garantizar que la cantidad sea positiva
            'step': 'any'  # Permite decimales
        })
    )

    class Meta:
        model = IngredienteReceta
        fields = ['insumo', 'cantidad_necesaria']
        widgets = {
            'insumo': forms.Select(attrs={'class': 'form-control'}),
        }



# Formulario para registrar una nueva receta
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

    def save(self, commit=True):
        receta = super().save(commit=False)
        if commit:
            receta.save()  # Guarda la receta
        return receta


# Formulario para editar una receta existente
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


# Formset para los ingredientes de la receta
IngredienteRecetaFormSet = inlineformset_factory(
    Receta,  # Modelo padre
    IngredienteReceta,  # Modelo relacionado
    form=IngredienteRecetaForm,  # Formulario para los ingredientes
    extra=1,  # Mínimo un ingrediente
    can_delete=True  # Permite eliminar ingredientes en la edición
)
