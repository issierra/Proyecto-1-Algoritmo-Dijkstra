"""
Título: Algoritmo de Dijkstra
Nombre completo: Elias Israel Sierra Rangel
Fecha de creación: 13 de octubre de 2026
Descripción: Implementación del algoritmo de Dijkstra en Python con POO
"""

class Nodo:
    # Representa un vértice del grafo con sus vecinos y pesos
    def __init__(self, nombre):
        self.nombre = nombre
        self.vecinos = {}  # Diccionario {nombre_vecino: peso}
 
 
class Grafo:
    # Representa el grafo completo mediante lista de adyacencia
    def __init__(self):
        self.nodos = {}  # Diccionario {nombre: objeto Nodo}
 
    def agregar_nodo(self, nombre):
        # Crea un nodo nuevo y lo guarda en el grafo
        self.nodos[nombre] = Nodo(nombre)
 
    def agregar_conexion(self, origen, destino, peso):
        # Conecta dos nodos en ambos sentidos con el mismo peso
        self.nodos[origen].vecinos[destino] = peso
        self.nodos[destino].vecinos[origen] = peso
 
    def construir_camino(self, anteriores, actual):
        # Función recursiva: reconstruye el camino desde el destino hasta el origen
        if actual is None:  # Caso base: se pasó del origen
            return []
        return self.construir_camino(anteriores, anteriores[actual]) + [actual]
 
    def dijkstra(self, inicio, destino):
        # Calcula la distancia mínima y el camino entre inicio y destino
        distancias = {}  # Menor costo conocido hasta cada nodo
        anteriores = {}  # Nodo previo de cada nodo en el mejor camino
        visitados = set()  # Nodos con costo ya definitivo
 
        # Inicializa todas las distancias en infinito y sin nodo previo
        for nombre in self.nodos:
            distancias[nombre] = float("inf")
            anteriores[nombre] = None
 
        # El origen cuesta 0 llegar a él
        distancias[inicio] = 0
 
        # Repite hasta visitar todos los nodos
        while len(visitados) < len(self.nodos):
            # Busca el nodo no visitado con menor distancia
            nodo_actual = None
            menor_distancia = float("inf")
 
            for nombre in self.nodos:
                if nombre not in visitados:
                    if distancias[nombre] < menor_distancia:
                        menor_distancia = distancias[nombre]
                        nodo_actual = nombre
 
            # Si no hay nodos alcanzables, termina
            if nodo_actual is None:
                break
 
            # Si se llegó al destino, termina
            if nodo_actual == destino:
                break
 
            # Marca el nodo actual como visitado
            visitados.add(nodo_actual)
 
            # Obtiene el objeto Nodo para revisar sus vecinos
            nodo = self.nodos[nodo_actual]
 
            # Relaja las aristas hacia cada vecino
            for vecino, peso in nodo.vecinos.items():
                nueva_distancia = distancias[nodo_actual] + peso
 
                # Actualiza solo si el nuevo trayecto es estrictamente más corto
                if nueva_distancia < distancias[vecino]:
                    distancias[vecino] = nueva_distancia
                    anteriores[vecino] = nodo_actual
 
        # Reconstruye el camino usando la función recursiva
        camino = self.construir_camino(anteriores, destino)
 
        # Devuelve la distancia total y el camino encontrado
        return distancias[destino], camino
 
 
# Crea el grafo
grafo = Grafo()
 
# Agrega los 10 nodos (A a J)
for letra in "ABCDEFGHIJ":
    grafo.agregar_nodo(letra)
 
# Define las conexiones con sus pesos
grafo.agregar_conexion("A", "B", 4)
grafo.agregar_conexion("A", "C", 2)
grafo.agregar_conexion("B", "C", 1)
grafo.agregar_conexion("B", "D", 5)
grafo.agregar_conexion("C", "E", 8)
grafo.agregar_conexion("C", "F", 10)
grafo.agregar_conexion("D", "E", 2)
grafo.agregar_conexion("D", "G", 6)
grafo.agregar_conexion("E", "F", 3)
grafo.agregar_conexion("E", "H", 5)
grafo.agregar_conexion("F", "I", 4)
grafo.agregar_conexion("G", "H", 3)
grafo.agregar_conexion("G", "J", 9)
grafo.agregar_conexion("H", "I", 2)
grafo.agregar_conexion("H", "J", 7)
grafo.agregar_conexion("I", "J", 3)
 
# Ejecuta Dijkstra de A a J
distancia, camino = grafo.dijkstra("A", "J")
 
# Muestra el resultado
print("Origen: A | Destino: J")
print("Distancia mínima:", distancia)
print("Camino:", " -> ".join(camino))