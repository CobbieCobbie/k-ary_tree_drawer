import streamlit as st
import tree_drawer as draw


def main():
    st.title("Tree Drawer")
    st.sidebar.title("Settings")
    st.sidebar.header("Tree Parameters")
    k = st.sidebar.number_input("Maximum amount of children for any vertex", 2, 10, 2)
    h = st.sidebar.number_input("Height of the k-ary tree", 1, 10, 3)
    integer = st.sidebar.checkbox("Place vertices on integer grid points by rounding the coordinates")
    logging = st.sidebar.checkbox("Enable / Disable a log of the graph drawn")
    color = st.sidebar.checkbox("Enable / Disable coloring of the vertices")
    if st.sidebar.button("Draw Tree"):
        figure = draw.draw(k, h, integer, logging, color)
        st.pyplot(figure)

if __name__ == "__main__":
    main()
