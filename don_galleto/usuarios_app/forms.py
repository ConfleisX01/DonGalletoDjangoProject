from django import forms
from django.contrib.auth.models import User
from .models import Usuario
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.hashers import make_password

class UsuarioForm(forms.ModelForm):
    username = forms.CharField(
        label="Nombre de usuario", 
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="Contraseña", 
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label="Confirmar contraseña", 
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        label="Nombre", 
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        label="Apellido", 
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    telefono = forms.CharField(
        label="Teléfono", 
        max_length=10,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    rol = forms.ChoiceField(
        label="Rol", 
        choices=[("admin", "Administrador"), ("user", "Usuario")],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ["username", "password", "password2", "email", "first_name", "last_name", "telefono", "rol"]

    def clean_password(self):
        password = self.cleaned_data.get("password")

        if password is None:
            raise ValidationError("La contraseña es requerida.")

        # Validar que la contraseña tenga al menos 8 caracteres
        if len(password) < 8:
            raise ValidationError("La contraseña debe tener al menos 8 caracteres.")

        # Validar que la contraseña tenga al menos una letra mayúscula
        if not re.search(r'[A-Z]', password):
            raise ValidationError("La contraseña debe tener al menos una letra mayúscula.")

        # Validar que la contraseña tenga al menos una letra minúscula
        if not re.search(r'[a-z]', password):
            raise ValidationError("La contraseña debe tener al menos una letra minúscula.")

        # Validar que la contraseña tenga al menos un número
        if not re.search(r'[0-9]', password):
            raise ValidationError("La contraseña debe tener al menos un número.")

        # Validar que la contraseña tenga al menos un carácter especial
        if not re.search(r'[\W_]', password):
            raise ValidationError("La contraseña debe tener al menos un carácter especial.")

        # Validar la contraseña contra la lista de contraseñas inseguras
        try:
            validate_password(password)
        except ValidationError as e:
            raise ValidationError(e.messages)

        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        # Validar que ambas contraseñas coincidan
        if password and password2 and password != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["username"]
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.is_staff = self.cleaned_data["rol"] == "admin"

        # Encriptar la contraseña antes de guardarla
        user.password = make_password(self.cleaned_data["password"])

        if commit:
            user.save()

        # Crear el modelo Usuario asociado
        usuario = Usuario(user=user, telefono=self.cleaned_data["telefono"], user_type=self.cleaned_data["rol"])
        if commit:
            usuario.save()

        return user
    

class EditarUsuarioForm(forms.ModelForm):
    username = forms.CharField(
        label="Nombre de usuario", 
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
    )
    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        label="Nombre", 
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        label="Apellido", 
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    telefono = forms.CharField(
        label="Teléfono", 
        max_length=10,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    rol = forms.ChoiceField(
        label="Rol", 
        choices=[("admin", "Administrador"), ("user", "Usuario")],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    # Campos opcionales para la contraseña
    password = forms.CharField(
        label="Nueva Contraseña", 
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Dejar en blanco si no cambia'}),
        required=False
    )
    password2 = forms.CharField(
        label="Confirmar Contraseña", 
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar nueva contraseña'}),
        required=False
    )

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "telefono", "rol"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password or password2:  # Si el usuario ingresó una nueva contraseña
            if password != password2:
                raise forms.ValidationError("Las contraseñas no coinciden.")
            if len(password) < 6:
                raise forms.ValidationError("La contraseña debe tener al menos 6 caracteres.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["username"]
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.is_staff = self.cleaned_data["rol"] == "admin"

        # Si el usuario ingresó una nueva contraseña, la encriptamos antes de guardarla
        password = self.cleaned_data.get("password")
        if password:
            user.password = make_password(password)

        if commit:
            user.save()

        # Actualizar modelo Usuario si existe
        usuario, created = Usuario.objects.get_or_create(user=user)
        usuario.telefono = self.cleaned_data["telefono"]
        usuario.user_type = self.cleaned_data["rol"]
        if commit:
            usuario.save()

        return user


