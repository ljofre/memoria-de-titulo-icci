from numpy.linalg import *
from scipy import *
from scipy.linalg import *
from scipy.signal import detrend
from numpy import ndarray, fliplr, append
from numpy import reshape
from numpy.linalg import eig
import numpy as np
import re


class Source(object):
    
    def __init__(self, event):
        
        # sensor_id de los que son acelerometros
        
        acelerometers_id = [76, 82, 118, 126, 146, 147]
        
        self.event = event
            
    def reconstruction(self):
        """Reconstruye los sismogramas dada la fuente estimda"""
        G = GreenKernel(self.event.LocR, self.srcTime, self.event.alpha, self.event.beta, self.event.rho)
        dt = self.srcTime[1] - self.srcTime[0]
        
        #x = (conv(G[0,0,:]))*dt
        
    
    def source(self, numpoints=100, L=0.5, por=0.0, LocR=None, srcTime=None):
        event = self.event
        # precondiciones

        assert(0 <= por)
        
        assert(L > 0)
        
        assert(numpoints == int(numpoints))
    
        if LocR is None:
            LocX, LocY, LocZ = (event.LocX, event.LocY, event.LocZ)
        else:
            LocX, LocY, LocZ = LocR
            
        if srcTime is None:
            self.srcTime = dateTime2Num(event.origin_time) + linspace(-por * L, (1 - por) * L, numpoints)
        
        '''
        reconstruccion de la fuente
        :param event: objeto del tipo event
        :param numpoints=100: numero de la discretizacion de la fuente estimada
        :param L: Largo de la ventana de tiempo de la fuente entimada
        :param por: fraccion de tiempo antes del tiempo estimado por Codelco
        '''
        
        dt = self.srcTime[1] - self.srcTime[0]
        
        """
            se requiere resolver un sistema lineal del tipo A*alphas = U
        """
        A, U = ([], [])
    
        # agregar el campo de desplazamiento a el vector de respuesta
        # los id son los mismos!
        for gs in event.seismograms:
    
            # se agregan todas las dimensiones que mantienen mediciones validas
            
            data = gs.data.values
            
            if gs.X_enabled == 1:
                U = hstack((U, data[:, 0].T))
    
            if gs.Y_enabled == 1:
                U = hstack((U, data[:, 1].T))
    
            if gs.Z_enabled == 1:
                U = hstack((U, data[:, 2].T))
    
        for G in event.seismograms:
    
            # frecuencia de muestreo
            hsr = G.hardware_sampling_rate
    
            # la relacion dt*hsr > 1
            deltat = dt * hsr
            #assert dt * hsr <= 1 , 'Advertencia: el producto dt * hsr deberia ser mayor que 1'
    
            R = (G.x_coord - LocX, G.y_coord - LocY, G.z_coord - LocZ)
    
            # funcion de green
            # t = G.timevector - dateTime2Num(date=event.origin_time)
            t = G.timevector - self.srcTime[0]
            alpha = G.P_velocity
            beta = G.S_velocity
            rho = G.RockDensity
    
            Gk = GreenKernel(R=R, time=t, alpha=alpha, beta=beta, rho=rho)
            assert(not any(isnan(Gk[:])))
            # integracion de la funcion de Green
            dtdomain = t[1] - t[0]
    
            F = cumsum(Gk, axis=2) * dtdomain
            FF = zeros(shape(F))
    
            # matriz auxiliar en donde se almacenaran todas las convoluciones
            # producidas en un solo sensor.
            B = []
    
            for jj in xrange(numpoints):
                # para todo elemento de la base
                ii = xrange(size(F, 2))
    
                # indices para los saltos en la convolucion entre la base y la
                # funcion de Green
    
                tf = map(lambda I: int(max(I - floor(jj * deltat), 0)), ii)
                ti = map(lambda I: int(max(I - floor((jj + 1) * deltat), 0)), ii)
    
                # convolucion con respecto la base seleccionada
                FF[:, :, ii] = F[:, :, tf] - F[:, :, ti]
    
                # convolucion para un elemento de la base
                C = []
                if G.X_enabled:
                    if C == []:
                        C = FF[0, :, :].copy()
                    else:
                        C = hstack((C, FF[0, :, :].copy()))
                    assert(not any(isnan(C[:])))
                if G.Y_enabled:
                    if C == []:
                        C = FF[1, :, :].copy()
                    else:
                        C = hstack((C, FF[1, :, :].copy()))
                    assert(not any(isnan(C[:])))
                if G.Z_enabled:
                    if C == []:
                        C = FF[2, :, :].copy()
                    else:
                        C = hstack((C, FF[2, :, :].copy()))
                    assert(not any(isnan(C[:])))
    
                if B == []:
                    B = C.copy()
                else:
                    B = vstack((B, C.copy()))
    
            if A == []:
                A = B.copy()
            else:
                A = hstack((A, B.copy()))
    
        # @todo: minimizar la norma 1 para hacer la estimacion mas robusta
        # resolucion del sistema lineal que minimiza la suma de la norma 2 de error
        assert(not any(isnan(A[:])))
        #from scipy.sparse import csr_matrix
        #from scipy.sparse.linalg import lsqr
        #matrix = csr_matrix(A.T)
        # X = numpy.linalg.lstsq(A.T, U)[0]
        # regresion lineal
        if det(dot(A, A.T)) != 0:
            #invertible
            X = dot(dot(U, A.T), inv(dot(A, A.T)))
        else:
            #no invertible
            X = dot(dot(U, A.T), pinv(dot(A, A.T)))
    
        src = zip(self.srcTime.T,
                  X[range(0, 3 * numpoints, 3)].T,
                  X[range(1, 3 * numpoints, 3)].T,
                  X[range(2, 3 * numpoints, 3)].T
                  )
        # post condiciones
        assert(shape(src) == (numpoints, 4))
    
        # error de estimacion
        error = norm(U - dot(X, A), 2)
        src = array(src)
        rot, vec, val = _rotate(src)
    
        #condiciones necesarias de orden de los valores propios y las coordenadas de
        #la fuente
        order = sorted(range(3), key=lambda k:val[k])
        val = val[order]
    
        #assert(val[0] <= val[1] <= val[2])
        rot[:, 1:4] = rot[:, 1:4][:, order]
        
        assert(sum(rot[:, 1:4]**2) != 0.0)
        
        return(src, error, rot, vec, val)


