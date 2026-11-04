"""
Título: Red de transporte - rutas más cortas
Nombre completo: Elias Israel Sierra Rangel
Fecha de creación: 2 de noviembre de 2026
Descripción: Programa interactivo que captura conexiones, las guarda en
un CSV, carga el grafo y calcula la ruta más corta con Dijkstra.
"""

from grafo import Grafo
from io_handler import (cargar_grafo, convierte_peso, formatea_peso,
                        guardar_conexion, valida_nombre_nodo)


def pide_si_no(mensaje: str) -> bool:
    """Pregunta hasta recibir una respuesta de sí o no.

    Args:
        mensaje: Pregunta que se muestra al usuario.

    Returns:
        True si la respuesta es sí, False si es no.
    """
    while True:
        respuesta = input(mensaje).strip().lower()
        if respuesta in ("s", "si", "sí", "SI", "SÍ",
                         "S", "Sí", "sI", "Si", "sÍ"):
            return True
        if respuesta in ("n", "no", "NO", "N", "No", "nO"):
            return False
        print("Validación: responde 's' para sí o 'n' para no")


def pide_nodo(mensaje: str) -> str:
    """Pide el nombre de un nodo hasta recibir uno válido.

    Args:
        mensaje: Texto que se muestra al usuario.

    Returns:
        Nombre del nodo ya validado.
    """
    while True:
        try:
            nombre = valida_nombre_nodo(input(mensaje))
        except ValueError as error:
            print(f"Validación: {error}")
        else:
            return nombre


def pide_destino(origen: str) -> str:
    """Pide el nodo destino, que debe ser distinto del origen.

    Args:
        origen: Nombre del nodo origen ya capturado.

    Returns:
        Nombre del nodo destino.
    """
    while True:
        destino = pide_nodo("Nodo destino: ")
        if destino != origen:
            return destino
        print("Validación: el destino debe ser distinto del origen")


def pide_peso() -> float:
    """Pide el peso de una conexión hasta recibir uno válido.

    Returns:
        Peso como número decimal mayor que cero.
    """
    while True:
        try:
            peso = convierte_peso(input("Peso de la conexión: "))
        except ValueError as error:
            print(f"Validación: {error}")
        else:
            return peso


def pide_nodo_existente(grafo: Grafo, mensaje: str) -> str:
    """Pide un nodo hasta que exista en el grafo cargado.

    Args:
        grafo: Grafo en el que se busca el nodo.
        mensaje: Texto que se muestra al usuario.

    Returns:
        Nombre de un nodo que existe en el grafo.
    """
    while True:
        nombre = pide_nodo(mensaje)
        if grafo.existe_nodo(nombre):
            return nombre
        disponibles = ", ".join(sorted(grafo.nodos))
        print(f"Validación: el nodo '{nombre}' no existe. "
              f"Disponibles: {disponibles}")


def captura_conexiones() -> None:
    """Captura conexiones por consola y las guarda en el CSV."""
    while pide_si_no("¿Deseas agregar una conexión? (s/n): "):
        origen = pide_nodo("Nodo origen: ")
        destino = pide_destino(origen)
        peso = pide_peso()
        try:
            guardar_conexion(origen, destino, peso)
        except OSError as error:
            # OSError agrupa los fallos de disco (permisos, ruta, etc.)
            print(f"No se pudo escribir en el archivo: {error}")
        else:
            print(f"Guardado: {origen},{destino},{formatea_peso(peso)}")


def main() -> None:
    """Ejecuta el programa completo: capturar, cargar y calcular."""
    print("=== Red de transporte: ruta más corta ===")
    captura_conexiones()

    grafo, omitidas = cargar_grafo()
    if not grafo.nodos:
        print("No hay conexiones cargadas. Agrega al menos una.")
        return
    print(f"Red cargada: {len(grafo.nodos)} nodos, "
          f"{omitidas} filas omitidas.")
    print("Nodos disponibles:", ", ".join(sorted(grafo.nodos)))

    inicio = pide_nodo_existente(grafo, "Nodo de inicio: ")
    destino = pide_nodo_existente(grafo, "Nodo de destino: ")
    distancia, camino = grafo.dijkstra(inicio, destino)

    if not camino:
        print(f"No existe una ruta entre {inicio} y {destino}.")
        return
    print("Ruta más corta:", " -> ".join(camino))
    print("Peso total:", formatea_peso(distancia))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nPrograma cancelado por el usuario.")
