"""
Título: Clases del grafo y algoritmo de Dijkstra
Nombre completo: Elias Israel Sierra Rangel
Fecha de creación: 2 de noviembre de 2026
Descripción: Clases Nodo y Grafo con el algoritmo de Dijkstra (POO).
"""


class Nodo:
    """Representa un vértice del grafo. Contiene sus vecinos y los pesos."""

    def __init__(self, nombre: str) -> None:
        """Crea un nodo sin conexiones.

        Args:
            nombre: Identificador del nodo (por ejemplo, "A").
        """
        self.nombre: str = nombre
        # Diccionario {nombre_vecino: peso}
        self.vecinos: dict[str, float] = {}


class Grafo:
    """Representa el grafo completo. Modela la red de transporte."""

    def __init__(self) -> None:
        """Crea un grafo vacío."""
        # Diccionario {nombre: objeto Nodo}
        self.nodos: dict[str, Nodo] = {}

    def agregar_nodo(self, nombre: str) -> None:
        """Crea un nodo nuevo si aún no existe en el grafo.

        Args:
            nombre: Identificador del nodo.
        """
        # La comprobación evita borrar las conexiones de un nodo existente
        if nombre not in self.nodos:
            self.nodos[nombre] = Nodo(nombre)

    def existe_nodo(self, nombre: str) -> bool:
        """Indica si un nodo ya existe en el grafo.

        Args:
            nombre: Identificador del nodo.

        Returns:
            True si el nodo existe, False si no.
        """
        return nombre in self.nodos

    def agregar_conexion(self, origen: str, destino: str,
                         peso: float) -> None:
        """Conecta dos nodos en ambos sentidos con el mismo peso.

        Si alguno de los nodos no existe, se crea automáticamente.
        Si la conexión ya existía, el nuevo peso la reemplaza.

        Args:
            origen: Nombre del primer nodo.
            destino: Nombre del segundo nodo.
            peso: Costo de la conexión.
        """
        self.agregar_nodo(origen)
        self.agregar_nodo(destino)
        self.nodos[origen].vecinos[destino] = peso
        self.nodos[destino].vecinos[origen] = peso

    def construir_camino(self, anteriores: dict[str, str | None],
                         actual: str | None) -> list[str]:
        """Reconstruye el camino desde el origen hasta el nodo actual.

        Es recursiva: retrocede por los nodos previos hasta pasarse
        del origen y arma la lista al regresar.

        Args:
            anteriores: Nodo previo de cada nodo en el mejor camino.
            actual: Nodo desde el que se retrocede.

        Returns:
            Lista de nombres de nodos, del origen al nodo actual.
        """
        if actual is None:  # Caso base: se pasó del origen
            return []
        return self.construir_camino(anteriores, anteriores[actual]) + [actual]

    def dijkstra(self, inicio: str,
                 destino: str) -> tuple[float, list[str]]:
        """Calcula la distancia mínima y el camino entre dos nodos.

        Args:
            inicio: Nodo de partida.
            destino: Nodo al que se quiere llegar.

        Returns:
            Tupla (distancia total, camino). Si el destino no es
            alcanzable, devuelve (inf, []).

        Raises:
            KeyError: Si inicio o destino no existen en el grafo.
        """
        for nombre in (inicio, destino):
            if nombre not in self.nodos:
                raise KeyError(f"El nodo '{nombre}' no existe en el grafo")

        distancias: dict[str, float] = {}  # Menor costo conocido
        anteriores: dict[str, str | None] = {}  # Nodo previo en el camino
        visitados: set[str] = set()  # Nodos con costo ya definitivo

        # Inicializa todas las distancias en infinito y sin nodo previo
        for nombre in self.nodos:
            distancias[nombre] = float("inf")
            anteriores[nombre] = None

        # Llegar al origen cuesta 0
        distancias[inicio] = 0

        # Repite hasta visitar todos los nodos
        while len(visitados) < len(self.nodos):
            # Busca el nodo no visitado con menor distancia
            nodo_actual: str | None = None
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

            visitados.add(nodo_actual)

            # Relaja las aristas hacia cada vecino
            nodo = self.nodos[nodo_actual]
            for vecino, peso in nodo.vecinos.items():
                nueva_distancia = distancias[nodo_actual] + peso

                # Actualiza solo si el trayecto es estrictamente más corto
                if nueva_distancia < distancias[vecino]:
                    distancias[vecino] = nueva_distancia
                    anteriores[vecino] = nodo_actual

        # Un destino con distancia infinita no tiene camino real
        if distancias[destino] == float("inf"):
            return distancias[destino], []

        camino = self.construir_camino(anteriores, destino)
        return distancias[destino], camino
