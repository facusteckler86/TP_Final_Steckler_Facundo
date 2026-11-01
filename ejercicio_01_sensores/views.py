import json
import os
from typing import cast

from django.views.generic import TemplateView
from .utils import limpiar_registro_sensor, generar_resumen_sensores

class PanelSensoresView(TemplateView):
    template_name = "ejercicio_1_sensores/panel_sensores.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Cargo los datos de la DB
        ruta_json = os.path.join(os.path.dirname(__file__), 'data', 'sensores_mock.json')
        
        try:
            with open(ruta_json, 'r', encoding='utf-8') as f:
                registros_crudos = json.load(f)
        except FileNotFoundError:
            registros_crudos = []

        sensores_limpios: list[dict[str, object]] = cast(
            list[dict[str, object]],
            [limpiar_registro_sensor(reg) for reg in registros_crudos],
        )

        # Defino el umbra de ejemplo en  25°C)
        UMBRAL = 25.0
        sensores_en_alerta, promedio_temperatura = cast(
            tuple[list[dict[str, object]], float],
            generar_resumen_sensores(sensores_limpios, UMBRAL),
        )

        context['sensores'] = sensores_limpios
        context['sensores_en_alerta'] = sensores_en_alerta
        context['promedio_temperatura'] = round(promedio_temperatura, 2)
        context['umbral'] = UMBRAL

        return context