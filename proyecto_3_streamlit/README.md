# Interfaz web de rutas más cortas con Streamlit

Proyecto 3 de Programación III. Aplicación web que carga una red de
conexiones desde un archivo CSV, permite agregar tramos nuevos y calcula
la ruta más corta entre dos nodos con el algoritmo de Dijkstra.

**Autor:** Elias Israel Sierra Rangel
**Fecha:** 16 de noviembre de 2026

## Qué hace la aplicación

- **Ruta más corta:** el usuario escribe un nodo de inicio y uno de destino.
  La app muestra la ruta, el peso total, los saltos, las indicaciones tramo
  por tramo y, en un desplegable, la tabla de distancias de Dijkstra desde
  el nodo de inicio.
- **Agregar tramo** (barra lateral): registra una conexión nueva con su peso.
  Se guarda en `nodos.csv` y en memoria. Si la conexión ya existía, se
  actualiza su peso.
- **Red actual:** tabla con todas las conexiones de la red.
- **Mapa esquemático:** dibuja la red y resalta la ruta calculada, con
  el inicio en verde y el destino en rojo. Se puede cambiar entre la
  vista *Mapa* y la vista *Satélite*. Las posiciones de los nodos se
  reparten automáticamente en un círculo, así que **no son coordenadas
  reales**.

## Estructura del proyecto

| Archivo | Función |
|---|---|
| `app.py` | Interfaz de Streamlit: pestañas, formularios, tablas y mensajes. |
| `grafo.py` | Clases del grafo y el algoritmo de Dijkstra. |
| `io_handler.py` | Lectura y escritura de `nodos.csv` y validación de datos. |
| `mapa.py` | Posiciones de los nodos y generación del mapa en SVG. |
| `main.py` | Versión por consola del programa. |
| `nodos.csv` | Red guardada: una conexión por fila. |
| `.streamlit/config.toml` | Tema de color de la interfaz. |
| `requirements.txt` | Dependencias. |

## Requisitos e instalación

Se necesita Python 3.10 o superior (se desarrolló con Python 3.13).

```bash
git clone https://github.com/issierra/Proyecto-1-Algoritmo-Dijkstra.git
cd Proyecto-1-Algoritmo-Dijkstra/proyecto_3_streamlit
pip install -r requirements.txt
```

## Ejecución

Desde la carpeta `proyecto_3_streamlit`:

```bash
streamlit run app.py
```

Debe ejecutarse desde esa carpeta, porque Streamlit lee de ahí el tema
(`.streamlit/config.toml`). La versión por consola se ejecuta con
`python main.py`.

## Formato de `nodos.csv`
Origen,Destino,Peso
A,B,4
A,C,2
- Cada fila es una conexión **no dirigida**: sirve en ambos sentidos.
- El peso debe ser un número mayor que 0.
- Las filas con datos inválidos se omiten y la app avisa cuántas fueron.

## Manejo de errores

La app nunca muestra un traceback. Los errores se capturan con excepciones
específicas y se muestran con `st.error` o `st.warning`:

- Campos vacíos, nodos que no existen, pesos inválidos (vacío, texto,
  cero, negativo, `nan` o `inf`) y conexiones de un nodo consigo mismo.
- Ruta inexistente entre dos nodos (`st.warning`).
- `nodos.csv` ausente, vacío, con filas inválidas, que no está en UTF-8
  o que no se puede escribir.

La conexión nueva solo se agrega a la memoria si el guardado en disco
tuvo éxito.

## Decisiones de diseño

- El CSV se lee **una sola vez por sesión** y el grafo se conserva en
  `st.session_state`.
- La última ruta calculada también se guarda en `st.session_state`, así
  que cambiar de vista del mapa no la borra. Se descarta al registrar una
  conexión nueva, porque podría cambiar la ruta más corta.
- `app.py` solo dibuja la interfaz; la lógica del grafo y del archivo
  vive en `grafo.py` e `io_handler.py`.

## Mejoras futuras

- Editar y eliminar nodos y conexiones desde la interfaz.
- Cargar posiciones reales de los nodos en lugar de repartirlos en círculo.
- Pruebas automáticas del grafo y de la lectura del CSV.