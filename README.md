# Proyecto 1: Algoritmo de Dijkstra
Implementación del algoritmo de Dijkstra en Python con Programación Orientada a Objetos. Encuentra el camino de mejor costo entre un nodo de origen y uno de destino en un grafo de 10 nodos (A a J) con conexiones ponderadas.

## Estructura del proyecto

```
.
├── dijkstra.py   # Clases Nodo y Grafo, algoritmo y ejemplo de ejecución
├── README.md
└── .gitignore
```

## Cómo funciona

- **`Nodo`**: representa un vértice. Guarda su nombre y un diccionario de vecinos con el peso de cada conexión (lista de adyacencia).
- **`Grafo`**: guarda todos los nodos y ofrece los métodos para construirlo y resolverlo.
  - `agregar_nodo(nombre)`: crea un nodo nuevo.
  - `agregar_conexion(origen, destino, peso)`: conecta dos nodos en ambos sentidos.
  - `dijkstra(inicio, destino)`: devuelve la distancia mínima y el camino.
  - `construir_camino(anteriores, actual)`: función recursiva que reconstruye el camino desde el destino hasta el origen.

### Idea del algoritmo

1. Todas las distancias empiezan en infinito, excepto la del origen, que es 0.
2. Se elige el nodo no visitado con menor distancia y se marca como visitado.
3. Para cada vecino se calcula la distancia pasando por ese nodo; si es menor a la conocida, se actualiza.
4. Se repite hasta llegar al destino o agotar los nodos alcanzables.
5. El camino se reconstruye con los nodos anteriores.

## Autor

Elias Israel Sierra Rangel
