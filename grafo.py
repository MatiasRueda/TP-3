class Grafo():

    """
    Crea el grafo.
    Se le puede pasar por parametro si se quiere un grafo NO dirigido y 
    tambien se le puede pasar por parametro una lista de vertices.
    En caso de que no se le pase nada por parametros el grafo se 
    creara dirigido y sin ningun vertice al principio.  
    """

    def __init__(self, es_dirigido = True, vertices = None):
        self.grafo = {}
        self.dirigido = es_dirigido
        self.vertices = vertices
        if vertices != None:
            for v in vertices:
                self.agregar_vertices(v);

    """
    Devuelve una lista con todos los adyacentes del vertice.
    Se le puede pasar por parametro la cantidad de adyacentes que se quiere.
    En caso de que no se le pase nada por parametro devuelve todos los adyacentes
    en una lista.
    """
    def adyacentes(self, v, cant_ady = 0):
        adyacentes = []
        if v not in self.grafo:
            return adyacentes
        if (cant_ady):
            agregados = 0;
            for w in self.grafo[v].keys():
                adyacentes.append(w)
                agregados += 1
                if (agregados == cant_ady):
                    return adyacentes
        for w in self.grafo[v].keys():
            adyacentes.append(w)
        return adyacentes

    """
    Agrega un vertice al grafo, en caso de que el vertice ya pertenezca al grafo
    devuelve None.
    """

    def agregar_vertice(self, v):
        if v in self.grafo:
            return None;
        self.grafo[v] = self.grafo.get(v, {})

    """
    Agrega una arista al grafo.
    Se le puede pasar un peso por parametro, en caso de que no se le pase ningun peso
    este mismo sera de valor 1.
    """
    def agregar_arista(self, v, w, peso = 1):
        if v not in self.grafo:
            return None
        self.grafo[v][w] = peso
        if not self.dirigido:
            self.grafo[w] = self.grafo.get(w, {})
            self.grafo[w][v] = peso

    """
    Devuelve el valor del peso que hay entre 2 vertices, en caso de que alguno de los 
    vertices no pertenezca al grafo devuelve None.
    """

    def peso(self, v, w):
        if ((v not in self.grafo) or (w not in self.grafo[v])):
            return None;
        return self.grafo[v][w]

    """
    Devuelve en un lista los vertices del grafo.
    """

    def obtener_vertices(self):
        vertices = []
        for v in self.grafo.keys():
            vertices.append(v)
        return vertices

    """
    Devuelve el primer vertice del grafo
    """

    def primer_vertice(self):
        return list(self.grafo)[0]