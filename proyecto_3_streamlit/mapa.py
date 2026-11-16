# Título: Dibujo esquemático de la red como mapa
# Nombre: Elias Israel Sierra Rangel
# Fecha: 16 de noviembre de 2026
# Descripción: Calcula posiciones y genera el SVG del mapa de la red.

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
        nombres: Nombres de los nodos del grafo.

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
        # Se empieza arriba (-90°) y se avanza en sentido horario
        angulo = -math.pi / 2 + 2 * math.pi * indice / len(nombres)
        posiciones[nombre] = (centro_x + radio_x * math.cos(angulo),
                              centro_y + radio_y * math.sin(angulo))
    return posiciones


PALETAS = {
    "Mapa": {
        "fondo": "#EDEAE3", "parque": "#D3E5C9", "calle": "#E3DFD5",
        "rio": "#B9D5EA", "via_borde": "#C4BFB2", "via_relleno": "#FFFFFF",
        "ruta_borde": "#1C4BB0", "ruta": "#2A62D9", "puntos": "#FFFFFF",
        "otro_fondo": "#FFFFFF", "otro_borde": "#CFCABD",
        "otro_texto": "#4A4F5C", "ruta_texto": "#FFFFFF",
        "medio_fondo": "#FFFFFF", "medio_texto": "#1C4BB0",
        "nodo_fondo": "#FFFFFF", "nodo_borde": "#8A8C94",
        "nodo_texto": "#1F2430", "inicio": "#1E8E5A", "destino": "#D92B2B",
        "icono": "#FFFFFF", "anillo": "#FFFFFF", "etiqueta": "#FFFFFF",
        "etiqueta_borde": "#CFCABD", "etiqueta_texto": "#1F2430",
        "brillo": False},
    "Satélite": {
        "fondo": "#0F1C1A", "parque": "#123324", "calle": "#162A27",
        "rio": "#0C2B43", "via_borde": "#1A2724", "via_relleno": "#55655F",
        "ruta_borde": "#0A5A4D", "ruta": "#3DF2D0", "puntos": "#0B2B26",
        "otro_fondo": "#1B2926", "otro_borde": "#4B5C57",
        "otro_texto": "#D5E0DC", "ruta_texto": "#052520",
        "medio_fondo": "#0F1C1A", "medio_texto": "#D8FFF7",
        "nodo_fondo": "#0F1C1A", "nodo_borde": "#6E9A91",
        "nodo_texto": "#E6F2EE", "inicio": "#2BD97C", "destino": "#FF6B6B",
        "icono": "#072B18", "anillo": "#0F1C1A", "etiqueta": "#0F1C1A",
        "etiqueta_borde": "#3A4C46", "etiqueta_texto": "#E6F2EE",
        "brillo": True},
}

# Dibujos de 24x24 de los íconos: casa (inicio) y pin (destino)
ICONO_INICIO = ('<path d="M3 11l9-8 9 8"/><path d="M5 10v10h14V10"/>'
                '<path d="M10 20v-6h4v6"/>')
ICONO_DESTINO = ('<path d="M12 21s7-6.2 7-11a7 7 0 1 0-14 0c0 4.8 7 '
                 '11 7 11z"/><circle cx="12" cy="10" r="2.5"/>')


def crea_linea(x1: float, y1: float, x2: float, y2: float,
               color: str, grosor: float, extra: str = "") -> str:
    """Devuelve el texto SVG de una línea redondeada entre dos puntos."""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" '
            f'y2="{y2:.1f}" stroke="{color}" stroke-width="{grosor}" '
            f'stroke-linecap="round" {extra}/>')


def crea_fondo(paleta: dict) -> list[str]:
    """Dibuja el fondo decorativo: parques, calles en cuadrícula y río.

    Es solo ambientación: no depende de los nodos del grafo.

    Args:
        paleta: Colores del modo de vista elegido.

    Returns:
        Lista de elementos SVG, del fondo hacia el frente.
    """
    partes = [f'<rect width="{ANCHO_MAPA}" height="{ALTO_MAPA}" rx="12" '
              f'fill="{paleta["fondo"]}"/>',
              f'<rect x="350" y="365" width="130" height="95" rx="10" '
              f'fill="{paleta["parque"]}"/>',
              f'<rect x="20" y="30" width="95" height="75" rx="10" '
              f'fill="{paleta["parque"]}"/>']
    for y in (60, 200, 335, 465):
        partes.append(crea_linea(-10, y, ANCHO_MAPA + 10, y,
                                 paleta["calle"], 6))
    for x in (45, 175, 345, 505):
        partes.append(crea_linea(x, -10, x, ALTO_MAPA + 10,
                                 paleta["calle"], 6))
    partes.append(f'<path d="M410 -10 C 460 70 560 55 670 15" fill="none" '
                  f'stroke="{paleta["rio"]}" stroke-width="26" '
                  f'stroke-linecap="round"/>')
    return partes


def crea_etiqueta(x: float, y: float, texto: str, ancho: float,
                  fondo: str, borde: str, color_texto: str,
                  tamano: int = 12) -> list[str]:
    """Dibuja una etiqueta redonda con texto centrado en (x, y)."""
    return [f'<rect x="{x - ancho / 2:.1f}" y="{y - 11:.1f}" '
            f'width="{ancho}" height="22" rx="11" fill="{fondo}" '
            f'stroke="{borde}"/>',
            f'<text x="{x:.1f}" y="{y + 4.5:.1f}" text-anchor="middle" '
            f'font-size="{tamano}" font-weight="bold" '
            f'fill="{color_texto}">{escape(texto)}</text>']


