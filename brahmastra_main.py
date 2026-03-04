# PROJECT BRAHMASTRA-M40: Master Simulation
# Developed by: Dassault369 (Alfred KS)

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# 1. Configuration
v0 = 13600.0        # Mach 40 speed
angle = 35.0        
m = 1500.0          
Cd = 0.15           
A = 0.8             
dt = 0.1            
MAX_SAFE_TEMP = 25000 

# 2. Simulation Engine
vx, vy = v0 * np.cos(np.radians(angle)), v0 * np.sin(np.radians(angle))
x, y = 0.0, 0.0
x_pos, y_pos, temperatures = [0], [0], [300]

while y >= 0:
    v = np.sqrt(vx**2 + vy**2)
    rho = 1.225 * np.exp(-y / 8500.0)
    drag = 0.5 * rho * v**2 * Cd * A
    
    # AI Governor Logic
    temp = 300 * (1 + 0.18 * (v/340)**2)
    if temp > MAX_SAFE_TEMP and y < 50000:
        vx *= 0.98  # Speed reduction by AI
        vy += 2.0   # Altitude adjustment by AI
    
    # Update Physics
    ax, ay = -(drag * (vx / v)) / 1500.0, -9.81 - (drag * (vy / v)) / 1500.0
    vx, vy = vx + ax*dt, vy + ay*dt
    x, y = x + vx*dt, y + vy*dt
    
    if y >= 0:
        x_pos.append(x/1000); y_pos.append(y/1000); temperatures.append(temp)

# 3. Save Data
pd.DataFrame({'Dist_km': x_pos, 'Alt_km': y_pos, 'Temp_K': temperatures}).to_csv('Brahmastra_Data.csv', index=False)

# 4. Plotting
plt.plot(x_pos, y_pos, color='red')
plt.title("PROJECT BRAHMASTRA-M40")
plt.show()
