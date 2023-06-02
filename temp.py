import numpy as np
import matplotlib.pyplot as plt


number_of_points = 100
center = 60
scale = 5

x = np.linspace(0, 50, number_of_points)
# y = [y for y in np.sin(x)+np.random.normal(0, 1,200)]
# y = [y for y in 40 * np.sin(x)+60]
y = [y for y in 40 * np.sin(x)+ center +np.random.normal(0, scale ,number_of_points)]

plt.plot(x, y)
plt.show()