from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from main.forms import RegistroForm
from django.views.generic import FormView, ListView
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from Recetas_app.models import Receta
class WelcomeView(ListView):
    template_name = 'welcome.html'
    model = Receta
    context_object_name = 'productos'

def main(request):
    return render(request, "main.html")

def principal(request):
    return render(request, 'inicio.html')

@login_required
def panel(request):
    return render(request, 'panel.html')

def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            #se verifica primero si es admin o solo usuario:
            if user.is_superuser:
                return redirect("panel")
            else:
                return redirect("welcome")
            return redirect("welcome")
    else:
        form = RegistroForm()

    return render(request, "registration/registro.html", {"form": form})