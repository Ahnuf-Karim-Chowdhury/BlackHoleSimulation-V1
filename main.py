import streamlit as st
from plotly_blackhole import BlackHoleVisualizer

st.title("Realistic Black Hole Visualization")

if st.button("Show Interactive Black Hole"):
    vis = BlackHoleVisualizer()
    st.plotly_chart(vis.fig, use_container_width=True)