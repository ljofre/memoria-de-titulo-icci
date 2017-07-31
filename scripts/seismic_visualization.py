import matplotlib.pylab as plt

import Source
from seismic_source import SeismicEvent

e = SeismicEvent.evento("../data-sets/2011_apr_10_07_52")
src = Source.Source(e)
n = 5
gs = e.seismograms[n]
st = e.seismograms[n].data

fig, axes = plt.subplots(nrows=3, ncols=1)

gs.data[0].plot(ax = axes[0])
gs.data[1].plot(ax = axes[1])
gs.data[2].plot(ax = axes[2])
