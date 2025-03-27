from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class RegistroForm(UserCreationForm):
    is_superuser = forms.BooleanField(required= False, initial= False)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "is_superuser"]

        def save(self, commit=True):
            user = super().save(commit=False)
            user.is_superuser = self.cleaned_data["is_superuser"]  # se asigna el rol según el registro
            user.email = self.cleaned_data["email"]  # se guarda el email

            if commit:
                user.save()
            return user