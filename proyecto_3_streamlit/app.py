# Título: Interfaz web de rutas más cortas con Streamlit
# Nombre: Elias Israel Sierra Rangel
# Fecha: 15 de noviembre de 2026
# Descripción: App web para ver la red, registrar tramos y calcular rutas.

import pandas as pd
import streamlit as st

from grafo import Grafo
from io_handler import (RUTA_CSV, cargar_grafo, convierte_peso,
                        formatea_peso, guardar_conexion,
                        valida_nombre_nodo)

SIMBOLO_INFINITO = "∞"
SIN_ANTERIOR = "—"
MENSAJE_SIN_CSV = ("No se encontró nodos.csv. Se creará al registrar "
                   "la primera conexión.")


def carga_estado() -> None:
    """Carga el grafo desde nodos.csv una sola vez por sesión.

    El grafo, el número de filas omitidas y un posible aviso de carga se
    guardan en st.session_state para no volver a leer el disco cuando
    el usuario interactúa con la app.
    """
    # Si el grafo ya está en memoria, no se vuelve a leer el disco
    if "grafo" in st.session_state:
        return

    grafo = Grafo()
    omitidas = 0
    aviso = ""
    if not RUTA_CSV.exists():
        aviso = MENSAJE_SIN_CSV

    try:
        grafo, omitidas = cargar_grafo(RUTA_CSV)
    except FileNotFoundError:
        aviso = MENSAJE_SIN_CSV
    except (PermissionError, UnicodeDecodeError) as error:
        aviso = f"No se pudo leer nodos.csv: {error}"

    st.session_state["grafo"] = grafo
    st.session_state["omitidas"] = omitidas
    st.session_state["aviso_carga"] = aviso


def crea_tabla_red(grafo: Grafo) -> pd.DataFrame:
    """Convierte las conexiones del grafo en una tabla de pandas.

    Args:
        grafo: Grafo cargado en memoria.

    Returns:
        DataFrame con las columnas Origen, Destino y Peso.
    """
    filas = []
    for origen in sorted(grafo.nodos):
        nodo = grafo.nodos[origen]
        for destino in sorted(nodo.vecinos):
            # Cada conexión se guarda en ambos sentidos: se lista una vez
            if origen < destino:
                filas.append({"Origen": origen, "Destino": destino,
                              "Peso": nodo.vecinos[destino]})
    return pd.DataFrame(filas, columns=["Origen", "Destino", "Peso"])


def crea_tabla_dijkstra(distancias: dict[str, float],
                        anteriores: dict[str, str | None]) -> pd.DataFrame:
    """Arma la tabla de distancias mínimas y nodos previos.

    Args:
        distancias: Distancia mínima desde el inicio hasta cada nodo.
        anteriores: Nodo previo de cada nodo en su mejor camino.

    Returns:
        DataFrame con las columnas Nodo, Distancia y Anterior.
    """
    filas = []
    for nodo in sorted(distancias):
        if distancias[nodo] == float("inf"):
            distancia = SIMBOLO_INFINITO
        else:
            distancia = formatea_peso(float(distancias[nodo]))
        filas.append({"Nodo": nodo, "Distancia": distancia,
                      "Anterior": anteriores[nodo] or SIN_ANTERIOR})
    return pd.DataFrame(filas, columns=["Nodo", "Distancia", "Anterior"])


def calcula_ruta(grafo: Grafo, inicio_texto: str,
                 destino_texto: str) -> None:
    """Valida los nodos, ejecuta Dijkstra y guarda el resultado.

    El resultado queda en st.session_state para que siga visible
    aunque el usuario interactúe con otros elementos de la app.

    Args:
        grafo: Grafo cargado en memoria.
        inicio_texto: Texto escrito para el nodo de inicio.
        destino_texto: Texto escrito para el nodo de destino.
    """
    # Se descarta el resultado anterior antes de calcular uno nuevo
    st.session_state.pop("ultima_ruta", None)
    inicio = inicio_texto.strip()
    destino = destino_texto.strip()

    try:
        if not inicio or not destino:
            raise ValueError("Escribe el nodo de inicio y el de destino.")
        distancia, camino = grafo.dijkstra(inicio, destino)
        distancias, anteriores = grafo.calcular_distancias(inicio)
    except ValueError as error:
        st.error(str(error))
        return
    except KeyError as error:
        st.error(error.args[0])
        return

    st.session_state["ultima_ruta"] = {
        "inicio": inicio, "destino": destino, "distancia": distancia,
        "camino": camino, "distancias": distancias,
        "anteriores": anteriores}


