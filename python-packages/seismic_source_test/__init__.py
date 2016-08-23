#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import unittest

import numpy as np
import matplotlib.pylab as plt
from numpy import shape

unittest.TestLoader.sortTestMethodsUsing = None

from seismic_source import importEvent, SeismicEvent, Source
from seismic_source.Source import GreenKernel, dateTime2Num

root_dir = os.path.dirname(__file__)
file_name1 = os.path.join(root_dir,"./../../data-sets/1998_aug_09_21_49_22.4n3")
file_name2 = os.path.join(root_dir,"./../../data-sets/1998_aug_02_07_30_40.d5g")
file_name3 = os.path.join(root_dir,"./../../data-sets/1998_aug_07_16_24_33.i6b")

class TestSeismicFramework(unittest.TestCase):
    
    def set_up_sensor_from_source(self, g, src):
        pass
    def test_0_artificial_event(self):
        """probar el algoritmo para un sismo artificial"""
        
        #copiamos un evento real
        e = SeismicEvent.evento(file_name1)
        
        origin_time = dateTime2Num(e.origin_time)
        srctime = np.linspace(start = origin_time, stop = origin_time + 0.01, num = 70)
        srctime = np.reshape(srctime,(-1,1))
        
        src = np.zeros((70,3))
        src[10:25,0] = 10^(14)
        src[30:45,1] = 10^(14)
        src[50:65,2] = 10^(14)
        
        np.hstack((srctime, src))
        
        for g in e.geosensors:
            g.data = self.set_up_sensor_from_source(g, src)
        
        pass
    
    def test_1_time_interval(self):
        pass
    
    def test_2_green_kernel(self):
        """la funcion no retorna nada en el kernel de green cuando la funcion no
        contiene al cero
        """
        #evaluar la funcion de green para distintos intervalos de fuentes sismicas
        alpha = 5600
        beta = 3500
        numpoints = 50
        L = 0.5
        # valores conocidos en donde si se puede estimar la señal
        start = 22.139236
        end = 22.639236
        
        e = SeismicEvent.evento(file_name1)
        estimation = Source.Source(e)
        
        estimation2 = Source.Source(e)
        
        estimation.srcTime = np.linspace(start, end , numpoints)
        estimation2.srcTime = np.linspace(start - L, end + L, 3*numpoints - 2)
        
        event = estimation.event
        LocX, LocY, LocZ = (event.LocX, event.LocY, event.LocZ)
         
        for G in event.seismograms:
            
            R = (G.x_coord - LocX, G.y_coord - LocY, G.z_coord - LocZ)
            
            #un intervalo adecuado para cada sismograma
            srcTime = np.linspace(G.timevector[0] - np.linalg.norm(R)/beta, G.timevector[-1] - np.linalg.norm(R)/alpha, numpoints)
            t = G.timevector - srcTime[0]
            #assert(t[0] <= 0 <= t[-1])
            Gk = GreenKernel(R=R, time=t, alpha= 5600.0, beta= 3500.0, rho= 2700)
            plt.plot(t, Gk[0][0])
            plt.show()
            print "suma para el primer intervalo >>", (Gk**2).sum(), "¿contiene al cero? >> ", t[0] <= 0 <= t[-1]
            
            

        # existe una subsecuencia en el segundo vector que debe contener al primer
        # vector, este es conocido tiene el tripe de largo y el triple de puntos
        
        assert(estimation.srcTime[0] == estimation2.srcTime[numpoints-1])
        
    def test_event(self):
        e = SeismicEvent.evento(file_name1)
        estimation = Source.Source(e)
        src, error, rot, vec, val = estimation.source(numpoints=50, L=0.5, por = 1)
        src2, error2, rot2, vec2, val2 = estimation.source(numpoints=25, L=0.25, por = 0)
        
        #assert(sum(rot[:, 1:4]**2) != 0.0)
        
        return src, error, rot, vec, val, src2, error2, rot2, vec2, val2

    
    def test_import_event(self):
        """testear que la lista de id de los sismografos implicados en un evento sismico
        coincida con los reales"""
        real_sensor_id = []
        e = SeismicEvent.evento(file_name1)
        sensor_ids = [i.sensor_id for i in e.seismograms]
        e.count()
        return e
    
    def test_signal(self):
        """testear que la se~nal en python sea la que corresponde, hay algunos 
        parametros que se pueden utilizar para no usar la se~nal completa, como 
        por ejemplo, el promedio, la norma infitito"""
        
        e = SeismicEvent.evento(file_name2)
        
        seismograms = e.seismograms
        pass
    
    def test_second_event(self):
        """testea que el evento sismico coincida con el calculado en matlab"""
        e = SeismicEvent.evento(file_name1)
        estimation = Source.Source(e)
        src, error, rot, vec, val = estimation.source(numpoints=100, L=0.5, por = 0.1)
        return src, error, rot, vec, val
        
if __name__ == '__main__':
    unittest.main()
        
        
        
        
        
    