import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# --- PROJECT BRAHMASTRA: PHASE 9 (3D SPATIAL DYNAMICS) ---

# 1. Physics Setup (v4.0 base + Z-axis)
v0 = 13600.0          # Mach 40 speed
initial_pitch = 35.0  # Vertical angle
initial_yaw = 5.0     # Horizontal angle (പുതിയത്)
dt = 0.5              

# Initial Vectors
vx = v0 * np.cos(np.radians(initial_pitch)) * np.cos(np.radians(initial_yaw))
vy = v0 * np.sin(np.radians(initial_pitch))
vz = v0 * np.cos(np.radians(initial_pitch)) * np.sin(np.radians(initial_yaw))

x, y, z = 0.0, 0.0, 0.0
x_p, y_p, z_p = [0], [0], [0]

# 2. 3D Simulation Loop
while y >= 0:
    v = np.sqrt(vx**2 + vy**2 + vz**2)
    rho = 1.225 * np.exp(-y / 8500.0)
    drag = 0.5 * rho * v**2 * 0.15 * 0.8
    
    # Simple Physics Update
    ax = -(drag * (vx / v)) / 1500
    ay = -9.81 - (drag * (vy / v)) / 1500
    az = -(drag * (vz / v)) / 1500
    
    vx += ax * dt
    vy += ay * dt
    vz += az * dt
    
    x += vx * dt
    y += vy * dt
    z += vz * dt
    
    if y >= 0:
        x_p.append(x/1000)
        y_p.append(y/1000)
        z_p.append(z/1000)

# 3. 3D Plotting
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Trajectory Plot
ax.plot(x_p, z_p, y_p, label='3D Brahmastra Path', color='red', lw=2)

ax.set_title("PROJECT BRAHMASTRA v5.0: 3D Flight Simulation")
ax.set_xlabel("Downrange (km)")
ax.set_ylabel("Crossrange (km)")
ax.set_zlabel("Altitude (km)")
ax.legend()
plt.show()
