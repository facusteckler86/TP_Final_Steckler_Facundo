from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sensor/', include('ejercicio_01_sensores.urls')), # Conecta con tu app
]
