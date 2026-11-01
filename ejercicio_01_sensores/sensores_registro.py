import re
from typing import Mapping, TypedDict

class SensorLimpio(TypedDict):
    sensor_id: str
    temperatura: float
    ubicacion: str

def limpiar_registro_sensor(registro_raw: Mapping[str, object]) -> SensorLimpio:

    # Punto A: Normalizo las lecturas

    sensor_id_raw = registro_raw.get("sensor_id", "")
    sensor_id = sensor_id_raw.strip() if isinstance(sensor_id_raw, str) else "SENSOR-UNKNOWN"
    if not sensor_id:
        sensor_id = "SENSOR-UNKNOWN"

    
    temp_raw = registro_raw.get("temperatura", 0.0)
    if isinstance(temp_raw, str):
        match = re.search(r'[-+]?\d+(?:\.\d*)?|[-+]?\.\d+', temp_raw)
        temperatura = float(match.group()) if match else 0.0
    elif isinstance(temp_raw, (int, float)):
        temperatura = float(temp_raw)
    else:
        temperatura = 0.0

    # Ubicacion por defecto
    ubicacion_raw = registro_raw.get("ubicacion")
    if isinstance(ubicacion_raw, str) and ubicacion_raw.strip():
        ubicacion = ubicacion_raw.strip()
    else:
        ubicacion = "Planta General (Por Defecto)"

    return {
        "sensor_id": sensor_id,
        "temperatura": temperatura,
        "ubicacion": ubicacion
    }


def generar_resumen_sensores(
    lista_sensores_limpios: list[SensorLimpio],
    umbral_temperatura: float,
) -> tuple[list[str], float]:
    
    # Punto B: Monitoreo y Mapeo Estadístico.
        
    lista_sensores_alerta: list[str] = []
    suma_temperaturas = 0.0
    total_sensores = len(lista_sensores_limpios)

    if total_sensores == 0:
        return [], 0.0

    for sensor in lista_sensores_limpios:
        temp = sensor["temperatura"]
        suma_temperaturas += temp
        
        if temp > umbral_temperatura:
            lista_sensores_alerta.append(sensor["sensor_id"])

    promedio_temperatura = suma_temperaturas / total_sensores

    return lista_sensores_alerta, promedio_temperatura

# Bloque de ejecución

if __name__ == "__main__":
    # Datos crudos para analizar
    registros_crudos: list[Mapping[str, object]] = [
        {"sensor_id": " SENSOR-001 ", "temperatura": "24.5C", "ubicacion": "Planta Norte"},
        {"sensor_id": "SENSOR-002", "temperatura": " 31.8 °C", "ubicacion": "   "},
        {"sensor_id": " SENSOR-003", "temperatura": "19.2", "ubicacion": "Planta Sur"},
        {"sensor_id": "SENSOR-004", "temperatura": "28.4°C", "ubicacion": None}
    ]

    print("--- 1. PROCESO DE SANITIZACIÓN ---")
    sensores_limpios: list[SensorLimpio] = []
    for reg in registros_crudos:
        sensor_limpio = limpiar_registro_sensor(reg)
        sensores_limpios.append(sensor_limpio)
        print(f"Crudo: {reg}  -->  Limpio: {sensor_limpio}")

    print("\n--- 2. ANÁLISIS ESTADÍSTICO Y REPORTES ---")
    UMBRAL = 25.0
    sensores_en_alerta, promedio_global = generar_resumen_sensores(sensores_limpios, UMBRAL)

    print(f"Umbral de temperatura configurado: {UMBRAL} °C")
    print(f"Promedio térmico global de la planta: {promedio_global:.2f} °C")
    print(f"Dispositivos que superan el umbral (Alerta): {sensores_en_alerta}")
