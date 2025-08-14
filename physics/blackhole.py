import numpy as np
from scipy.integrate import solve_ivp

class BlackHole:
    def __init__(self, mass, position=[0, 0, 0]):
        self.mass = mass  # in kg
        self.position = np.array(position, dtype=np.float64)
        self.schwarzschild_radius = 2 * 6.67430e-11 * mass / (299792458.0**2)
    
    def geodesic_equation(self, t, y):
        """Schwarzschild geodesic equations for light rays"""
        r, phi, dr, dphi = y
        rs = self.schwarzschild_radius
        
        f = 1 - rs/r
        if r <= rs or f <= 0:
            return [0, 0, 0, 0]  # Inside event horizon
        
        d2r = - (rs/(2*r**2)) * f * (1/f)**2 \
              + (rs/(2*r**2*f)) * dr**2 \
              + (r - rs) * dphi**2
        
        d2phi = -2 * dr * dphi / r
        
        return [dr, dphi, d2r, d2phi]
    
    def bend_light(self, ray_origin, ray_direction, steps=100):
        """Calculate light bending due to gravity by solving geodesic equations"""
        # Convert to polar coordinates relative to black hole
        rel_pos = ray_origin - self.position
        r = np.linalg.norm(rel_pos)
        phi = np.arctan2(rel_pos[1], rel_pos[0])
        
        # Convert direction to polar components
        ray_dir = ray_direction / np.linalg.norm(ray_direction)
        dr = np.dot(ray_dir, rel_pos/r)
        dphi = (-ray_dir[0] * np.sin(phi) + ray_dir[1] * np.cos(phi)) / r
        
        # Solve geodesic equation
        sol = solve_ivp(self.geodesic_equation, [0, 10], 
                       [r, phi, dr, dphi], 
                       t_eval=np.linspace(0, 10, steps))
        
        # Get final direction
        final_r = sol.y[0, -1]
        final_phi = sol.y[1, -1]
        final_dir = np.array([
            np.cos(final_phi),
            np.sin(final_phi),
            0  # Simplified 2D version
        ])
        
        return final_dir