def S_Kernel(R, time, alpha, beta, rho):

    '''
    :param R: posicion
    :param time: vector de tiempo uniformemente distribuido
    :param alpha: velocidad de la onda p
    :param beta: velocidad de la onda s
    :param rho: densidad del medio
    '''
    r = norm(R, 2)
    x, y, z = R

    dt = time[0] - time[1]

    c_3 = array(map(int, time > r / beta))

    assert(not any(isnan(c_3)))

    c_3 = append(diff(c_3[::-1])[::-1], 0)

    c_3 = c_3 / dt

    c_3 = c_3 / (4 * pi * rho * beta ** 2 * r)

    # Funcion de Green
    G = ndarray(shape=(3, 3, len(time)))

    assert(not any(isnan(c_3)))

    # evaluar la funcion de Green
    G[0, 0, :] = -((x * x) / (r ** 2) - 1) * c_3
    G[0, 1, :] = -((x * y) / (r ** 2)) * c_3
    G[0, 2, :] = -((x * z) / (r ** 2)) * c_3
    G[1, 0, :] = G[0, 1, :].copy()
    G[1, 1, :] = -((y * y) / (r ** 2) - 1) * c_3
    G[1, 2, :] = -((y * z) / (r ** 2)) * c_3
    G[2, 0, :] = G[0, 2, :].copy()
    G[2, 1, :] = G[1, 2, :].copy()
    G[2, 2, :] = -((z * z) / (r ** 2) - 1) * c_3

    assert(not any(isnan(G[:])))
    return G


def P_Kernel(R, time, alpha, beta, rho):

    '''
    :param R: posicion
    :param time: vector de tiempo uniformemente distribuido
    :param alpha: velocidad de la onda p
    :param beta: velocidad de la onda s
    :param rho: densidad del medio
    '''
    r = norm(R, 2)
    x, y, z = R

    dt = time[0] - time[1]

    c_2 = array(map(int, time > r / alpha))

    assert(not any(isnan(c_2)))

    c_2 = append(diff(c_2[::-1])[::-1], 0)

    c_2 = c_2 / dt

    c_2 = c_2 / (4 * pi * rho * alpha ** 2 * r ** 3)

    # Funcion de Green
    G = ndarray(shape=(3, 3, len(time)))

    assert(not any(isnan(c_2)))

    # evaluar la funcion de Green
    G[0, 0, :] = (x ** 2) * c_2
    G[0, 1, :] = (x * y) * c_2
    G[0, 2, :] = (x * z) * c_2
    G[1, 0, :] = G[0, 1, :].copy()
    G[1, 1, :] = (y ** 2) * c_2
    G[1, 2, :] = (y * z) * c_2
    G[2, 0, :] = G[0, 2, :].copy()
    G[2, 1, :] = G[1, 2, :].copy()
    G[2, 2, :] = (z ** 2) * c_2

    assert(not any(isnan(G[:])))
    return G


