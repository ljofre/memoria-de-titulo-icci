
import os
import unittest
from jedi.evaluate.iterable import unite
unittest.TestLoader.sortTestMethodsUsing = None

from seismic_source import importEvent, SeismicEvent, Source

root_dir = os.path.dirname(__file__)
file_name1 = os.path.join(root_dir,"./../../data-sets/1998_aug_09_21_49_22.4n3")
file_name2 = os.path.join(root_dir,"./../../data-sets/1998_aug_02_07_30_40.d5g")
file_name3 = os.path.join(root_dir,"./../../data-sets/1998_aug_07_16_24_33.i6b")

class TestSeismicFramework(unittest.TestCase):
    
    
    def test_event(self):
        e = SeismicEvent.evento(file_name1)
        estimation = Source.Source(e)
        src, error, rot, vec, val = estimation.source(numpoints=100, L=0.5, por = 0)
        src2, error2, rot2, vec2, val2 = estimation.source(numpoints=50, L=0.25, por = 0)
        
        assert(sum(rot[:, 1:4]**2) != 0.0)
        
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
        
        
        
        
        
    