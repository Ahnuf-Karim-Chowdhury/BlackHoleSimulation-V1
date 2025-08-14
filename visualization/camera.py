import numpy as np
from math import sin, cos, radians

class Camera:
    def __init__(self, position=[0, 0, 5], target=[0, 0, 0], up=[0, 1, 0], fov=60):
        self.position = np.array(position, dtype=np.float64)
        self.target = np.array(target, dtype=np.float64)
        self.up = np.array(up, dtype=np.float64)
        self.fov = fov
        self.yaw = -90.0  # Horizontal rotation
        self.pitch = 0.0  # Vertical rotation
        self.update_vectors()
        
    def update_vectors(self):
        # Calculate new forward vector from yaw and pitch
        front = np.array([
            cos(radians(self.yaw)) * cos(radians(self.pitch)),
            sin(radians(self.pitch)),
            sin(radians(self.yaw)) * cos(radians(self.pitch))
        ])
        self.forward = front / np.linalg.norm(front)
        
        # Recalculate right and up vectors
        self.right = np.cross(self.forward, np.array([0, 1, 0]))
        self.right = self.right / np.linalg.norm(self.right)
        self.camera_up = np.cross(self.right, self.forward)
        
        # Update target position
        self.target = self.position + self.forward
    
    def rotate(self, yaw, pitch):
        self.yaw += yaw
        self.pitch = max(-89.0, min(89.0, self.pitch + pitch))
        self.update_vectors()
    
    def move(self, direction, speed):
        if direction == "FORWARD":
            self.position += self.forward * speed
        elif direction == "BACKWARD":
            self.position -= self.forward * speed
        elif direction == "LEFT":
            self.position -= self.right * speed
        elif direction == "RIGHT":
            self.position += self.right * speed
        self.target = self.position + self.forward
    
    def get_ray(self, u, v, width, height):
        aspect_ratio = width / height
        scale = np.tan(np.radians(self.fov * 0.5))
        
        x = (2 * (u + 0.5) / width - 1) * aspect_ratio * scale
        y = (1 - 2 * (v + 0.5) / height) * scale
        
        direction = (self.forward + x * self.right + y * self.camera_up)
        direction = direction / np.linalg.norm(direction)
        
        return self.position, direction