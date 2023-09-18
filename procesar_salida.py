def imprimir_lista(lista, separador):
    print("{}".format(separador.join(lista) ))

def imprimir_costo(lista):
    print("Costo: {}".format(len(lista) - 1))

# Contiene un diccionario donde cada clave es el comando a la funcion de net
#y el valor es una lista de tuplas que especifica la funcion de salida que tiene que ejecutar 
func_salida = {
    "camino" : [(imprimir_lista, " -> "), (imprimir_costo,)],
    "rango" : [(print,)],
    "diametro" : [(imprimir_lista, " -> "), (imprimir_costo,)],
    "navegacion" : [(imprimir_lista, " -> ")],
    "ciclo" : [(imprimir_lista, " -> ")],
    "mas_importantes" : [(imprimir_lista, ", ")],
    "conectados" : [(imprimir_lista, ", ")],
    "comunidad" : [(imprimir_lista, ", ")],
    "listar_operaciones" : [(imprimir_lista, "\n")],
}

mensaje_error = {
    "camino" : "No se encontro recorrido",
    "ciclo" : "No se encontro recorrido",
}

def ejecutar_salida(comando, salida):
    if salida is None:
        print(mensaje_error[comando])
        return
    for paquete in func_salida[comando]:
        func = paquete[0]
        params = paquete[1:]
        if not params:
            func(salida)
        else:
            func(salida, *params)