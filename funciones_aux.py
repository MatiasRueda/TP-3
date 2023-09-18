from nodo_heap import Nodo_heap
import heapq
import csv
import sys

##############
# AUXILIARES #
##############
"""
Construye un recorrido que parte desde el origen hasta destino.
Devuelve una lista con el recorrido ya construido.
"""
def construir_recorrido(origen, destino, padres):
    recorrido = []
    aux = destino
    while aux != origen:
        recorrido.append(aux)
        aux = padres[aux]
    recorrido.append(origen)
    recorrido.reverse()
    return recorrido

def top_k(dicc, feature, k):
    """
    Recibe un diccionario de diccionarios, donde el segundo diccionario contiene features de los elementos del primero,
    y devuelve el top K de los elementos cuya feature sea mayor.
    """
    top_k = []
    for x in dicc.keys():
        if len(top_k) < k:
            nodo = Nodo_heap((dicc[x][feature], x))
            heapq.heappush(top_k, nodo)
        else:
            if top_k[0].obtener_valor()[0] < dicc[x][feature]:
                heapq.heappop(top_k)
                nodo = Nodo_heap((dicc[x][feature], x))
                heapq.heappush(top_k, nodo)
    top_k.sort(reverse=True)
    return [x.obtener_valor()[1] for x in top_k]

def leer_tsv(tsv_file, grafo):
    with open(tsv_file) as f:
        archivo = csv.reader(f, delimiter="\t")

        for linea in archivo:
            origen = linea[0]
            grafo.agregar_vertice(origen)
            for destino in linea[1:]:
                grafo.agregar_arista(origen, destino)

def chequear_parametros(parametros, i):
    return True if len(parametros) == i else False

def chequear_entrada():
    cant_entrada = len(sys.argv)
    if cant_entrada != 2:
        print("ERROR: Debes ingresar 1 (y solo 1) archivo de entrada")
        return False
    return True