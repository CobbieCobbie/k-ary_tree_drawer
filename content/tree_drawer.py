"""k-ary tree drawer — core algorithm and Plotly rendering."""

from __future__ import annotations

import math
import os
import time
import logging as log
from dataclasses import dataclass, field
from datetime import datetime

import plotly.graph_objects as go

import content.argparser as arg
import content.draw_support as support
from content.Vertex import Vertex


# ---------------------------------------------------------------------------
# Layout computation (pure, no globals)
# ---------------------------------------------------------------------------

@dataclass
class _LayoutState:
    """Mutable accumulator passed through the recursive layout traversal."""
    k: int
    h: int
    integer: bool
    nodes: list[Vertex] = field(default_factory=list)
    edges: list[tuple[Vertex, Vertex]] = field(default_factory=list)
    l_min: float = float("inf")
    l_max: float = 0.0
    v_counter: int = 0
    percentage: float = 0.0

    @property
    def v_max(self) -> float:
        if self.k > 1:
            return (pow(self.k, self.h + 1) - 1) / (self.k - 1)
        return self.h + 1


def _place_children(v: Vertex, r: float, state: _LayoutState) -> None:
    """Recursively place children of *v* onto the layout."""
    if v.height > state.h - 1:
        return

    d = 2 * pow(state.k, state.h - v.height - 1)
    x_start = v.x - (state.k - 1) * pow(state.k, state.h - v.height - 1)

    for i in range(state.k):
        x_coord = x_start + i * d
        delta_x = x_coord - v.x
        y_coord = v.y - math.sqrt(r * r - delta_x * delta_x)

        if state.integer:
            y_coord = round(y_coord, 0)

        state.v_counter += 1
        child = Vertex(
            id=state.v_counter,
            coordinates=(x_coord, y_coord),
            height=v.height + 1,
        )

        state.nodes.append(child)
        state.edges.append((v, child))

        edge_length = math.sqrt(
            (v.x - child.x) ** 2 + (v.y - child.y) ** 2
        )
        if edge_length < state.l_min:
            state.l_min = edge_length
        if edge_length > state.l_max:
            state.l_max = edge_length

        percent = round((state.v_counter / state.v_max) * 100, 0)
        if percent > state.percentage:
            state.percentage = percent
            print(f"Percentage of vertices processed: {percent:.0f}%")

        _place_children(child, r, state)


def compute_layout(
    k: int,
    h: int,
    integer: bool = False,
) -> tuple[list[Vertex], list[tuple[Vertex, Vertex]], float, float]:
    """Compute node positions for a k-ary tree of the given height.

    Returns
    -------
    nodes:
        All ``Vertex`` objects in traversal order (root first).
    edges:
        List of (parent, child) ``Vertex`` pairs.
    l_min:
        Minimum edge length in the resulting drawing.
    l_max:
        Maximum edge length in the resulting drawing.
    """
    root = Vertex(id=0, coordinates=(0.0, 0.0), height=0)
    state = _LayoutState(k=k, h=h, integer=integer)
    state.nodes.append(root)
    state.v_counter = 1  # root already counted

    r = float(pow(k, h))
    _place_children(root, r, state)

    return state.nodes, state.edges, state.l_min, state.l_max


# ---------------------------------------------------------------------------
# Plotly rendering
# ---------------------------------------------------------------------------

def draw(
    k: int,
    h: int,
    integer: bool = False,
    logging: bool = False,
    color: bool = False,
) -> go.Figure:
    """Compute and render a k-ary tree drawing as an interactive Plotly figure.

    Parameters
    ----------
    k:
        Branching factor (max children per node).
    h:
        Height of the tree.
    integer:
        Snap y-coordinates to integer grid points.
    logging:
        Write a timestamped ``.log`` file to the ``logging/`` directory.
    color:
        Colour-code nodes by cycling through the RGB colour wheel.

    Returns
    -------
    plotly.graph_objects.Figure
    """
    _time = time.time()

    if logging:
        folder = "logging"
        if not os.path.exists(folder):
            os.makedirs(folder)
        file_name = (
            datetime.today().strftime("%Y-%m-%d_%H-%M-%S")
            + f"_{k}-ary_tree_with_height_{h}.log"
        )
        log.basicConfig(
            filename=os.path.join(folder, file_name),
            encoding="utf-8",
            level=log.DEBUG,
            force=True,
        )
        log.info(f"Parameters: k={k}, h={h}, integer={integer}, color={color}")

    nodes, edges, l_min, l_max = compute_layout(k, h, integer)

    # --- edge traces (one trace per edge for clean hover suppression) -------
    # Batch all edges into a single trace using None-separated segments for
    # performance; this is the standard Plotly idiom.
    edge_x: list[float | None] = []
    edge_y: list[float | None] = []
    for parent, child in edges:
        edge_x += [parent.x, child.x, None]
        edge_y += [parent.y, child.y, None]

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        mode="lines",
        line=dict(color="#555555", width=1, dash="dot"),
        hoverinfo="none",
        showlegend=False,
    )

    # --- node trace --------------------------------------------------------
    total = len(nodes)
    if color:
        node_colors = [support.calc_hex_code(i, total) for i in range(total)]
        node_colors[0] = "#000000"  # root always black
    else:
        node_colors = ["#000000"] * total

    node_x = [v.x for v in nodes]
    node_y = [v.y for v in nodes]
    hover_text = [
        f"id: {v.id}<br>x: {v.x:.4f}<br>y: {v.y:.4f}<br>depth: {v.height}"
        for v in nodes
    ]

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers",
        marker=dict(size=6, color=node_colors, line=dict(width=0)),
        text=hover_text,
        hoverinfo="text",
        showlegend=False,
    )

    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(
        title=f"{k}-ary tree, height {h}",
        xaxis=dict(visible=False, scaleanchor="y", scaleratio=1),
        yaxis=dict(visible=False),
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=20, r=20, t=40, b=20),
        hovermode="closest",
    )

    # statistics
    _time = time.time() - _time
    _minutes = int(_time / 60)
    _seconds = _time % 60
    support.print_statistics(_minutes, _seconds, l_min, l_max)

    return fig


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = arg.create_parser()
    args = parser.parse_args()
    fig = draw(
        k=args.k,
        h=args.h,
        integer=args.integer,
        logging=args.logging,
        color=args.color,
    )
    fig.show()


if __name__ == "__main__":
    main()
