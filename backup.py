import streamlit as st
from interactive_viewer import InteractiveViewer

def main():
    st.title("Interactive 3D Black Hole")
    
    if st.button("Show Interactive Simulation"):
        viewer = InteractiveViewer()
        st.plotly_chart(viewer.fig, use_container_width=True)

if __name__ == "__main__":
    main()