# importing required modules 
import matplotlib.pyplot as plt
from math import (tan, cos, sin, acos, atan, atan2,
                  pi, sqrt, radians, degrees)
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

# 115.01689347810004
x0 = 957.0725106519561
xf = 500
h = 75
g = 0.3
v =15.71128872705285 

def predict_angle(xf, h, g, v):
    try:
        c1 = (g*(xf-x0)**2/v**2 - h) / sqrt(h**2 + (xf-x0)**2)
        c1 = acos(c1)
    except ValueError:
        print("Impossible to reach!")
        return False
    else:
        c2 = atan(abs((xf-x0))/h)
        angle = (c1 + c2) * 0.5
        print("best angle =", degrees(angle))
        print(cos(angle))
        return pi - angle if xf < x0 else angle

angle = predict_angle(xf, h, g, v)
print("cos =", cos(angle)*v, "sin =", sin(angle)*v)

# x_values = range(x0, h_range)    
# y_values = [get_trajectory(x, x0, y0, v, alpha) for x in x_values]

# Plot 
# plt.plot(x_values, y_values)

t_values = range(0, 100)
xt_values = [x0 + vx * t for t in t_values]
yt_values = [get_yt(t, y0, vy, g) for t in t_values]

# Plot 
# plt.plot(xt_values, yt_values)

# saving the file - make sure you 
# use savefig() before show().
# plt.savefig('squares.png',bbox_inches='tight', pad_inches=0.025)
  
plt.show()

def on_floor_ball_collision(self):
gameball = self.game.gameball # Sake of readability
bot = self.game.bot
if self.circle_2_circle_overlap(gameball):
    if self == self.game.bot:
        best_angle = gameball.predict_angle(
            gameball.pos.x, 
            bot.x_to_reach, 
            HEIGHT - gameball.pos.y - gameball.r, 
            0.3, 
            self.vel.magnitude())
        Dx = abs(d * cos(best_angle))
        best_spot = gameball.pos.x + Dx
        vx = gameball.vel.magnitude() * cos(best_angle)
        vy = gameball.vel.magnitude() * -sin(best_angle)
        gameball.vel.x, gameball.vel.y = vx, vy
        print("angle_c =", angle_c, "best angle =", degrees(best_angle), degrees(best_angle) - 90)
        print("best spot=", best_spot)