def muestra_ruta(grafo: Grafo) -> None:
    """Dibuja la última ruta calculada, si existe.

    Args:
        grafo: Grafo cargado en memoria, usado para leer el peso de
            cada tramo de la ruta.
    """
    ruta = st.session_state.get("ultima_ruta")
    if ruta is None:
        return

    camino = ruta["camino"]
    if not camino:
        st.warning(f"No existe una ruta entre {ruta['inicio']} "
                   f"y {ruta['destino']}.")
    else:
        st.success("Ruta más corta: " + " → ".join(camino))
        columna_peso, columna_saltos = st.columns(2)
        columna_peso.metric("Peso total", formatea_peso(ruta["distancia"]))
        columna_saltos.metric("Saltos en la ruta", len(camino) - 1)

        st.subheader("Indicaciones")
        for numero, (origen, siguiente) in enumerate(
                zip(camino, camino[1:]), start=1):
            peso = grafo.nodos[origen].vecinos[siguiente]
            st.write(f"{numero}. De **{origen}** a **{siguiente}** "
                     f"(peso {formatea_peso(peso)})")

    # Detalle técnico del algoritmo, oculto hasta que el usuario lo pida
    with st.expander(f"Distancias de Dijkstra desde {ruta['inicio']}"):
        st.dataframe(
            crea_tabla_dijkstra(ruta["distancias"], ruta["anteriores"]),
            hide_index=True)


def registra_conexion(origen_texto: str, destino_texto: str,
                      peso_texto: str) -> None:
    """Valida una conexión nueva, la guarda en el CSV y en memoria.

    Args:
        origen_texto: Texto escrito para el nodo de origen.
        destino_texto: Texto escrito para el nodo de destino.
        peso_texto: Texto escrito para el peso de la conexión.
    """
    origen = origen_texto.strip()
    destino = destino_texto.strip()

    try:
        valida_nombre_nodo(origen)
        valida_nombre_nodo(destino)
        if origen == destino:
            raise ValueError("El origen y el destino deben ser distintos.")
        peso = convierte_peso(peso_texto)
    except ValueError as error:
        st.error(str(error))
        return

    try:
        guardar_conexion(origen, destino, peso)
    except OSError as error:
        st.error(f"No se pudo guardar en nodos.csv: {error}")
        return

    # Solo se actualiza la memoria si el guardado en disco tuvo éxito
    st.session_state["grafo"].agregar_conexion(origen, destino, peso)
    # Una conexión nueva puede cambiar la ruta: se descarta la guardada
    st.session_state.pop("ultima_ruta", None)
    st.success(f"Conexión {origen} - {destino} (peso "
               f"{formatea_peso(peso)}) guardada en nodos.csv.")


def main() -> None:
    """Dibuja la interfaz completa de la aplicación."""
    st.set_page_config(page_title="Rutas más cortas", layout="wide")
    st.title("Algoritmo de Dijkstra: Calculando la ruta más corta")
    st.caption("Dijkstra sobre la red guardada en nodos.csv.")

    carga_estado()
    grafo = st.session_state["grafo"]

    if st.session_state["aviso_carga"]:
        st.warning(st.session_state["aviso_carga"])
    if st.session_state["omitidas"]:
        st.warning(f"Se omitieron {st.session_state['omitidas']} filas "
                   "de nodos.csv por tener datos inválidos.")

    with st.sidebar:
        st.header("Agregar tramo")
        origen_nuevo = st.text_input("Nodo origen", key="origen_nuevo")
        destino_nuevo = st.text_input("Nodo destino", key="destino_nuevo")
        peso_nuevo = st.text_input("Peso (número mayor que 0)",
                                   key="peso_nuevo")
        if st.button("Guardar conexión", key="boton_registro"):
            registra_conexion(origen_nuevo, destino_nuevo, peso_nuevo)

    tab_ruta, tab_red = st.tabs(["Ruta más corta", "Red actual"])

    with tab_ruta:
        if grafo.nodos:
            st.caption("Nodos disponibles: " + ", ".join(sorted(grafo.nodos)))
        else:
            st.info("La red está vacía. Registra una conexión primero.")
        columna_inicio, columna_destino = st.columns(2)
        inicio = columna_inicio.text_input("Nodo de inicio",
                                           key="inicio_ruta")
        destino = columna_destino.text_input("Nodo de destino",
                                             key="destino_ruta")
        if st.button("Calcular ruta", key="boton_ruta"):
            calcula_ruta(grafo, inicio, destino)
        muestra_ruta(grafo)

    # Esta pestaña se dibuja al final para reflejar conexiones recién
    # guardadas en la misma ejecución
    with tab_red:
        tabla = crea_tabla_red(grafo)
        st.caption(f"{len(grafo.nodos)} nodos y {len(tabla)} conexiones.")
        st.dataframe(tabla, hide_index=True)


if __name__ == "__main__":
    main()
