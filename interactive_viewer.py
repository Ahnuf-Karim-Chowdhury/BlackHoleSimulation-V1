import numpy as np
import plotly.graph_objects as go
from physics.blackhole import BlackHole
from physics.objects import CelestialObject

class InteractiveViewer:
    def __init__(self):
        self.fig = go.Figure()
        self.setup_scene()
        
    def setup_scene(self):
        # Create black hole
        black_hole = BlackHole(mass=1e31)
        self.add_black_hole(black_hole)
        
        # Add some celestial objects
        objects = [
            CelestialObject(position=[-2, 0, -5], radius=0.5, color=[1, 0, 0]),
            CelestialObject(position=[2, 0, -5], radius=0.5, color=[0, 1, 0]),
            CelestialObject(position=[0, 3, -5], radius=0.5, color=[0, 0, 1])
        ]
        self.add_objects(objects)
        
        # Set up layout
        self.fig.update_layout(
            scene=dict(
                xaxis=dict(nticks=10, range=[-10,10]),
                yaxis=dict(nticks=10, range=[-10,10]),
                zaxis=dict(nticks=10, range=[-10,10]),
            ),
            width=800,
            height=600,
            margin=dict(r=20, l=10, b=10, t=10)
        )
    
    def add_black_hole(self, black_hole):
        # Create event horizon sphere
        self.fig.add_trace(
            go.Scatter3d(
                x=[black_hole.position[0]],
                y=[black_hole.position[1]],
                z=[black_hole.position[2]],
                mode='markers',
                marker=dict(
                    size=black_hole.schwarzschild_radius*50,  # Scale for visibility
                    color='black',
                    opacity=0.8
                ),
                name='Black Hole'
            )
        )
        
        # Add accretion disk (simplified)
        theta = np.linspace(0, 2*np.pi, 100)
        x = black_hole.position[0] + 3 * np.cos(theta)
        y = black_hole.position[1] + 3 * np.sin(theta)
        z = np.full_like(theta, black_hole.position[2])
        
        self.fig.add_trace(
            go.Scatter3d(
                x=x,
                y=y,
                z=z,
                mode='lines',
                line=dict(color='orange', width=3),
                name='Accretion Disk'
            )
        )
    
    def add_objects(self, objects):
        for obj in objects:
            self.fig.add_trace(
                go.Scatter3d(
                    x=[obj.position[0]],
                    y=[obj.position[1]],
                    z=[obj.position[2]],
                    mode='markers',
                    marker=dict(
                        size=obj.radius*20,  # Scale for visibility
                        color=obj.color,
                        opacity=0.8
                    ),
                    name=f'Object at {obj.position}'
                )
            )
    
    def show(self):
        self.fig.show()

if __name__ == "__main__":
    viewer = InteractiveViewer()
    viewer.show()