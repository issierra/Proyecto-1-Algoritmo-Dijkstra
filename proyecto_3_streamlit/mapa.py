# Título: Dibujo esquemático de la red como mapa
# Nombre: Elias Israel Sierra Rangel
# Fecha: 15 de noviembre de 2026
# Descripción: Calcula posiciones y genera el svg del mapa de la red

import math

ANCHO_MAPA = 660
ALTO_MAPA = 520
MARGEN_MAPA = 80


def calcula_posiciones(
        nombres: list[str]) -> dict[str, tuple[float, float]]:
    """Reparte los nodos en un círculo dentro del lienzo del mapa.

    Las posiciones son esquemáticas, no coordenadas reales. Los nodos
    se ordenan alfabéticamente y el primero queda en la parte superior.

    Args:
        nombres: Nombres de los nodos del grafo

    Returns:
        Diccionario con la posición (x, y) de cada nodo en el lienzo.
    """
    centro_x = ANCHO_MAPA / 2
    centro_y = ALTO_MAPA / 2
    # Un solo nodo se coloca en el centro
    if len(nombres) == 1:
        return {nombres[0]: (centro_x, centro_y)}

    radio_x = ANCHO_MAPA / 2 - MARGEN_MAPA
    radio_y = ALTO_MAPA / 2 - MARGEN_MAPA
    posiciones = {}
    for indice, nombre in enumerate(sorted(nombres)):
        # Se empieza de arriba (-90°) y se avanazan en sentido horario
        angulo = -math.pi / 2 + 2 * math.pi * indice / len(nombres)
        posiciones[nombre] = (centro_x + radio_x * math.cos(angulo),
                              centro_y + radio_y * math.sin(angulo))
    return posiciones
