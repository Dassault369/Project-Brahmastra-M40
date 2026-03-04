# ==========================================
# PROJECT BRAHMASTRA-M40: MASTER SIMULATION
# Developed by: Dassault369 (Alfred KS)
# GitHub: https://github.com/Dassault369
# ==========================================

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# 1. ശാസ്ത്രീയമായ സജ്ജീകരണങ്ങൾ (Configuration)
v0 = 13600.0        # Mach 40 വേഗത (m/s)
initial_angle = 35.0 # വിക്ഷേപണ കോൺ
m = 1500.0          # മിസൈലിന്റെ ഭാരം (kg)
Cd = 0.15           # വായു പ്രതിരോധ ഗുണകം (Drag Coefficient)
A = 0.8             # മിസൈലിന്റെ മുൻഭാഗത്തെ വിസ്തീർണ്ണം (m^2)
dt = 0.1            # ഓരോ സെക്കൻഡിലെയും മാറ്റം
MAX_SAFE_TEMP = 25000 # AI ഇടപെടേണ്ട താപനില (Kelvin)

# തുടക്കത്തിലെ വേഗതയും സ്ഥാനവും
vx = v0 * np.cos(np.radians(initial_angle))
vy = v0 * np.sin(np.radians(initial_angle))
x, y = 0.0, 0.0
current_angle = initial_angle

# ഡാറ്റ സംഭരിക്കാനുള്ള ലിസ്റ്റുകൾ
x_pos, y_pos, temperatures, ai_log = [0], [0], [300], [0]

# 2. സിമുലേഷൻ ലൂപ്പ് (The Mission Engine)
while y >= 0:
    v = np.sqrt(vx**2 + vy**2)
    rho = 1.225 * np.exp(-y / 8500.0) # ഉയരം കൂടുമ്പോൾ വായു കുറയുന്നു
    drag = 0.5 * rho * v**2 * Cd * A
    
    # താപനില കണക്കാക്കുന്നു (Aerodynamic Heating)
    mach_number = v / 340
    temp = 300 * (1 + 0.18 * mach_number**2)
    
    # AI ഗവർണ്ണർ ലോജിക് (Decision Making)
    ai_active = 0
    if temp > MAX_SAFE_TEMP and y < 50000:
        current_angle += 0.5 # ചൂട് കുറയ്ക്കാൻ കൂടുതൽ ഉയരത്തിലേക്ക്
        v *= 0.98            # ഘർഷണം കുറയ്ക്കാൻ വേഗത അല്പം കുറയ്ക്കുന്നു
        vx = v * np.cos(np.radians(current_angle))
        vy = v * np.sin(np.radians(current_angle))
        ai_active = 1
    
    # ഫിസിക്സ് അപ്ഡേറ്റ് (Acceleration & Movement)
    ax = -(drag * (vx / v)) / m
    ay = -9.81 - (drag * (vy / v)) / m
    
    vx += ax * dt
    vy += ay * dt
    x += vx * dt
    y += vy * dt
    
    if y >= 0:
        x_pos.append(x / 1000) # km-ലേക്ക് മാറ്റുന്നു
        y_pos.append(y / 1000)
        temperatures.append(temp)
        ai_log.append(ai_active)

# 3. ഡാറ്റ സേവ് ചെയ്യുന്നു (CSV Export for GitHub)
df = pd.DataFrame({
    'Distance_km': x_pos, 
    'Altitude_km': y_pos, 
    'Temperature_K': temperatures,
    'AI_Active': ai_log
})
df.to_csv('Brahmastra_Mission_Data.csv', index=False)

# 4. റിസൾട്ട് ഗ്രാഫ് (Visualization)
plt.figure(figsize=(10, 6))
plt.plot(x_pos, y_pos, color='red', label='Flight Path (Brahmastra)')
plt.title("PROJECT BRAHMASTRA-M40: AI Guided Trajectory")
plt.xlabel("Distance (km)")
plt.ylabel("Altitude (km)")
plt.grid(True)
plt.legend()
plt.show()

print(f"Mission Data saved to CSV. Maximum Temperature: {max(temperatures):.2f} K")
