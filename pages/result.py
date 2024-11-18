import streamlit as st
import content.tree_drawer as draw
import pages.input as input


def main():
    st.title("Tree Drawer")
    figure = input.get_drawing()
    
    st.pyplot(figure)


if __name__ == "__main__":
    main()
