import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# --- PROJECT BRAHMASTRA: PHASE 8 (GLOBAL TRAJECTORY & SPHERICAL EARTH) ---

# 1. Constants & Physics Configuration
v0 = 13600.0          # Mach 40 speed (m/s)
initial_angle = 35.0  
m = 1500.0            # Missile mass (kg)
Cd = 0.15             # Drag coefficient
A = 0.8               # Cross-sectional area
dt = 0.1              # Time step
target_x = 2500.0     # 2500 km Target

# Earth Constants
R_EARTH = 6371000.0   # ഭൂമിയുടെ ആരം (meters)
G_SURFACE = 9.81      # ഉപരിതലത്തിലെ ഗുരുത്വാകർഷണം

# Initial Physics Setup
vx = v0 * np.cos(np.radians(initial_angle))
vy = v0 * np.sin(np.radians(initial_angle))
x, y = 0.0, 0.0
current_angle = initial_angle

# Data Logging
x_pos, y_pos, temperatures, gravity_log = [0], [0], [300], [G_SURFACE]

# 2. Advanced Simulation Loop
while y >= 0:
    v = np.sqrt(vx**2 + vy**2)
    dist_from_center = R_EARTH + y
    
    # Atmospheric Density (Altitude based)
    rho = 1.225 * np.exp(-y / 8500.0)
    drag = 0.5 * rho * v**2 * Cd * A
    
    # Heat calculation (Mach 40 Heating)
    temp = 300 * (1 + 0.18 * (v/340)**2)
    
    # --- GLOBAL PHYSICS LOGIC (NEW) ---
    # 1. Variable Gravity (ദൂരം കൂടുമ്പോൾ ഗുരുത്വാകർഷണം കുറയുന്നു)
    g_current = G_SURFACE * (R_EARTH / dist_from_center)**2
    
    # 2. Centrifugal Acceleration (അതിവേഗതയിൽ പുറത്തേക്ക് തെറിക്കുന്ന ബലം)
    a_centrifugal = (v**2) / dist_from_center
    
    # AI Governor & Stealth (Phase 6 Logic)
    if temp > 25000 and y < 50000:
        current_angle += 0.2
        vx = v * np.cos(np.radians(current_angle))
        vy = v * np.sin(np.radians(current_angle))

    # Physics Acceleration Update
    ax = -(drag * (vx / v)) / m
    # Gravity കേന്ദ്രത്തിലേക്ക് വലിക്കുന്നു, Centrifugal പുറത്തേക്ക് തള്ളുന്നു
    ay = a_centrifugal - g_current - (drag * (vy / v)) / m
    
    vx += ax * dt
    vy += ay * dt
    x += vx * dt
    y += vy * dt
    
    if y >= 0:
        x_pos.append(x / 1000)
        y_pos.append(y / 1000)
        temperatures.append(temp)
        gravity_log.append(g_current)

# 3. Final Result Visualization
fig, ax1 = plt.subplots(figsize=(12, 6))

ax1.set_xlabel('Distance from Launch (km)')
ax1.set_ylabel('Altitude (km)', color='tab:red')
ax1.plot(x_pos, y_pos, color='tab:red', label='Global Trajectory')
ax1.tick_params(axis='y', labelcolor='tab:red')
ax1.axvline(x=target_x, color='black', linestyle='--', label='Target Lock')

ax2 = ax1.twinx() 
ax2.set_ylabel('Gravity (m/s^2)', color='tab:blue')
ax2.plot(x_pos, gravity_log, color='tab:blue', linestyle=':', label='Variable Gravity')
ax2.tick_params(axis='y', labelcolor='tab:blue')

plt.title("PROJECT BRAHMASTRA v4.0: Global Spherical Earth Model")
fig.tight_layout()
plt.grid(True)
plt.show()

print(f"Final Analysis: Max Temp {max(temperatures):.1f}K | Target Impact at {x/1000:.2f}km")
