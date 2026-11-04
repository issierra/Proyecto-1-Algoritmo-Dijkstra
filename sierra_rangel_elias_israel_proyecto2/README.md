# Proyecto 2: Persistencia, Archivos y Excepciones

Programa interactivo en Python que captura conexiones de una red de
transporte, las guarda en un archivo CSV, carga el grafo en memoria y
calcula la ruta más corta con el algoritmo de Dijkstra (Unidad 1).

**Autor:** Elias Israel Sierra Rangel

## Estructura

```
sierra_rangel_elias_israel_proyecto2/
├── main.py            # Programa principal interactivo
├── grafo.py           # Clases Nodo y Grafo (incluye Dijkstra)
├── io_handler.py      # Validación y lectura/escritura del CSV
├── nodos.csv          # Conexiones guardadas (Origen,Destino,Peso)
├── requirements.txt   # Dependencias de desarrollo (flake8)
└── README.md
```

## Requisitos

- Python 3.10 o superior
- flake8 (solo para revisar el estilo del código)

```bash
pip install -r requirements.txt
```

## Cómo ejecutarlo

Desde la carpeta del proyecto:

```bash
python main.py
```

El programa sigue estos pasos:

1. Pregunta si se desea agregar una conexión (origen, destino y peso).
   Si el dato es inválido, muestra un mensaje y vuelve a preguntar.
2. Guarda cada conexión validada al final de `nodos.csv`.
3. Lee `nodos.csv` fila por fila y construye el grafo. Las filas con
   errores se omiten y se informa cuáles fueron.
4. Pide un nodo de inicio y uno de destino, y muestra la ruta más
   corta con su peso total.

## Formato del CSV

```
Origen,Destino,Peso
A,B,4
A,C,2
```

## Revisión de estilo

```bash
flake8
```

## Decisiones y supuestos

- El grafo no es dirigido: cada conexión se puede recorrer en ambos
  sentidos con el mismo peso.
- El peso debe ser un número mayor que cero (Dijkstra no admite pesos
  negativos).
- Los nombres de nodos distinguen mayúsculas de minúsculas (`A` y `a`
  son nodos distintos).
- Si una misma conexión se ingresa dos veces, el peso más reciente
  reemplaza al anterior.
- Un nodo no puede conectarse consigo mismo.
