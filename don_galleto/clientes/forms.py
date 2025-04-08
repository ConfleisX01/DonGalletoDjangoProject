from django.contrib.auth.models import User
from django import forms
from clientes.models import Cliente
from ventas_app.models import Venta

class ConfirmarCarritoForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['fecha_recoleccion']
        widgets = {
            'fecha_recoleccion': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
        }

class ClienteCrearForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombres'})
    )

    last_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos'})
    )

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'})
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'})
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
    )

    class Meta:
        model = Cliente
        fields = []  # No necesitamos campos adicionales, ya que estamos usando User.

    def save(self, commit=True):
        # Crear el usuario de manera segura
        user = User.objects.create_user(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']  # set_password se usa internamente en create_user
        )

        # Crear el cliente relacionado con el usuario
        cliente = Cliente.objects.create(user=user, user_type='cliente')

        return cliente
    



class ClienteEditarForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombres'})
    )

    last_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos'})
    )

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario', 'readonly': 'readonly'})
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'})
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
        required=False 
    )

    class Meta:
        model = Cliente
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
    
    def __init__(self, *args, **kwargs):
        # Llamamos al init del formulario padre
        super().__init__(*args, **kwargs)
    
    # Si la instancia existe (estamos editando un cliente), pre-poblamos los campos
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['username'].initial = self.instance.user.username  # Lo haremos readonly
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        # Actualizar la información del usuario
        user = self.instance.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        
        # Solo actualizamos la contraseña si fue cambiada
        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])
        
        user.save()
        return self.instance