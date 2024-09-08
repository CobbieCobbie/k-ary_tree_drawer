import streamlit as st
import content.tree_drawer as draw


def main():
    st.title("Tree Drawer")
    st.sidebar.title("Settings")
    st.sidebar.header("Tree Parameters")
    st.session_state['k'] = st.sidebar.number_input("Maximum amount of children for any vertex", 2, 10, 2)
    st.session_state['h'] = st.sidebar.number_input("Height of the k-ary tree", 1, 10, 3)
    st.session_state['integer'] = st.sidebar.checkbox("Place vertices on integer grid points by rounding the coordinates")
    st.session_state['logging'] = st.sidebar.checkbox("Enable / Disable a log of the graph drawn")
    st.session_state['color'] = st.sidebar.checkbox("Enable / Disable coloring of the vertices")
    start_drawing = st.sidebar.button("Draw Tree", on_click=trigger_drawing)
    

def trigger_drawing():
    figure = draw.draw( 
                        st.session_state['k'], 
                        st.session_state['h'], 
                        st.session_state['integer'], 
                        st.session_state['logging'], 
                        st.session_state['color']
                    )
    st.pyplot(figure)
    st.write()        

if __name__ == "__main__":
    main()
