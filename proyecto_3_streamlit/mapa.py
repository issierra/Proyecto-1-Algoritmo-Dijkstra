# Título: Dibujo esquemático de la red como mapa
# Nombre: Elias Israel Sierra Rangel
# Fecha: 15 de noviembre de 2026
# Descripción: Calcula posiciones y genera el svg del mapa de la red

import math
from html import escape

from grafo import Grafo
from io_handler import formatea_peso

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


def crea_svg_mapa(grafo: Grafo) -> str:
    """Genera el SVG del mapa con nodos, conexiones y pesos.

    Args:
        grafo: Grafo cargado en memoria

    Returns:
        Texto con el SVG completo, listo para mostrarse en una página.
    """
    posiciones = calcula_posiciones(list(grafo.nodos))
    partes = [f'<svg xmlns="http://www.w3.org/2000/svg" '
              f'viewBox="0 0 {ANCHO_MAPA} {ALTO_MAPA}" '
              f'width="100%" font-family="sans-serif">',
              f'<rect width="{ANCHO_MAPA}" height="{ALTO_MAPA}" '
              f'rx="12" fill="#EEF2F5"/>']

    # Primero las líneas, para que los nodos queden encima
    etiquetas = []
    for origen in sorted(grafo.nodos):
        for destino, peso in sorted(grafo.nodos[origen].vecinos.items()):
            # Cada conexión se guarda en ambos sentidos: se dibuja una vez
            if origen < destino:
                x1, y1 = posiciones[origen]
                x2, y2 = posiciones[destino]
                partes.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" '
                              f'x2="{x2:.1f}" y2="{y2:.1f}" '
                              f'stroke="#9AA5B1" stroke-width="5" '
                              f'stroke-linecap="round"/>')
                etiquetas.append(((x1 + x2) / 2, (y1 + y2) / 2,
                                  formatea_peso(peso)))

    # Los pesos van sobre las líneas, en una etiqueta en el punto medio
    for x, y, texto in etiquetas:
        ancho = 10 * len(texto) + 14
        partes.append(f'<rect x="{x - ancho / 2:.1f}" y="{y - 11:.1f}" '
                      f'width="{ancho}" height="22" rx="11" '
                      f'fill="#FFFFFF" stroke="#C5CDD5"/>')
        partes.append(f'<text x="{x:.1f}" y="{y + 5:.1f}" '
                      f'text-anchor="middle" font-size="13" '
                      f'fill="#1F2933">{escape(texto)}</text>')

    for nombre, (x, y) in posiciones.items():
        partes.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="22" '
                      f'fill="#FFFFFF" stroke="#5B6770" stroke-width="3"/>')
        partes.append(f'<text x="{x:.1f}" y="{y + 6:.1f}" '
                      f'text-anchor="middle" font-size="18" '
                      f'font-weight="bold" fill="#1F2933">'
                      f'{escape(nombre)}</text>')

    partes.append("</svg>")
    return "\n".join(partes)
