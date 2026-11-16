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


PALETAS = {
    "Mapa": {
        "fondo": "#EEF2F5", "linea": "#9AA5B1", "etiqueta": "#FFFFFF",
        "borde_etiqueta": "#C5CDD5", "texto": "#1F2933",
        "nodo": "#FFFFFF", "borde_nodo": "#5B6770", "ruta": "#2A62D9",
        "inicio": "#1E8E5A", "destino": "#D92B2B", "brillo": False},
    "Satélite": {
        "fondo": "#0F1C1A", "linea": "#37524D", "etiqueta": "#16302C",
        "borde_etiqueta": "#37524D", "texto": "#E6F4F1",
        "nodo": "#16302C", "borde_nodo": "#6E9A91", "ruta": "#3DF2D0",
        "inicio": "#4ADE80", "destino": "#FF6B6B", "brillo": True},
}


def crea_linea(x1: float, y1: float, x2: float, y2: float,
               color: str, grosor: int, extra: str = "") -> str:
    """Devuelve el texto SVG de una línea redondeada entre dos puntos."""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" '
            f'y2="{y2:.1f}" stroke="{color}" stroke-width="{grosor}" '
            f'stroke-linecap="round" {extra}/>')


def crea_svg_mapa(grafo: Grafo, camino: list[str] | None = None,
                  modo: str = "Mapa") -> str:
    """Genera el SVG del mapa con nodos, conexiones y pesos.

    Args:
        grafo: Grafo cargado en memoria.
        camino: Nodos de la ruta a resaltar, en orden. Si es None o está
            vacío, solo se dibuja la red.
        modo: Nombre de la paleta de colores: "Mapa" o "Satélite".

    Returns:
        Texto con el SVG completo, listo para mostrarse en una página.
    """
    paleta = PALETAS[modo]
    camino = camino or []
    # frozenset hace que el tramo A-B sea igual al B-A
    tramos_ruta = {frozenset(par) for par in zip(camino, camino[1:])}
    posiciones = calcula_posiciones(list(grafo.nodos))
    partes = [f'<svg xmlns="http://www.w3.org/2000/svg" '
              f'viewBox="0 0 {ANCHO_MAPA} {ALTO_MAPA}" '
              f'width="100%" height="100%" font-family="sans-serif">',
              '<defs><filter id="brillo" x="-20%" y="-20%" width="140%" '
              'height="140%"><feGaussianBlur stdDeviation="6"/>'
              '</filter></defs>',
              f'<rect width="{ANCHO_MAPA}" height="{ALTO_MAPA}" '
              f'rx="12" fill="{paleta["fondo"]}"/>']

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
                if en_ruta:
                    # En modo satélite, un trazo borroso simula el brillo
                    if paleta["brillo"]:
                        lineas_ruta.append(crea_linea(
                            x1, y1, x2, y2, paleta["ruta"], 16,
                            'opacity="0.6" filter="url(#brillo)"'))
                    lineas_ruta.append(
                        crea_linea(x1, y1, x2, y2, paleta["ruta"], 8))
                else:
                    lineas_red.append(
                        crea_linea(x1, y1, x2, y2, paleta["linea"], 5))
                etiquetas.append(((x1 + x2) / 2, (y1 + y2) / 2,
                                  formatea_peso(peso), en_ruta))
    # Las líneas de la ruta se dibujan después para quedar encima
    partes += lineas_red + lineas_ruta

    # Los pesos van sobre las líneas, en una etiqueta en el punto medio
    for x, y, texto, en_ruta in etiquetas:
        ancho = 10 * len(texto) + 14
        borde = paleta["ruta"] if en_ruta else paleta["borde_etiqueta"]
        color_texto = paleta["ruta"] if en_ruta else paleta["texto"]
        partes.append(f'<rect x="{x - ancho / 2:.1f}" y="{y - 11:.1f}" '
                      f'width="{ancho}" height="22" rx="11" '
                      f'fill="{paleta["etiqueta"]}" stroke="{borde}" '
                      f'stroke-width="2"/>')
        partes.append(f'<text x="{x:.1f}" y="{y + 5:.1f}" '
                      f'text-anchor="middle" font-size="13" '
                      f'font-weight="bold" fill="{color_texto}">'
                      f'{escape(texto)}</text>')

    for nombre, (x, y) in posiciones.items():
        relleno = paleta["nodo"]
        borde = paleta["borde_nodo"]
        color_texto = paleta["texto"]
        if camino and nombre == camino[0]:
            relleno = borde = paleta["inicio"]
            color_texto = "#0F1C1A" if paleta["brillo"] else "#FFFFFF"
        elif camino and nombre == camino[-1]:
            relleno = borde = paleta["destino"]
            color_texto = "#0F1C1A" if paleta["brillo"] else "#FFFFFF"
        elif nombre in camino:
            borde = paleta["ruta"]
        partes.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="22" '
                      f'fill="{relleno}" stroke="{borde}" '
                      f'stroke-width="3"/>')
        partes.append(f'<text x="{x:.1f}" y="{y + 6:.1f}" '
                      f'text-anchor="middle" font-size="18" '
                      f'font-weight="bold" fill="{color_texto}">'
                      f'{escape(nombre)}</text>')

    partes.append("</svg>")
    return "\n".join(partes)
