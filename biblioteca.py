from collections import deque
from funciones_aux import construir_recorrido

######################################
#              COMANDOS              # 
######################################

"""
Encuentra el camino minimo entre el vertice origen y el destino
En caso de que se encuentre devuelve una lista con el recorrido encontrado,
en caso contrario, devuelve None
"""
def camino(grafo, origen, destino):
    padres, orden = BFS(grafo, origen)
    if destino not in orden:
        return None;
    recorrido = construir_recorrido(origen, destino, padres)
    return recorrido;

"""
Cuenta los vertices que se encuentren a rango
Devuelve un numero con todos los vertices que se encuentren
a rango.
"""
def rango(grafo, origen, rango):
    contador = 0
    padres, ordenes = BFS(grafo, origen)
    for valor in ordenes.values():
        if (valor == int(rango)):
            contador += 1
    return contador

"""
Obtiene el camino minimo mas grande de todo el grafo.
Devuelve una lista con el recorrido. 
"""
def diametro(grafo):
    maximo = 0
    nuevo_padre = None 
    fin = ""
    inicio = ""
    for v in grafo.obtener_vertices():
        padre, orden = BFS(grafo, v)
        for pagina, valor in orden.items():
            if (valor > maximo):
                maximo = valor
                inicio = v
                fin = pagina
                nuevo_padre = padre
    recorrido = construir_recorrido(inicio, fin, nuevo_padre)
    return recorrido

"""
Arma un recorrido visitando el primer adyacente de cada vertice,
en caso de no tener adyacente se termina el recorrido, en caso de que se
hayan agregado 20 vertices entonces se termina el recorrido.
Devuelve el recorrido
"""
def navegacion(grafo, origen):
    contador = 1;
    adyacente = "";
    actual = origen;
    recorrido = [];
    limite = 21;
    recorrido.append(origen);
    while (contador != limite and len(grafo.adyacentes(actual, 1)) != 0):
        adyacente = grafo.adyacentes(actual, 1);
        recorrido.append(adyacente[0])
        contador += 1
        actual = adyacente[0]
    return recorrido;

"""
Busca un ciclo en el grafo que tenga tamanio que se le pase por parametro.
En caso de encontrar un camino devuelve una lista con el camino encontrado,
en caso contrario devuelve None.
"""
def ciclo(grafo, origen, tamanio):
    tamanio = int(tamanio)
    camino = []
    visitados = set()
    if recorrido(grafo, origen, visitados, camino, tamanio, origen):
        return camino;
    return None

"""
Verifica que se pueda crear un recorrido que sea un ciclo y que tenga el tamanio que se le pasa por parametro
en caso de que exista el recorrido que cumpla dichas condiciones devuelve True y el camino que se le pase por parametro
contendra el camino.
en caso que no se encuentre un camino, devuelve False.
"""
def recorrido(grafo, v, visitados, camino, tamanio, origen):
    visitados.add(v)
    camino.append(v)
    if (len(visitados) == tamanio) and (origen in grafo.adyacentes(v)):
        camino.append(origen)
        return True
    if (len(visitados) >= tamanio):
        visitados.remove(v)
        camino.pop()
        return False
    for w in grafo.adyacentes(v):
        if w not in visitados:
            if recorrido(grafo, w, visitados, camino, tamanio, origen):
                return True
    visitados.remove(v)
    camino.pop();
    return False

"""
Recorre el grafo desde el vertice origen que se le pase por parametro
Devuelve 2 diccionarios: 
- el primero tiene como claves a los vertices del grafo y tiene como 
valores a los vertices de donde vienen
- el segundo tiene como clave  a los vertices del grafo y tiene como 
valores la cantidad de aristas minimas que hay entre el vertice origen y el vertice
de la clave. 
"""
def BFS(grafo, origen):
    visitados = set()
    padres = {}
    orden = {}
    padres[origen] = None
    orden[origen] = 0
    visitados.add(origen)
    cola = deque()
    cola.append(origen)
    while (len(cola) != 0):
        v = cola.popleft()
        for w in grafo.adyacentes(v):
            if w not in visitados:
                padres[w] = v
                orden[w] = orden[v] + 1
                visitados.add(w)
                cola.append(w)
    return padres, orden

def obtener_incidentes(grafo):
    """
    Recibe un grafo y devuelve un diccionario donde cada clave es un vertice del grafo, y 
    cada valor es una lista con los vertices que apuntan a ese vertice.
    """
    incidentes = {}
    for v in grafo.obtener_vertices():
        for w in grafo.adyacentes(v):
            incidentes[w] = incidentes.get(w, []) + [v]
    return incidentes