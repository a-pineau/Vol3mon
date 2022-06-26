# importing required modules 
import matplotlib.pyplot as plt
from math import tan, cos, sin, radians, degrees
x0 = 303
y0 = 70.19304257163867
g = 0.3
h_range = 894
alpha = 1.2222481311630375
v = 16.278854985956542
vx = v*cos(alpha)
vy = v*sin(alpha)

def get_trajectory(x, x0, y0, v, alpha):
    return y0 - ((x - x0) * tan(alpha) - g * (x - x0)**2 / (2*v**2*cos(alpha)**2))

def get_yt(t, y0, vy, g):
    return y0 + vy * t - g * t**2 * 0.5

x_values = range(x0, h_range)    
y_values = [get_trajectory(x, x0, y0, v, alpha) for x in x_values]

# Plot 
plt.plot(x_values, y_values)

t_values = range(0, 100)
xt_values = [x0 + vx * t for t in t_values]
yt_values = [get_yt(t, y0, vy, g) for t in t_values]

# Plot 
plt.plot(xt_values, yt_values)

# saving the file - make sure you 
# use savefig() before show().
# plt.savefig('squares.png',bbox_inches='tight', pad_inches=0.025)
  
plt.show()
