import json
import os

# Genero la excepcion personalizada
class StockInvalidoError(Exception):
    """Excepción personalizada para stock negativo o inválido."""
    pass

class DispositivoEcologico:
    def __init__(self, id_dispositivo: str, modelo: str, stock: int) -> None:
        self.id_dispositivo = id_dispositivo
        self.modelo = modelo
        self.stock = stock  # Invoca al setter para validar

    @property
    def stock(self) -> int:
        return self.__stock

    @stock.setter
    def stock(self, valor: int) -> None:
        if valor < 0:
            raise StockInvalidoError(f"Error de stock para '{self.modelo}': El stock no puede tomar valores negativos ({valor}).")
        self.__stock = valor

    def generar_ficha_tecnica(self):
        return f"FICHA COMERCIAL BÁSICA:\nID: {self.id_dispositivo}\nModelo: {self.modelo}\nStock Disponible: {self.__stock}"


class PanelSolar(DispositivoEcologico):
    def __init__(self, id_dispositivo: str, modelo: str, stock: int, potencia_w: int, tipo_celda: str) -> None:
        super().__init__(id_dispositivo, modelo, stock)
        self.potencia_w = potencia_w
        self.tipo_celda = tipo_celda

    def generar_ficha_tecnica(self):
        ficha_base = super().generar_ficha_tecnica()
        return (
            f"{ficha_base}\n"
            f"Tipo de Dispositivo: Panel Solar\n"
            f"Potencia Nominal: {self.potencia_w} W\n"
            f"Tecnología de Celda: {self.tipo_celda}"
        )


class GestorInventario:
    @staticmethod
    def guardar_catalogo_json(lista_dispositivos: list[DispositivoEcologico], ruta_archivo: str) -> None:
        datos: list[dict[str, object]] = []
        for disp in lista_dispositivos:
            item: dict[str, object] = {
                "id_dispositivo": disp.id_dispositivo,
                "modelo": disp.modelo,
                "stock": disp.stock
            }
            # Identificamos atributos específicos si es un Panel Solar por ej
            if isinstance(disp, PanelSolar):
                item["categoria"] = "PanelSolar"
                item["potencia_w"] = disp.potencia_w
                item["tipo_celda"] = disp.tipo_celda
            else:
                item["categoria"] = "DispositivoEcologicoGenerico"
            
            datos.append(item)

        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)
        print(f"\n[ÉXITO] Catálogo exportado correctamente al archivo: '{ruta_archivo}'.")

    @staticmethod
    def cargar_catalogo_json(ruta_archivo: str) -> list[DispositivoEcologico]:
        """Lee la base de datos JSON y reconstruye las instancias de objetos."""
        if not os.path.exists(ruta_archivo):
            print(f"[ADVERTENCIA] El archivo '{ruta_archivo}' no existe todavía.")
            return []

        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            datos = json.load(f)

        lista_dispositivos: list[DispositivoEcologico] = []
        for item in datos:
            categoria = item.get("categoria")
            if categoria == "PanelSolar":
                dispositivo = PanelSolar(
                    id_dispositivo=item["id_dispositivo"],
                    modelo=item["modelo"],
                    stock=item["stock"],
                    potencia_w=item["potencia_w"],
                    tipo_celda=item["tipo_celda"]
                )
            else:
                dispositivo = DispositivoEcologico(
                    id_dispositivo=item["id_dispositivo"],
                    modelo=item["modelo"],
                    stock=item["stock"]
                )
            lista_dispositivos.append(dispositivo)

        print(f"\n[ÉXITO] Catálogo cargado correctamente desde la base de datos: '{ruta_archivo}'.")
        return lista_dispositivos


# Aca es donde se aplican las pruebas
if __name__ == "__main__":
    print("=== INICIO DE PRUEBAS ECOTECH SOLUTIONS ===\n")

    # 1. Verificación de captura controlada de StockInvalidoError
    print("1. Probando la validación de stock negativo...")
    try:
        # Intentamos crear un dispositivo con stock negativo para forzar el error
        dispositivo_fallido = DispositivoEcologico("DEV-ERR", "Medidor Falla", -10)
    except StockInvalidoError as e:
        print(f"-> [EXCEPCIÓN CAPTURADA EXITOSAMENTE]: {e}\n")

    # 2. Creación de productos válidos y guardado en JSON (DB)
    print("2. Creando instancias válidas y guardando en JSON...")
    try:
        generico = DispositivoEcologico("GEN-01", "Filtro de Agua Sustentable", 50)
        panel1 = PanelSolar("PAN-101", "SunPower Max 400W", 15, 400, "Monocristalino")
        panel2 = PanelSolar("PAN-102", "EcoPanel Lite", 30, 250, "Policristalino")

        catalogo_productos: list[DispositivoEcologico] = [generico, panel1, panel2]
        archivo_db = os.path.join(os.path.dirname(__file__), "catalogo_ecotech.json")
        
        # Guardamos en el archivo JSON (creo la DB)
        GestorInventario.guardar_catalogo_json(catalogo_productos, archivo_db)

        # 3. Lectura del JSON que lo uso como DB
        print("\n3. Leyendo el archivo JSON como base de datos e imprimiendo fichas:")
        catalogo_desde_db = GestorInventario.cargar_catalogo_json(archivo_db)

        print("-" * 50)
        for disp in catalogo_desde_db:
            print(disp.generar_ficha_tecnica())
            print("-" * 50)

    except Exception as ex:
        print(f"Ocurrió un error inesperado durante la ejecución: {ex}")

    print("\n=== FIN DE LAS PRUEBAS ===")