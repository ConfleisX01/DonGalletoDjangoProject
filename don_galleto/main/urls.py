from django.urls import path
from main.views import main, welcome ,principal, panel
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('', principal, name='home'),
    

] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)