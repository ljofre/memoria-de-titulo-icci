
import numpy as np
import scipy as sp


class path_bound(object):

    def __init__(self, vertices, segments):
        pass

    def max_len_path(self):
        pass

    def max_len_path_id():
        pass

    def refine(self):
        """agrega un nodo intermedio a entre los dos nodos vecinos que describan
        el mayor largo"""
        
    def update_vectices(new_vertices):
        """actualiza la posición de los nodos"""
        pass
    
"""
algoritmo
"""

def puntual_field(x,y):
    return x+y

solution = path_bound(vertices=[[0,0],[1,1],[1,0]], segments=[0,1,2,0])

#generaremos un campo de una fiente conocida, de una esfera de rario 1
empirical_field = [[1,2,3],[1,2,8]] 
#inicialmente es un triangulo, entonces se busca el triangulo que mejor se ajuste a los datos conocidos

solution, error = iterate_newton(solution, empiricial_field = empirical_field)

