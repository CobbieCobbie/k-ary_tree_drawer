import streamlit as st
import plotly.graph_objects as go
import content.draw_support as draw_support
import matplotlib.pyplot as plt
import content.tree_drawer as tree_drawer

if __name__ == "__main__":
    st.write("Hello World")
    tree_drawer.draw(2, 3, False, False, False)
    st.pyplot(fig)