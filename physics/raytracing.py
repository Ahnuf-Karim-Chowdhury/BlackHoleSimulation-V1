import numpy as np
from numba import njit, types
from numba.typed import List

class Ray:
    def __init__(self, origin, direction):
        """Ray class representing a ray with origin and direction vectors"""
        self.origin = np.array(origin, dtype=np.float64)
        self.direction = np.array(direction, dtype=np.float64)
        self.direction = self.direction / np.linalg.norm(self.direction)  # Normalize

# Numba-compatible object representation
object_dtype = np.dtype([
    ('position', np.float64, 3),
    ('radius', np.float64),
    ('color', np.float64, 3),
    ('emission', np.float64)
])

@njit
def trace_ray(ray_origin, ray_dir, objects_array, black_hole_pos, black_hole_mass, max_bounces=3):
    """Numba-compatible ray tracing function"""
    color = np.zeros(3)
    current_origin = ray_origin.copy()
    current_dir = ray_dir.copy()
    attenuation = 1.0
    rs = 2 * 6.67430e-11 * black_hole_mass / (299792458.0**2) if black_hole_mass > 0 else 0
    
    for _ in range(max_bounces):
        # Find closest intersection
        closest_t = np.inf
        closest_obj_idx = -1
        closest_normal = np.zeros(3)
        
        for i in range(len(objects_array)):
            obj = objects_array[i]
            oc = current_origin - obj['position']
            a = np.dot(current_dir, current_dir)
            b = 2.0 * np.dot(oc, current_dir)
            c = np.dot(oc, oc) - obj['radius']**2
            discriminant = b**2 - 4*a*c
            
            if discriminant < 0:
                continue
                
            t = (-b - np.sqrt(discriminant)) / (2.0 * a)
            if t < 0:
                t = (-b + np.sqrt(discriminant)) / (2.0 * a)
                if t < 0:
                    continue
            
            if t < closest_t:
                closest_t = t
                closest_obj_idx = i
                closest_normal = (current_origin + t*current_dir - obj['position']) / obj['radius']
        
        if closest_obj_idx == -1:
            # Sky color
            color += attenuation * np.array([0.1, 0.1, 0.3])
            break
        
        # Calculate lighting
        obj = objects_array[closest_obj_idx]
        hit_point = current_origin + closest_t * current_dir
        
        # Emission
        color += attenuation * obj['color'] * obj['emission']
        
        # Diffuse shading
        light_dir = np.array([1.0, 1.0, 1.0])
        light_dir = light_dir / np.sqrt(np.dot(light_dir, light_dir))
        diffuse = max(0.0, np.dot(closest_normal, light_dir))
        color += attenuation * obj['color'] * diffuse * 0.7
        
        # Prepare next bounce
        current_origin = hit_point + closest_normal * 1e-5
        current_dir = current_dir - 2 * np.dot(current_dir, closest_normal) * closest_normal
        attenuation *= 0.5
        
        # Gravitational lensing
        if black_hole_mass > 0:
            dir_to_bh = black_hole_pos - current_origin
            distance = np.sqrt(np.dot(dir_to_bh, dir_to_bh))
            influence = min(1.0, rs / distance)
            current_dir = current_dir * (1 - influence) + dir_to_bh * influence
            current_dir = current_dir / np.sqrt(np.dot(current_dir, current_dir))
    
    return np.clip(color, 0, 1)

def prepare_objects(objects):
    """Convert Python objects to Numba-compatible array"""
    objects_array = np.zeros(len(objects), dtype=object_dtype)
    for i, obj in enumerate(objects):
        objects_array[i]['position'] = obj.position
        objects_array[i]['radius'] = obj.radius
        objects_array[i]['color'] = obj.color
        objects_array[i]['emission'] = obj.emission
    return objects_array