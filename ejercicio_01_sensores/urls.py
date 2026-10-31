from django.urls import path
from .views import PanelSensoresView

app_name = 'ejercicio_1'

urlpatterns = [
    path('panel/', PanelSensoresView.as_view(), name='panel_sensores'),
]