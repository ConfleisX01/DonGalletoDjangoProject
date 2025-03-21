from django.shortcuts import render
from django.views.generic.base import TemplateView

def main(request):
    return render(request, "main.html")

def welcome(request):
    return render(request, 'welcome.html')