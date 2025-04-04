from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from main.views import principal, panel, WelcomeView
from clientes.views import ListaCarritoComprasView

urlpatterns = [
    path('', principal, name='home'),
    path('welcome/', WelcomeView.as_view(), name='welcome'),
    path("accounts/", include("django.contrib.auth.urls")),
    path("compras/", include('ventas_app.urls')),
    path("mi_carrito/", ListaCarritoComprasView.as_view(), name="carrito_de_compras"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
