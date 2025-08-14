import numpy as np

class CelestialObject:
    def __init__(self, position, radius, color, emission=0.0):
        self.position = np.array(position, dtype=np.float64)
        self.radius = radius
        self.color = np.array(color, dtype=np.float64)
        self.emission = emission  # Light emission strength
    
    def intersect(self, ray_origin, ray_direction):
        """Check if ray intersects with this object"""
        oc = ray_origin - self.position
        a = np.dot(ray_direction, ray_direction)
        b = 2.0 * np.dot(oc, ray_direction)
        c = np.dot(oc, oc) - self.radius**2
        discriminant = b**2 - 4*a*c
        
        if discriminant < 0:
            return None  # No intersection
        
        t = (-b - np.sqrt(discriminant)) / (2.0 * a)
        if t < 0:
            t = (-b + np.sqrt(discriminant)) / (2.0 * a)
            if t < 0:
                return None  # Intersection behind ray origin
        
        return t
    
    def normal_at(self, point):
        """Calculate surface normal at a point"""
        return (point - self.position) / self.radius