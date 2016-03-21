from importEvent import *
import numpy as np
import pandas as pd
import scipy.signal as sig
import re
from Source import dateTime2Num


class evento(object):

    '''@summary: conjunto de atributos que representan un evento sismico,
    con todos los atributos en los set de datos standar definidos en
    el los documentos de Codelco
    
    Este objeto carga los atributos dinamicamente por lo que es
    posible que si el documento que carga esta modificado o es
    adulterado manualmente pueda obtener resultados desconocidos.

    '''

    def count(self):
        # retorna la cantidad de geofonos del evento
        return(len(self.seismograms))

    def doc2event(self, path):
        '''@precondition: El documento a leer debe tener datos correctos
        :param path: Ruta en donde se encuentra el archivo a leer

        '''

        # Abrir archivo del evento
        texto = open(path, 'r').read()

        # extraer todos los atributos del documento
        keyValuePatt = r'(\S+)[ ]+=[ ]+(.+)\n'
        atributos = re.findall(keyValuePatt, texto, 0)
        print "importado!"
        # eliminar el texto sobrante []{3}\(in user system:.*\)
        sob = '[ ]+\(in user system:.*\)'
        f = lambda x:re.sub(sob, '', x)
        atributos = map(lambda x:tuple(map(f, x)), atributos)

        # extraer la tabla con todas las mediciones de los geosensores
        pattNameValue = '(\d+)[ ]+(\d+):[ ]+(.+E.+)[ ]+(.+E.+)[ ]+(.+E.+)'
        med = re.findall(pattNameValue, texto)
        med = np.array(map(lambda x:map(float, x), med))

        # pasar las mediciones a una lista de mediciones correspondiente a cada
        # una de las mediciones de los geofonos

        Ng = int(med[-1, 0]) # numero de geosensores
        gssMedList = []

        # filtrar las mediciones para generar la lista
        for j in range(Ng + 1):
            gssMedList.append(med[med[:, 0] == j * 1.0, :])

        # agregamos al evento los atributos, el primer elemento de la
        # tupla es el nom del atributo, y el segundo elemento es el
        # val del atributo. De esta manera se agregan uno por uno los
        # atributos a el objeto evento.
        func = lambda x: geosensor(gssMedList[x])
        gss = map(func, range(Ng + 1))
        flag = 0
        g = 0
        for index, atrib in enumerate(atributos):
            nom, val = atrib
            if flag == 0:
                setattr(self, nom, str2Attrib(val))

            elif flag == 1 :
                setattr(gss[g], nom, str2Attrib(val))

                if (atributos[index - 2 ][0] == 'sensor_id') & (nom ==
                                                                'surface_station'):
                    g = g + 1

            if nom == 'best_location':
                flag = 1

        # agregar los geofonos al evento
        setattr(self, 'seismograms', gss)
        
    def __init__(self, path):
        # convertir el archivo a objeto python
        self.doc2event(path)
        
        # @warning: se requieren convertir las matrices y los atributos que
        # tienen puntos a arrays y a atributos de estructuras respectivamenente

        #convertimos todos los sismos a campos de desplazamiento
        
        acelerometers_id = [76, 82, 118, 126, 146, 147]
        
        
        #transformar todo a campo de desplazamiento
        for s in self.seismograms:
            
            #guardar los datos crudos para analisis posteriores
            s.raw_data = s.data
            # si es acelerometro
            if s.sensor_id in acelerometers_id:
                s.data = sig.detrend(np.cumsum(sig.detrend(np.cumsum(s.data[
                               :,2:5], axis=1), axis=1), axis=1), axis=1)    
            # si es velocimetro
            else:
                s.data = sig.detrend(np.cumsum(s.data[:, 2:5], axis=1), axis=1)
            
            timevector = s.timevector
            s.data = pd.DataFrame(s.data, index = timevector)
            s.raw_data = pd.DataFrame(s.raw_data[:,2:5], index = timevector)

class geosensor(object):
    '''
    Un objeto con los atributos asociados a un geofono
    '''

    def __init__(self, data):
        self.data = data

    @property
    def timevector(self):

        tt = dateTime2Num(self.t_time)
        tp = self.TriggerPosition
        hsr = self.hardware_sampling_rate
        L = len(self.data) 
        return tt + (np.arange(L) - tp) / hsr

class seismicSource(object):
    ''' 
    fuente sismica y sus atributos
    '''
    pass
