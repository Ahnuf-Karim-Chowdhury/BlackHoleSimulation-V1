# Initialize physics package
from .blackhole import BlackHole
from .objects import CelestialObject
from .raytracing import trace_ray, prepare_objects  # Removed Ray import


__all__ = ['BlackHole', 'CelestialObject', 'trace_ray', 'prepare_objects']  # Removed Ray