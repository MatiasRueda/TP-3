#!/usr/bin/python3
import sys

from funciones_aux import chequear_entrada, leer_tsv
from net import Net
from grafo import Grafo
from procesar_salida import ejecutar_salida

sys.setrecursionlimit(100000)

def main():
    if not chequear_entrada(): return

    grafo_net = Grafo()
    leer_tsv(sys.argv[1], grafo_net)
    net = Net(grafo_net)

    for line in sys.stdin:
        tupla_cmd_params = line.strip().split(" ", 1)
        comando = tupla_cmd_params[0]
        if len(tupla_cmd_params) != 2:
            parametros = ""
        else:
            parametros = tupla_cmd_params[1]
        salida = net.ejecutar_comando(comando, parametros)

        ejecutar_salida(comando, salida)
    
main()