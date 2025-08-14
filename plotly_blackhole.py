import numpy as np
import plotly.graph_objects as go
from matplotlib import cm

class BlackHoleVisualizer:
    def __init__(self, mass=10, position=[0, 0, 0]):
        self.fig = go.Figure()
        self.mass = mass * 2e30  # Convert to kg
        self.position = np.array(position)
        self.rs = 2 * 6.67430e-11 * self.mass / (299792458.0**2)
        self.rs *= 1e9  # Artificial scale-up for visibility
        self.setup_visualization()

    def setup_visualization(self):
        self.add_event_horizon()
        self.add_glow_shell()
        self.add_photon_ring()
        self.add_accretion_disk()
        self.add_gravitational_lensing()

        self.fig.update_layout(
            scene=dict(
                xaxis=dict(visible=False, range=[-15*self.rs, 15*self.rs]),
                yaxis=dict(visible=False, range=[-15*self.rs, 15*self.rs]),
                zaxis=dict(visible=False, range=[-15*self.rs, 15*self.rs]),
                aspectratio=dict(x=1, y=1, z=1),
                camera=dict(
                    eye=dict(x=0, y=-3*self.rs, z=0.5*self.rs),
                    up=dict(x=0, y=0, z=1)
                ),
                bgcolor='black'
            ),
            margin=dict(l=0, r=0, b=0, t=0),
            paper_bgcolor='black',
            plot_bgcolor='black'
        )

    def add_event_horizon(self):
        u, v = np.mgrid[0:2*np.pi:50j, 0:np.pi:25j]
        x = self.rs * np.cos(u)*np.sin(v)
        y = self.rs * np.sin(u)*np.sin(v)
        z = self.rs * np.cos(v)

        self.fig.add_trace(go.Surface(
            x=x+self.position[0],
            y=y+self.position[1],
            z=z+self.position[2],
            colorscale=[[0, 'black'], [1, '#111111']],
            showscale=False,
            opacity=0.95,
            hoverinfo='none'
        ))

    def add_glow_shell(self):
        glow_radius = 1.2 * self.rs
        u, v = np.mgrid[0:2*np.pi:60j, 0:np.pi:30j]
        xg = glow_radius * np.cos(u)*np.sin(v)
        yg = glow_radius * np.sin(u)*np.sin(v)
        zg = glow_radius * np.cos(v)

        self.fig.add_trace(go.Surface(
            x=xg+self.position[0],
            y=yg+self.position[1],
            z=zg+self.position[2],
            colorscale=[[0, 'rgba(255,140,0,0.1)'], [1, 'rgba(255,69,0,0.3)']],
            showscale=False,
            opacity=0.3,
            hoverinfo='none'
        ))

    def add_photon_ring(self):
        radius = 1.5 * self.rs
        theta = np.linspace(0, 2*np.pi, 300)
        x = radius * np.cos(theta) + self.position[0]
        y = radius * np.sin(theta) + self.position[1]
        z = 0.05 * self.rs * np.sin(3 * theta) + self.position[2]  # slight vertical ripple

        self.fig.add_trace(go.Scatter3d(
            x=x, y=y, z=z,
            mode='lines',
            line=dict(color='white', width=6),
            hoverinfo='none'
        ))

    def add_accretion_disk(self):
        inner_radius = 3 * self.rs
        outer_radius = 8 * self.rs
        radii = np.linspace(inner_radius, outer_radius, 40)

        for r in radii:
            theta = np.linspace(0, 2*np.pi, 300)
            x = r * np.cos(theta) + self.position[0]
            y = r * np.sin(theta) + self.position[1]

            warp_factor = 1 - (inner_radius/r)**0.5
            z = 1.2 * self.rs * warp_factor * np.sin(2*theta)

            temp = 1 - (r - inner_radius)/(outer_radius - inner_radius)
            color = cm.inferno(temp)
            color_str = f'rgba({int(color[0]*255)},{int(color[1]*255)},{int(color[2]*255)},1.0)'

            self.fig.add_trace(go.Scatter3d(
                x=x, y=y, z=z+self.position[2],
                mode='lines',
                line=dict(color=color_str, width=8),
                hoverinfo='none'
            ))

    def add_gravitational_lensing(self):
        num_stars = 300
        angles = np.random.uniform(0, 2*np.pi, num_stars)
        distances = np.random.normal(loc=20*self.rs, scale=3*self.rs, size=num_stars)

        x = distances * np.cos(angles)
        y = distances * np.sin(angles)
        z = np.random.uniform(-15*self.rs, 15*self.rs, num_stars)

        def lens_position(pos):
            dir_to_bh = self.position - pos
            dist = np.linalg.norm(dir_to_bh)
            influence = min(0.95, (self.rs/dist)**2)
            return pos * (1 - influence) + self.position * influence

        lensed_positions = np.array([lens_position(np.array([x[i], y[i], z[i]])) 
                                  for i in range(num_stars)])

        self.fig.add_trace(go.Scatter3d(
            x=lensed_positions[:,0],
            y=lensed_positions[:,1],
            z=lensed_positions[:,2],
            mode='markers',
            marker=dict(
                size=3,
                color='white',
                opacity=0.7
            ),
            hoverinfo='none'
        ))

    def show(self):
        self.fig.show()
