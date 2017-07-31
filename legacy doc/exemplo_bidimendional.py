"""
Reconstrucción de una circunferencia que genera un campo gravitacional
"""


import numpy as np
from scipy.constants import G


# definimos la naturaleza del campo escalar que genera en el espacio cada
# elemento del area.
def F(x, y):
    return G / (np.sqrt(x ** 2 + y ** 2))


def distance(bounds):
    pass


class boundPath(object):

    def Jacobian(F):
        pass

    def __init__(number_of_points, constrainst):
        # condicion inicial
        x0 = np.array([[0, 0] for _ in range(nv)])
        pass

    def optimize(cache, puntual_field, empiricial_field):
        pass

    # generamos n puntos en el plano con distintos valores
    # positivos
n = 10
p = [(np.random.uniform() + 1, np.random.uniform() + 1)
     for _ in range(n)]

# buscamos que todos estos puntos estén a una distancia
# superior de 1 al origen

psi = [F(*i) for i in p]

# dado estos objetos se pueden identificar los bordes y sus vecinos, estos
# son los segmentos se deben iterarse hasta converger a la forma que
# minimiza el funcional

bound = boundPath(nv=3, constrainst=None)
relative_error = 1
while relative_error > 0.05:
    bound.optimize(puntual_field=F, empiricial_field=psi)
    path0 = bound.path
    bound.addPoint(bound.best_new_point)
    bound.optimize(puntual_field=F, empiricial_field=psi)
    path1 = bound.path
    relative_error = distance(bounds=(path0, path1))
