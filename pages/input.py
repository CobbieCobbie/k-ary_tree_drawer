import streamlit as st
import content.tree_drawer as draw


def main():
    st.title("Parameter Input for the drawing algorithm")
    st.header("Tree Parameters")
    st.session_state['k'] = st.number_input("Maximum amount of children for any vertex", 2, 10, 2)
    st.session_state['h'] = st.number_input("Height of the k-ary tree", 1, 10, 3)
    st.session_state['integer'] = st.checkbox("Place vertices on integer grid points by rounding the coordinates")
    st.session_state['logging'] = st.checkbox("Enable / Disable a log of the graph drawn")
    st.session_state['color'] = st.checkbox("Enable / Disable coloring of the vertices")
    start_drawing = st.button("Draw Tree", on_click=get_drawing())
    if start_drawing:
        st.success("The drawing has been cached and can be viewed in the \"result\" tab.")



@st.cache_resource
def get_drawing():
    drawing = draw.draw(
        st.session_state['k'], 
        st.session_state['h'], 
        st.session_state['integer'], 
        st.session_state['logging'], 
        st.session_state['color']
    )
    return drawing


if __name__ == "__main__":
    main()