def crea_nodo(nombre: str, x: float, y: float, papel: str,
              paleta: dict) -> list[str]:
    """Dibuja un nodo según su papel en la ruta.

    Args:
        nombre: Nombre del nodo.
        x: Posición horizontal en el lienzo.
        y: Posición vertical en el lienzo.
        papel: "inicio", "destino", "medio" (dentro de la ruta) o "otro".
        paleta: Colores del modo de vista elegido.

    Returns:
        Lista de elementos SVG del nodo y, si es extremo, su ícono y
        su etiqueta.
    """
    if papel in ("inicio", "destino"):
        icono = ICONO_INICIO if papel == "inicio" else ICONO_DESTINO
        texto = f"{nombre} · {'Inicio' if papel == 'inicio' else 'Destino'}"
        # Si el nodo está muy abajo, la etiqueta va arriba para no tapar
        # la leyenda
        y_etiqueta = y - 38 if y > 400 else y + 38
        partes = [f'<circle cx="{x:.1f}" cy="{y:.1f}" r="20" '
                  f'fill="{paleta[papel]}" stroke="{paleta["anillo"]}" '
                  f'stroke-width="3"/>',
                  f'<g transform="translate({x - 10:.1f} {y - 10:.1f}) '
                  f'scale(0.8333)" fill="none" stroke="{paleta["icono"]}" '
                  f'stroke-width="2.3" stroke-linecap="round" '
                  f'stroke-linejoin="round">{icono}</g>']
        partes += crea_etiqueta(
            x, y_etiqueta, texto, 7 * len(texto) + 18,
            paleta["etiqueta"], paleta["etiqueta_borde"],
            paleta["etiqueta_texto"])
        return partes

    if papel == "medio":
        fondo, borde = paleta["medio_fondo"], paleta["ruta"]
        color_texto = paleta["medio_texto"]
    else:
        fondo, borde = paleta["nodo_fondo"], paleta["nodo_borde"]
        color_texto = paleta["nodo_texto"]
    # El círculo crece si el nombre es largo
    radio = max(16, 4.2 * len(nombre) + 4)
    return [f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{radio:.1f}" '
            f'fill="{fondo}" stroke="{borde}" stroke-width="3"/>',
            f'<text x="{x:.1f}" y="{y + 5:.1f}" text-anchor="middle" '
            f'font-size="14" font-weight="bold" fill="{color_texto}">'
            f'{escape(nombre)}</text>']


def crea_leyenda(paleta: dict) -> list[str]:
    """Dibuja la leyenda del mapa en la esquina inferior izquierda."""
    y = ALTO_MAPA - 24
    partes = [f'<rect x="16" y="{y - 16}" width="456" height="32" rx="16" '
              f'fill="{paleta["etiqueta"]}" fill-opacity="0.92" '
              f'stroke="{paleta["etiqueta_borde"]}"/>']
    for x, color in ((34, paleta["inicio"]), (104, paleta["destino"])):
        partes.append(f'<circle cx="{x}" cy="{y}" r="6" fill="{color}"/>')
    partes.append(crea_linea(182, y, 208, y, paleta["ruta"], 6))
    partes.append(crea_linea(322, y, 348, y, paleta["via_borde"], 9))
    partes.append(crea_linea(322, y, 348, y, paleta["via_relleno"], 5))
    for x, texto in ((46, "Inicio"), (116, "Destino"),
                     (216, "Ruta más corta"), (356, "Otras conexiones")):
        partes.append(f'<text x="{x}" y="{y + 4}" font-size="12" '
                      f'fill="{paleta["etiqueta_texto"]}">{texto}</text>')
    return partes


def crea_svg_mapa(grafo: Grafo, camino: list[str] | None = None,
                  modo: str = "Mapa") -> str:
    """Genera el SVG del mapa con fondo, red, ruta, nodos y leyenda.

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
              '</filter></defs>']
    partes += crea_fondo(paleta)

    vias = []
    rutas = []
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
                        rutas.append(crea_linea(
                            x1, y1, x2, y2, paleta["ruta"], 22,
                            'opacity="0.3" filter="url(#brillo)"'))
                    rutas.append(crea_linea(
                        x1, y1, x2, y2, paleta["ruta_borde"], 15))
                    rutas.append(crea_linea(
                        x1, y1, x2, y2, paleta["ruta"], 10))
                    rutas.append(crea_linea(
                        x1, y1, x2, y2, paleta["puntos"], 3,
                        'stroke-dasharray="0.1 14"'))
                else:
                    vias.append(crea_linea(
                        x1, y1, x2, y2, paleta["via_borde"], 13))
                    vias.append(crea_linea(
                        x1, y1, x2, y2, paleta["via_relleno"], 8))
                etiquetas.append(((x1 + x2) / 2, (y1 + y2) / 2,
                                  formatea_peso(peso), en_ruta))
    # Las rutas se dibujan después de las vías para quedar encima
    partes += vias + rutas

    # Los pesos van sobre las líneas, en una etiqueta en el punto medio
    for x, y, texto, en_ruta in etiquetas:
        ancho = 10 * len(texto) + 14
        if en_ruta:
            partes += crea_etiqueta(x, y, texto, ancho, paleta["ruta"],
                                    paleta["ruta"], paleta["ruta_texto"], 13)
        else:
            partes += crea_etiqueta(x, y, texto, ancho, paleta["otro_fondo"],
                                    paleta["otro_borde"],
                                    paleta["otro_texto"], 13)

    for nombre, (x, y) in posiciones.items():
        papel = "otro"
        if camino and nombre == camino[0]:
            papel = "inicio"
        elif camino and nombre == camino[-1]:
            papel = "destino"
        elif nombre in camino:
            papel = "medio"
        partes += crea_nodo(nombre, x, y, papel, paleta)

    partes += crea_leyenda(paleta)
    partes.append("</svg>")
    return "\n".join(partes)