def GreenKernel(R, time, alpha, beta, rho):

    '''
    :param R: posicion
    :param time: vector de tiempo uniformemente distribuido
    :param alpha: velocidad de la onda p
    :param beta: velocidad de la onda s
    :param rho: densidad del medio
    '''
    r = norm(R, 2)
    x, y, z = R

    dt = time[0] - time[1]

    c_1 = array(map(int, logical_and(r / alpha < time, time < r / beta)))
    c_2 = array(map(int, time > r / alpha))
    c_3 = array(map(int, time > r / beta))

    assert(not any(isnan(c_1)))
    assert(not any(isnan(c_2)))
    assert(not any(isnan(c_3)))

    c_2 = append(diff(c_2[::-1])[::-1], 0)
    c_3 = append(diff(c_3[::-1])[::-1], 0)

    c_1 = logical_and(c_1, logical_not(c_2))
    c_1 = logical_and(c_1, logical_not(c_3))

    c_1 = time * c_1 / (4 * pi * rho * (r ** 3))

    c_2 = c_2 / dt
    c_3 = c_3 / dt

    c_2 = c_2 / (4 * pi * rho * alpha ** 2 * r ** 3)
    c_3 = c_3 / (4 * pi * rho * beta ** 2 * r)

    # Funcion de Green
    G = ndarray(shape=(3, 3, len(time)))

    assert(not any(isnan(c_1)))
    assert(not any(isnan(c_2)))
    assert(not any(isnan(c_3)))

    # evaluar la funcion de Green
    G[0, 0, :] = (3 * (x * x) / (r ** 2) - 1) * c_1 + (
        x ** 2) * c_2 - ((x * x) / (r ** 2) - 1) * c_3
    G[0, 1, :] = (3 * (x * y) / (r ** 2)) * c_1 + (
        x * y) * c_2 - ((x * y) / (r ** 2)) * c_3
    G[0, 2, :] = (3 * (x * z) / (r ** 2)) * c_1 + (
        x * z) * c_2 - ((x * z) / (r ** 2)) * c_3
    G[1, 0, :] = G[0, 1, :].copy()
    G[1, 1, :] = (3 * (y * y) / (r ** 2) - 1) * c_1 + (
        y ** 2) * c_2 - ((y * y) / (r ** 2) - 1) * c_3
    G[1, 2, :] = (3 * (y * z) / (r ** 2)) * c_1 + (
        y * z) * c_2 - ((y * z) / (r ** 2)) * c_3
    G[2, 0, :] = G[0, 2, :].copy()
    G[2, 1, :] = G[1, 2, :].copy()
    G[2, 2, :] = (3 * (z * z) / (r ** 2) - 1) * c_1 + (
        z ** 2) * c_2 - ((z * z) / (r ** 2) - 1) * c_3

    assert(not any(isnan(G[:])))
    return G


def dateTime2Num(date):
    '''
    Convierte el string de fecha en una unidad numerica de tiempo en milesimas
    de segundo
    :param date: String con la fecha tal como aparece en el documento de Codelco
    '''
    minute, seg, cen = re.findall(r'\w{3} \w{3}[ ]{1,2}\d{1,2} \d{2}:(\d{2}):(\d{2}).(\d{6}) \d{4}', date)[0]

    minute = int(minute) * 1.0
    seg = int(seg) * 1.0
    cen = int(cen) * 1.0

    return(seg + cen / 1000000)
    #return(minute * 60 + seg + cen / 1000000)


def _rotate(data):

    # valores y vectores propios
    covariance_matrix = cov(data[:, 1:4], rowvar=0)
    val, vec = eig(covariance_matrix)

    # verificar que la matriz sea simetrica y que el cambio de base produzca
    # covarianza cero entre las 3 se~nales retornar el cambio de dase
    rot = data.copy()
    rot[:, 1:4] = dot(data[:, 1:4], vec)
    return(rot, vec, val)
