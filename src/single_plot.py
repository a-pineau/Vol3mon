# importing required modules 
import matplotlib.pyplot as plt
from math import tan, cos, radians, degrees
x0 = 45
y0 = 0
g = 0.3
h_range = 835 
v = 15.620499351813308
alpha = 0.8760580505981935

x_values = range(x0, h_range)
def get_trajectory(x, x0, y0, v, alpha):
        return y0 + (x - x0) * tan(alpha) - g * (x - x0)**2 / (2*v**2*cos(alpha))
    
y_values = [get_trajectory(x, x0, y0, v, alpha) for x in x_values]

# plotting 
plt.plot(x_values, y_values)
plt.xlabel('X')
plt.ylabel('Y')
  
# saving the file.Make sure you 
# use savefig() before show().
# plt.savefig('squares.png',bbox_inches='tight', pad_inches=0.025)
  
plt.show()
