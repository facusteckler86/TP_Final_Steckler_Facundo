import re
from typing import Mapping, TypedDict


class SensorLimpio(TypedDict):
    sensor_id: str
    temperatura: float
    ubicacion: str


def limpiar_registro_sensor(registro_raw: Mapping[str, object]) -> SensorLimpio:
    sensor_id_raw = registro_raw.get("sensor_id", "")
    if isinstance(sensor_id_raw, str):
        sensor_id = sensor_id_raw.strip() or "SENSOR-UNKNOWN"
    else:
        sensor_id = "SENSOR-UNKNOWN"

    temperatura_raw = registro_raw.get("temperatura", 0.0)
    if isinstance(temperatura_raw, str):
        coincidencia = re.search(r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)", temperatura_raw)
        temperatura = float(coincidencia.group()) if coincidencia else 0.0
    elif isinstance(temperatura_raw, (int, float)):
        temperatura = float(temperatura_raw)
    else:
        temperatura = 0.0

    ubicacion_raw = registro_raw.get("ubicacion")
    ubicacion = (
        ubicacion_raw.strip()
        if isinstance(ubicacion_raw, str) and ubicacion_raw.strip()
        else "Planta General (Por Defecto)"
    )

    return {
        "sensor_id": sensor_id,
        "temperatura": temperatura,
        "ubicacion": ubicacion,
    }


def generar_resumen_sensores(
    lista_sensores_limpios: list[SensorLimpio],
    umbral_temperatura: float,
) -> tuple[list[str], float]:
    if not lista_sensores_limpios:
        return [], 0.0

    lista_sensores_alerta: list[str] = []
    suma_temperaturas = 0.0

    for sensor in lista_sensores_limpios:
        temperatura = sensor["temperatura"]
        suma_temperaturas += temperatura
        if temperatura > umbral_temperatura:
            lista_sensores_alerta.append(sensor["sensor_id"])

    promedio_temperatura = suma_temperaturas / len(lista_sensores_limpios)
    return lista_sensores_alerta, promedio_temperatura