# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 23:26:41 2016

@author: leonardojofre
"""

import os

from matplotlib import pylab as plt

from Source import Source
from seismic_source import SeismicEvent

direc = os.path.dirname(__file__)

file_name = os.path.join(direc,"./../../data-sets/1998_aug_09_21_49_22.4n3")

e = SeismicEvent.evento(file_name)

src = Source(e)

src.source(numpoints=100, L=0.5, por=0.09)

plt.plot(src[0])

plt.show()

