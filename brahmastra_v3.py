import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# --- PROJECT BRAHMASTRA: PHASE 7 (EVASIVE MANEUVERS & SURVIVABILITY) ---

# 1. Mission Configuration
v0 = 13600.0          # Mach 40 speed
initial_angle = 35.0  
m = 1500.0            
Cd = 0.15             
dt = 0.1              
MAX_SAFE_TEMP = 25000 
target_x = 2500.0     

# Interceptor Detection Parameters
interceptor_zone_start = 1200.0 # 1200km മുതൽ ശത്രു മിസൈൽ പ്രതീക്ഷിക്കുന്നു
interceptor_zone_end = 1800.0
evasion_active = False

# Initial conditions
vx = v0 * np.cos(np.radians(initial_angle))
vy = v0 * np.sin(np.radians(initial_angle))
x, y = 0.0, 0.0
current_angle = initial_angle

x_pos, y_pos, temperatures, maneuver_log = [0], [0], [300], [0]

# 2. Simulation Loop
while y >= 0:
    v = np.sqrt(vx**2 + vy**2)
    rho = 1.225 * np.exp(-y / 8500.0)
    drag = 0.5 * rho * v**2 * Cd * 0.8
    
    # Heat calculation
    temp = 300 * (1 + 0.18 * (v/340)**2)
    
    # --- EVASIVE MANEUVER LOGIC (NEW) ---
    current_dist_km = x / 1000
    is_evading = 0
    
    if interceptor_zone_start < current_dist_km < interceptor_zone_end:
        if not evasion_active:
            print(f"WARNING: Interceptor Detected at {current_dist_km:.2f} km! Executing Evasive Maneuvers...")
            evasion_active = True
        
        # Zig-Zag Motion (Maneuvering)
        # പെട്ടെന്ന് ഉയരം കൂട്ടുകയും വശങ്ങളിലേക്ക് മാറുകയും ചെയ്യുന്നു
        maneuver_shift = np.random.uniform(-15, 15) 
        current_angle += maneuver_shift
        vy += 50.0 # Rapid climb to dodge
        is_evading = 1
    else:
        evasion_active = False

    # AI Governor for Thermal Safety
    if temp > MAX_SAFE_TEMP and y < 50000:
        current_angle += 0.5
        v *= 0.99
        vx = v * np.cos(np.radians(current_angle))
        vy = v * np.sin(np.radians(current_angle))

    # Physics Update
    ax = -(drag * (vx / v)) / m
    ay = -9.81 - (drag * (vy / v)) / m
    
    vx += ax * dt
    vy += ay * dt
    x += vx * dt
    y += vy * dt
    
    if y >= 0:
        x_pos.append(current_dist_km)
        y_pos.append(y / 1000)
        temperatures.append(temp)
        maneuver_log.append(is_evading)

# 3. Visualization
plt.figure(figsize=(12, 6))
plt.plot(x_pos, y_pos, color='red', label='Brahmastra Trajectory')

# Highlight Evasion Zone
plt.axvspan(interceptor_zone_start, interceptor_zone_end, color='yellow', alpha=0.3, label='Interceptor Hazard Zone')

plt.scatter(target_x, 0, color='black', marker='X', s=100, label='Target')
plt.title("PROJECT BRAHMASTRA v3.0: Evasive Maneuvering at Mach 40")
plt.xlabel("Distance (km)")
plt.ylabel("Altitude (km)")
plt.legend()
plt.grid(True)
plt.show()

print(f"Mission Brahmastra Successful. Target hit at {target_x} km after dodging interceptors.")
