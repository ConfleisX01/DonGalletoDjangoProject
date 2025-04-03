from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from clientes.models import Cliente  

class RegistroForm(UserCreationForm):
    is_superuser = forms.BooleanField(required=False, initial=False)
    
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre de usuario"})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Correo electrónico"})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Contraseña"})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Confirmar contraseña"})
    )
    is_superuser = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "is_superuser"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_superuser = self.cleaned_data["is_superuser"]
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()
            if not user.is_superuser:  # Solo usuarios normales se guardan en Cliente
                Cliente.objects.create(user=user, user_type="cliente")

        return user
