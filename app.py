"""k-ary Tree Drawer — Streamlit single-page application."""

import streamlit as st
from content.tree_drawer import draw


# ---------------------------------------------------------------------------
# Cached drawing — re-runs only when parameters actually change
# ---------------------------------------------------------------------------

@st.cache_data
def get_figure(k: int, h: int, integer: bool, color: bool):
    """Compute and cache the Plotly figure for the given tree parameters."""
    return draw(k=k, h=h, integer=integer, logging=False, color=color)


# ---------------------------------------------------------------------------
# Page layout
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="k-ary Tree Drawer",
    page_icon="🌳",
    layout="wide",
)

st.title("k-ary Tree Drawer")
st.caption("Interactive straight-line drawing with uniform edge lengths.")

# --- Sidebar: parameters ---------------------------------------------------
with st.sidebar:
    st.header("Parameters")

    k = st.number_input(
        "Branching factor k",
        min_value=2,
        max_value=20,
        value=2,
        help="Maximum number of children per node.",
    )
    h = st.number_input(
        "Height h",
        min_value=1,
        max_value=10,
        value=3,
        help="Height of the tree (root is at depth 0).",
    )
    integer = st.checkbox(
        "Snap to integer grid",
        value=False,
        help="Round y-coordinates to the nearest integer.",
    )
    color = st.checkbox(
        "Color-code nodes",
        value=False,
        help="Cycle through the RGB colour wheel across all nodes.",
    )

    draw_button = st.button("Draw Tree", type="primary", use_container_width=True)

# --- Main area: result -----------------------------------------------------
if draw_button or "figure" in st.session_state:
    with st.spinner("Computing layout…"):
        fig = get_figure(k=int(k), h=int(h), integer=integer, color=color)
    st.session_state["figure"] = fig
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Set the parameters in the sidebar and press **Draw Tree**.")
