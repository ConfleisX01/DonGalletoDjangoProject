import pandas as pd
import plotly.express as px
from django.db.models import F, Sum
from django.shortcuts import render
from .models import Venta

def dashboard(request):
    # Obtener las ventas diarias con el total de ventas, calculando desde DetalleVenta
    ventas_diarias = Venta.objects.annotate(
        total_vendido=Sum(F('detalleventa__cantidad') * F('detalleventa__precio_unitario'))
    ).values('fecha', 'total_vendido')

    # Prepara los datos para el gráfico
    fechas = [venta['fecha'] for venta in ventas_diarias]
    totales = [venta['total_vendido'] for venta in ventas_diarias]

    # Crear un DataFrame con pandas
    df = pd.DataFrame({
        'Fecha': fechas,
        'Total Vendido': totales
    })

    # Crear el gráfico con Plotly usando el DataFrame
    fig = px.line(df, x='Fecha', y='Total Vendido', labels={'x': 'Fecha', 'y': 'Total Vendido'}, title='Ventas Diarias')

    # Convertir el gráfico a HTML para que se pueda incrustar en el template
    graph_html = fig.to_html(full_html=False)

    return render(request, 'dashboard.html', {'graph_html': graph_html})
