
from django.urls import path
from .views import dashboard

urlpatterns = [
    path('dashboard-ventas-diarias/', dashboard, name='dashboard_ventas'),
]
