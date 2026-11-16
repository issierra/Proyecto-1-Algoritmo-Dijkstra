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
COLOR_RUTA = "#2A62D9"
COLOR_INICIO = "#1E8E5A"
COLOR_DESTINO = "#D92B2B"


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


def crea_svg_mapa(grafo: Grafo, camino: list[str] | None = None) -> str:
    """Genera el SVG del mapa con nodos, conexiones y pesos.

    Args:
        grafo: Grafo cargado en memoria.
        camino: Nodos de la ruta a resaltar, en orden. Si es None o está
            vacío, solo se dibuja la red.

    Returns:
        Texto con el SVG completo, listo para mostrarse en una página.
    """
    camino = camino or []
    # frozenset hace que el tramo A-B sea igual al B-A
    tramos_ruta = {frozenset(par) for par in zip(camino, camino[1:])}
    posiciones = calcula_posiciones(list(grafo.nodos))
    partes = [f'<svg xmlns="http://www.w3.org/2000/svg" '
              f'viewBox="0 0 {ANCHO_MAPA} {ALTO_MAPA}" '
              f'width="100%" height="100%" font-family="sans-serif">',
              f'<rect width="{ANCHO_MAPA}" height="{ALTO_MAPA}" '
              f'rx="12" fill="#EEF2F5"/>']

    lineas_red = []
    lineas_ruta = []
    etiquetas = []
    for origen in sorted(grafo.nodos):
        for destino, peso in sorted(grafo.nodos[origen].vecinos.items()):
            # Cada conexión se guarda en ambos sentidos: se dibuja una vez
            if origen < destino:
                x1, y1 = posiciones[origen]
                x2, y2 = posiciones[destino]
                en_ruta = frozenset((origen, destino)) in tramos_ruta
                color = COLOR_RUTA if en_ruta else "#9AA5B1"
                grosor = 8 if en_ruta else 5
                linea = (f'<line x1="{x1:.1f}" y1="{y1:.1f}" '
                         f'x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" '
                         f'stroke-width="{grosor}" stroke-linecap="round"/>')
                # Las líneas de la ruta se dibujan después para quedar encima
                (lineas_ruta if en_ruta else lineas_red).append(linea)
                etiquetas.append(((x1 + x2) / 2, (y1 + y2) / 2,
                                  formatea_peso(peso), en_ruta))
    partes += lineas_red + lineas_ruta

    # Los pesos van sobre las líneas, en una etiqueta en el punto medio
    for x, y, texto, en_ruta in etiquetas:
        ancho = 10 * len(texto) + 14
        borde = COLOR_RUTA if en_ruta else "#C5CDD5"
        color_texto = COLOR_RUTA if en_ruta else "#1F2933"
        partes.append(f'<rect x="{x - ancho / 2:.1f}" y="{y - 11:.1f}" '
                      f'width="{ancho}" height="22" rx="11" '
                      f'fill="#FFFFFF" stroke="{borde}" stroke-width="2"/>')
        partes.append(f'<text x="{x:.1f}" y="{y + 5:.1f}" '
                      f'text-anchor="middle" font-size="13" '
                      f'font-weight="bold" fill="{color_texto}">'
                      f'{escape(texto)}</text>')

    for nombre, (x, y) in posiciones.items():
        relleno, borde, color_texto = "#FFFFFF", "#5B6770", "#1F2933"
        if camino and nombre == camino[0]:
            relleno = borde = COLOR_INICIO
            color_texto = "#FFFFFF"
        elif camino and nombre == camino[-1]:
            relleno = borde = COLOR_DESTINO
            color_texto = "#FFFFFF"
        elif nombre in camino:
            borde = COLOR_RUTA
        partes.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="22" '
                      f'fill="{relleno}" stroke="{borde}" '
                      f'stroke-width="3"/>')
        partes.append(f'<text x="{x:.1f}" y="{y + 6:.1f}" '
                      f'text-anchor="middle" font-size="18" '
                      f'font-weight="bold" fill="{color_texto}">'
                      f'{escape(nombre)}</text>')

    partes.append("</svg>")
    return "\n".join(partes)
