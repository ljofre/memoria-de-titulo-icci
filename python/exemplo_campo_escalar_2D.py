
import matplotlib.pyplot as plt
import numpy as np

t = np.arange(0, 2 * np.pi, 0.01)

x = np.cos(t) + 0.5 * np.sin(0.5 * t)
y = np.sin(t) + 0.5 * np.sin(0.5 * t)

plt.plot(x, y)
plt.show()
