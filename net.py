from biblioteca import camino, rango, diametro, navegacion, ciclo, obtener_incidentes
from funciones_aux import chequear_parametros, top_k
from collections import deque, Counter

class Net():
    def __init__(self, grafo):
        self.grafo = grafo
        self.features = {}
        self.tam = len(grafo.obtener_vertices())
        for v in grafo.obtener_vertices():
            self.features[v] = {}
        self.cfc = None
        self.comandos = {
            "camino" : (camino, self.grafo, 2),
            "rango" : (rango, self.grafo, 2),
            "diametro" : (diametro, self.grafo, 0),
            "navegacion" : (navegacion, self.grafo, 1),
            "ciclo" : (ciclo, self.grafo, 2),
            "mas_importantes" : (self.mas_importantes, self, 1),
            "conectados" : (self.conectados, self, 1),
            "comunidad" : (self.comunidad, self, 1),
            "listar_operaciones" : (self.listar_operaciones, self, 0),
        }

    def ejecutar_comando(self, comando, parametros):
        funcion, objeto, cant_params = self.comandos[comando]
        parametros = parametros.split(",")
        if cant_params and not chequear_parametros(parametros, cant_params): return
        if objeto is self:
            return funcion(*parametros) if cant_params else funcion()
        return funcion(objeto, *parametros) if cant_params else funcion(objeto)

    def listar_operaciones(self):
        """
        Devuelve una lista con las operaciones que puede ejecutar la net
        """
        operaciones = []
        for cmd in self.comandos:
            if cmd != "listar_operaciones": operaciones.append(cmd)
        return operaciones

    def mas_importantes(self, k):
        """
        Recibe un parametro K
        y devuelve las K paginas mas importantes del net.
        """
        k = int(k)
        if not self.features[self.grafo.primer_vertice()].get("pagerank", False): self.calcular_pagerank()
        return top_k(self.features, "pagerank", k)

    def conectados(self, pagina):
        """
        Recibe una pagina
        y devuelve una lista con todas las paginas que pertenecen a la misma CFC de dicha pagina.
        """
        if pagina not in self.grafo.obtener_vertices():
            return
        if not self.features[pagina].get("conectados", False):
            visitados = set()
            apilados = set()
            todas_cfc = []
            orden = dict()
            mb = dict()
            pila = deque()
            orden_contador = [0]
            estructuras_aux = [visitados, apilados, todas_cfc, orden, mb, pila, orden_contador]
            for v in self.grafo.obtener_vertices():
                if v not in visitados:
                    self.componente_fuertemente_conexas(v, estructuras_aux)
            self.cfc = todas_cfc

        return self.cfc[self.features[pagina]["conectados"]]

    def comunidad(self, pagina):
        """
        Recibe una pagina 
        y devuelve una lista con las paginas que pertenecen a la misma comunidad de dicha pagina.
        """
        if pagina not in self.grafo.obtener_vertices():
            return
        if not self.features[pagina].get("comunidad", False): self.calcular_comunidad()
        return [x for x in self.grafo.obtener_vertices() if self.features[x]["comunidad"] == self.features[pagina]["comunidad"]]

    def calcular_pagerank(self):
        #algoritmo sacado de https://en.wikipedia.org/wiki/PageRank
        cant_iteraciones = 10
        d = 0.85
        for v in self.features.keys():
            self.features[v]["pagerank"] = 1/self.tam
        incidentes = obtener_incidentes(self.grafo)
        for _ in range(cant_iteraciones):
            for v in self.features.keys():
                self.features[v]["pagerank"] = (1-d)/self.tam + d*sum([self.features[x]["pagerank"] / ( len(self.grafo.adyacentes(x)) or self.tam ) for x in incidentes[v]])

    def componente_fuertemente_conexas(self, v, estructuras_aux):
        visitados, apilados, todas_cfc, orden, mb, pila, orden_contador = estructuras_aux
        visitados.add(v)
        orden[v] = orden_contador[0]
        mb[v] = orden[v]
        orden_contador[0] += 1
        pila.appendleft(v)
        apilados.add(v)

        for w in self.grafo.adyacentes(v):
            if w not in visitados:
                self.componente_fuertemente_conexas(w, estructuras_aux)
            if w in apilados:
                mb[v] = min(mb[v], mb[w])
            
        if orden[v] == mb[v] and len(pila) > 0:
            nueva_cfc = []
            while True:
                w = pila.popleft()
                self.features[w]["conectados"] = len(todas_cfc)
                apilados.remove(w)
                nueva_cfc.append(w)
                if w == v:
                    break
            
            todas_cfc.append(nueva_cfc)
        
    def calcular_comunidad(self):
        cant_iteraciones = 80
        for v in self.features.keys():
            self.features[v]["comunidad"] = v
        incidentes = obtener_incidentes(self.grafo)
        for _ in range(cant_iteraciones):
            for v in self.features.keys():
                self.features[v]["comunidad"] = Counter([self.features[x]["comunidad"] for x in incidentes[v]]).most_common(1)[0][0]