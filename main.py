import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.integrate import solve_ivp
from IPython.display import display, Video

# constants

g = 9.80665 # m/s²
L = 1 # m
omega0 = 0.0 # initial angular velocity
theta0 = 0.8 # initial angle in radians

# define functions

def pendulum_eqn(t,y):
  theta, omega = y
  dtheta_dt = omega
  domega_dt = -(g/L)*np.sin(theta)
  return [dtheta_dt, domega_dt]

duration = 10                  
fps = 30                       
total_frames = duration * fps  

t_span = (0, duration)            
t_eval = np.linspace(0, duration, total_frames) 
initial_state = [theta0, omega0]


# integrating over time
solution = solve_ivp(pendulum_eqn, t_span, initial_state, t_eval = t_eval)
angles = solution.y[0]
times  = solution.t

# coordinates
y_coordinates = -L*np.cos(angles)
x_coordinates = L*np.sin(angles)

# plot and animaiton

fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(-L - 0.2, L + 0.2)
ax.set_ylim(-L - 0.2, 0.2)
ax.set_aspect('equal')
ax.grid(True, linestyle='--')
ax.set_title("Animated Simple Pendulum")

# visulas
rod_line, = ax.plot([], [], color='purple', linewidth=2)
bob_circle, = ax.plot([], [], marker='o', color='pink', markersize=15)

def init():

    rod_line.set_data([], [])
    bob_circle.set_data([], [])
    return rod_line, bob_circle

  
def update(frame):

    x = float(x_coordinates[frame].item())
    y = float(y_coordinates[frame].item())
    
    rod_line.set_data([0, x], [0, y])
    bob_circle.set_data([x], [y])
    return rod_line, bob_circle


anim = FuncAnimation(
    fig, update, frames=total_frames, init_func=init, blit=True, interval=int(1000/fps)
)
plt.close()
video_filename = 'pendulum.mp4'
anim.save(video_filename, writer='ffmpeg', fps=fps)

# show on the screen with the integrated player
display(Video(video_filename, embed=True, width=400, height=400))
