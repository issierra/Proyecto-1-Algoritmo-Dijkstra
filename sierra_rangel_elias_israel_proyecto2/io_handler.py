"""
Título: Lectura y escritura de conexiones en CSV
Nombre completo: Elias Israel Sierra Rangel
Fecha de creación: 2 de noviembre de 2026
Descripción: Validación de datos y persistencia de las conexiones del
grafo en el archivo nodos.csv.
"""

import csv
import math
from pathlib import Path

from grafo import Grafo

# El CSV vive en este archivo, sin importar de dónde se ejecute
RUTA_CSV: Path = Path(__file__).resolve().parent / "nodos.csv"
ENCABEZADOS: list[str] = ["Origen", "Destino", "Peso"]


def valida_nombre_nodo(nombre: str) -> str:
    """Valida que el nombre de un nodo no esté vacío.

    Args:
        nombre: Texto escrito por el usuario o leído del CSV.

    Returns:
        El nombre sin espacios al inicio ni al final.

    Raises:
        ValueError: Si el nombre está vacío.
    """
    nombre = nombre.strip()
    if nombre == "":
        raise ValueError("El nombre del nodo no puede estar vacío")
    return nombre


def convierte_peso(texto: str) -> float:
    """Convierte un texto en un valor de peso válido para una conexión.

    Args:
        texto: Peso escrito por el usuario o leído del CSV.

    Returns:
        El peso como número decimal, mayor que cero.

    Raises:
        ValueError: Si está vacío, no es un número, no es finito
            o no es mayor que cero.
    """
    texto = texto.strip()
    if texto == "":
        raise ValueError("El peso no puede estar vacío")
    try:
        peso = float(texto)
    except ValueError:
        # "from None" oculta el mensaje técnico de float()
        raise ValueError(f"El peso debe ser un número, no '{texto}'") from None
    if not math.isfinite(peso):
        raise ValueError("El peso debe ser un número finito")
    if peso <= 0:
        raise ValueError("El peso debe ser mayor que cero")
    return peso


def formatea_peso(peso: float) -> str:
    """Da formato a un peso: 4.0 se muestra como 4 y 2.5 como 2.5.

    Args:
        peso: Peso numérico.

    Returns:
        El peso como texto.
    """
    if peso.is_integer():
        return str(int(peso))
    return str(peso)


def _termina_en_salto_de_linea(ruta: Path) -> bool:
    """Indica si el último carácter del archivo es un salto de línea.

    Args:
        ruta: Ruta del archivo, que debe existir y no estar vacío.

    Returns:
        True si el archivo termina en salto de línea.
    """
    with open(ruta, "rb") as archivo:
        archivo.seek(-1, 2)  # Posiciona el cursor en el último byte
        return archivo.read(1) == b"\n"


def guardar_conexion(origen: str, destino: str, peso: float,
                     ruta: Path = RUTA_CSV) -> None:
    """Agrega una conexión al final del CSV (modo append).

    Escribe el encabezado solo si el archivo no existe o está vacío.

    Args:
        origen: Nombre del nodo origen.
        destino: Nombre del nodo destino.
        peso: Peso de la conexión.
        ruta: Ruta del archivo CSV.
    """
    existe_con_datos = ruta.exists() and ruta.stat().st_size > 0
    # Si el archivo se editó a mano y no termina en salto de línea, la
    # fila nueva quedaría pegada a la última
    falta_salto = existe_con_datos and not _termina_en_salto_de_linea(ruta)

    with open(ruta, "a", newline="", encoding="utf-8") as archivo:
        if falta_salto:
            archivo.write("\n")
        escritor = csv.writer(archivo, lineterminator="\n")
        if not existe_con_datos:
            escritor.writerow(ENCABEZADOS)
        escritor.writerow([origen, destino, formatea_peso(peso)])


def _lee_fila(fila: dict[str, str]) -> tuple[str, str, float]:
    """Valida una fila del CSV y extrae sus tres datos.

    Args:
        fila: Diccionario {encabezado: valor} de una fila.

    Returns:
        Tupla (origen, destino, peso).

    Raises:
        KeyError: Si falta una de las columnas esperadas.
        ValueError: Si la fila está incompleta o tiene datos inválidos.
    """
    if None in fila.values():
        raise ValueError("la fila tiene campos faltantes")
    origen = valida_nombre_nodo(fila["Origen"])
    destino = valida_nombre_nodo(fila["Destino"])
    peso = convierte_peso(fila["Peso"])
    if origen == destino:
        raise ValueError("el origen y el destino no pueden ser iguales")
    return origen, destino, peso


def cargar_grafo(ruta: Path = RUTA_CSV) -> tuple[Grafo, int]:
    """Lee el CSV fila por fila y construye el grafo en memoria.

    Las filas con errores se omiten y se informa de cada una, sin
    detener la carga.

    Args:
        ruta: Ruta del archivo CSV.

    Returns:
        Tupla (grafo construido, cantidad de filas omitidas).
    """
    grafo = Grafo()
    omitidas = 0
    try:
        with open(ruta, "r", newline="", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            # La fila 1 es el encabezado, los datos empiezan en la 2
            for numero_fila, fila in enumerate(lector, start=2):
                try:
                    origen, destino, peso = _lee_fila(fila)
                except KeyError as error:
                    omitidas += 1
                    print(f"Fila {numero_fila} omitida: falta la columna "
                          f"{error}")
                except ValueError as error:
                    omitidas += 1
                    print(f"Fila {numero_fila} omitida: {error}")
                else:
                    grafo.agregar_conexion(origen, destino, peso)
    except FileNotFoundError:
        print(f"No existe el archivo '{ruta.name}'.")
    except UnicodeDecodeError:
        print(f"El archivo '{ruta.name}' no está guardado en UTF-8.")
    return grafo, omitidas
