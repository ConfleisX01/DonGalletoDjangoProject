from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from main.forms import RegistroForm
from django.views.generic import FormView
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required


def main(request):
    return render(request, "main.html")

@login_required
def welcome(request):
    return render(request, 'welcome.html')

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
            login(request, user)

            #se verifica primero si es admin o solo usuario:
            if user.is_superuser:
                return redirect("panel.html")
            else:
                return redirect("welcome.html")
    else:
        form = RegistroForm()

    return render(request, "registration/registro.html", {"form": form})