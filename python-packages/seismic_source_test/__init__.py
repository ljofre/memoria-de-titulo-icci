
import os
import unittest
from seismic_source import importEvent, SeismicEvent, Source

root_dir = os.path.dirname(__file__)
file_name = os.path.join(root_dir,"./../../data-sets/1998_aug_09_21_49_22.4n3")
file_name2 = os.path.join(root_dir,"./../../data-sets/1998_aug_02_07_30_40.d5g")

class test_seismic(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def testImportEvent(self):
        """testear que la lista de id de los sismografos implicados en un evento sismico
        coincida con los reales"""
        real_sensor_id = []
        e = SeismicEvent.evento(file_name)
        
        sensor_ids = [i.sensor_id for i in e.seismograms]
        e.count()
        return e
    
    def testSignal(self):
        
        """testear que la se~nal en python sea la que corresponde, hay algunos 
        parametros que se pueden utilizar para no usar la se~nal completa, como 
        por ejemplo, el promedio, la norma infitito"""
        
        e = SeismicEvent.evento(file_name2)
        
        seismograms = e.seismograms
        pass
    
    def test_event(self):
        """testea que el evento sismico coincida con el calculado en matlab"""
        e = SeismicEvent.evento(file_name)
        src = Source.Source(e)
        src, error, rot, vec, val = src.source()
        

if __name__ == '__main__':
    unittest.main()
        
        
        
        
        
    