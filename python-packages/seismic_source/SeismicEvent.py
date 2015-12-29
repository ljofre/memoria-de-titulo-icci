from importEvent import *
import numpy
import re
from Source import dateTime2Num


class evento(object):
    '''
    @summary: conjunto de atributos que representan un evento sismico, con todos
    los atributos en los set de datos standar definidos en el los documentos de
    Codelco
    
    Este objeto carga los atributos dinamicamente por lo que es posible que si el
    documento que carga esta modificado o es adulterado manualmente pueda obtener
    resultados desconocidos.
    
    '''

    def __init__(self, path):
        # convertir el archivo a objeto python
        self = self.doc2event(path)

        # @warning: se requieren convertir las matrices y los atributos que
        # tienen puntos a arrays y a atributos de estructuras respectivamenente


    def count(self):
        # retorna la cantidad de geofonos del evento
        return(self.seismograms.length())

    def doc2event(self, path):
        '''
        @precondition: El documento a leer debe tener datos correctos
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
        med = numpy.array(map(lambda x:map(float, x), med))

        # pasar las mediciones a una lista de mediciones correspondiente a cada
        # una de las mediciones de los geofonos

        Ng = int(med[-1, 0]) # numero de geosensores
        gssMedList = []

        # filtrar las mediciones para generar la lista
        for j in range(Ng + 1):
            gssMedList.append(med[med[:, 0] == j * 1.0, :])

        # agregamos al evento los atributos, el primer elemento de la tupla es el
        # nom del atributo, y el segundo elemento es el val del atributo. De esta
        # manera se agregan uno por uno los atributos a el objeto evento.
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

                if (atributos[index - 2 ][0] == 'sensor_id') & (nom == 'surface_station'):
                    g = g + 1

            if nom == 'best_location':
                flag = 1

        # agregar los geofonos al evento
        setattr(self, 'seismograms', gss)

class geosensor(object):
    '''
    Un objeto con los atributos asociados a un geofono
    '''

    def __init__(self, data):
        self.data = data

    def plot(self , dim):
        import matplotlib.pyplot as plt

        plt.plot(self.data[:, dim + 2])
        plt.show()

    def timevector(self):

        tt = dateTime2Num(self.t_time)
        tp = self.TriggerPosition
        hsr = self.hardware_sampling_rate
        L = int(self.data[-1, 1])
        return(tt + (numpy.arange(L + 1) - tp) / hsr)

class seismicSource(object):
    ''' 
    fuente sismica y sus atributos
    '''
    pass
