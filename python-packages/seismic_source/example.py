# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 23:26:41 2016

@author: leonardojofre
"""

import os
from seismic_source import SeismicEvent


dir = os.path.dirname(__file__)

file_name = os.path.join(dir,"./../../data-sets/2011_apr_10_07_52")
e = SeismicEvent.evento(file_name)