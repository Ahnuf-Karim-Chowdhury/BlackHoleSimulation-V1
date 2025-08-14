import streamlit as st
import numpy as np
from visualization.camera import Camera

class InteractionHandler:
    def __init__(self):
        self.last_mouse_pos = None
        self.rotation_speed = 0.1
        self.move_speed = 0.5
        
        if 'camera' not in st.session_state:
            st.session_state.camera = Camera()
        
    def handle_mouse_move(self, mouse_x, mouse_y):
        if self.last_mouse_pos:
            dx = mouse_x - self.last_mouse_pos[0]
            dy = mouse_y - self.last_mouse_pos[1]
            
            st.session_state.camera.rotate(-dx * self.rotation_speed, 
                                         dy * self.rotation_speed)
        
        self.last_mouse_pos = (mouse_x, mouse_y)
    
    def handle_key_press(self, key):
        if key == "w":
            st.session_state.camera.move("FORWARD", self.move_speed)
        elif key == "s":
            st.session_state.camera.move("BACKWARD", self.move_speed)
        elif key == "a":
            st.session_state.camera.move("LEFT", self.move_speed)
        elif key == "d":
            st.session_state.camera.move("RIGHT", self.move_speed)