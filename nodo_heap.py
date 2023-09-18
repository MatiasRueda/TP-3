class Nodo_heap():
    def __init__(self, dato):
        self.dato = dato
    
    def obtener_valor(self):
        return self.dato
    
    def __lt__(self, other):
        return self.dato[0] < other.dato[0]
    
    def __gt__(self, other):
        return self.dato[0] > other.dato[0]

    def __eq__(self, other):
        return self.dato[0] == other.dato[0]
    
    def __str__(self):
        return str(self.dato[0])

    def __repr__(self):
        return str(self.dato[0])