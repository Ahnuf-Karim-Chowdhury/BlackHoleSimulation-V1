import numpy as np
from PIL import Image
from tqdm import tqdm
import streamlit as st
from physics.raytracing import trace_ray, prepare_objects

class Renderer:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
    
    def render(self, objects, black_hole=None, camera=None, samples_per_pixel=1):
        if camera is None:
            from visualization.camera import Camera
            camera = Camera()
        
        objects_array = prepare_objects(objects)
        bh_pos = black_hole.position if black_hole else np.zeros(3)
        bh_mass = black_hole.mass if black_hole else 0.0
        
        image = np.zeros((self.height, self.width, 3), dtype=np.float32)
        
        for y in tqdm(range(self.height), desc="Rendering"):
            for x in range(self.width):
                color = np.zeros(3)
                for _ in range(samples_per_pixel):
                    u = x + np.random.rand()
                    v = y + np.random.rand()
                    ray_origin, ray_dir = camera.get_ray(u, v, self.width, self.height)
                    color += trace_ray(ray_origin, ray_dir, objects_array, bh_pos, bh_mass)
                image[y, x] = np.clip(color / samples_per_pixel, 0, 1)
        
        return (image * 255).astype(np.uint8)