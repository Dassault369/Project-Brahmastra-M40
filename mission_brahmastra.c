#include <stdio.h>
#include <math.h>
#include <stdlib.h>

int main() {
    double v0 = 13600.0;         
    double initial_angle = 35.0; 
    double dt = 0.1;             
    double R_EARTH = 6371000.0;  

    double x = 0.0, y = 0.0;
    double rad = initial_angle * M_PI / 180.0;
    double vx = v0 * cos(rad);
    double vy = v0 * sin(rad);
    
    printf("--- MISSION BRAHMASTRA C-v2.0: EVASION ACTIVE ---\n");

    for (int step = 0; step < 3000; step++) {
        double v = sqrt(vx*vx + vy*vy);
        double dist_km = x / 1000.0;

        // Evasive Maneuver Logic
        if (dist_km > 1200.0 && dist_km < 1800.0) {
            if (step % 50 == 0) {
                printf("[ALERT] Interceptor Detected at %.2f km! Executing Evasion...\n", dist_km);
                vy += (rand() % 40) - 10; 
                vx += (rand() % 20) - 10;
            }
        }

        double g_current = 9.81 * pow(R_EARTH / (R_EARTH + y), 2);
        double ay = (v * v / (R_EARTH + y)) - g_current; 

        vx += 0; // Simplified ax
        vy += ay * dt;
        x += vx * dt;
        y += vy * dt;

        if (step % 400 == 0) {
            printf("Dist: %.2f km | Alt: %.2f km\n", dist_km, y/1000.0);
        }

        if (y < 0 && step > 10) break; 
    }

    printf("MISSION SUCCESS: Final Impact at %.2f km\n", x/1000.0);
    return 0;
}
