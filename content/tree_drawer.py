import math
import os
import networkx as nx
import time
import logging as log
from datetime import datetime
import matplotlib.pyplot as plt

import content.argparser as arg
import content.draw_support as support
import content.Vertex as Vertex


integer_grid = False
k = 2
h = 3

percentage = 0.0
v_max = 0
v_counter = 0
l_max = 0
l_min = float("inf")

# color counter
col_r = 255
col_g = 0
col_b = 0


def main():
    parser = arg.create_parser()
    parser.parse_args()
    
    # global variable initializations
    global k, h, integer_grid
    k = parser.k
    h = parser.h
    integer_grid = parser.integer
    logging = parser.logging
    color = parser.color

    plot = draw(k, h, integer_grid, logging, color)
    plot.show()


def draw_vertices(v, r, h, k, G):
    if v.height <= h - 1:
        d = 2 * pow(k, h - v.height - 1)
        x_start = v.coordinates[0] - (k - 1) * pow(k, h - v.height - 1)
        for i in range(k):
            x_coord = x_start + i * d
            y_coord = v.coordinates[1] - math.sqrt(r * r - (x_coord - v.coordinates[0]) * (x_coord - v.coordinates[0]))
            if integer_grid is True:
                y_coord = round(y_coord, 0)
            global v_counter
            v_counter += 1
            v_child = Vertex(x_coord, y_coord, v.height + 1, v_counter)
            G.add_node(v_child)
            G.add_edge(v, v_child)
            global l_min, l_max
            edge_length = math.sqrt(
                (v.coordinates[0] - v_child.coordinates[0]) ** 2
                +
                (v.coordinates[1] - v_child.coordinates[1]) ** 2)
            if edge_length < l_min:
                l_min = edge_length
            if edge_length > l_max:
                l_max = edge_length
            global percentage, v_max
            percent = round((v_counter / v_max) * 100, 0)
            if percent > percentage:
                percentage = percent
                print(f"Percentage of vertices processed: {percent}%")
            draw_vertices(v_child, r, h, k, G)


def draw(k, h, integer, logging, color):
    integer_grid = integer

    # time init
    _time = time.time()

    # logging init
    if logging is True:
        log.info("Parameters:")
        log.info(f"k = {k}, h = {h}, integer grid = {integer_grid}")
        folder = 'logging'
        file_name = datetime.today().strftime('%Y-%m-%d_%H-%M-%S') + f"_{k}-ary_tree_with_height_{h}" + '.log'
        full_path = os.path.join(folder, file_name)
        if not os.path.exists(folder):
            os.makedirs(folder)
        log.basicConfig(filename=full_path, encoding='utf-8', level=log.DEBUG, force=True)

    global v_counter, v_max
    if k > 1:
        v_max = (pow(k, h + 1) - 1) / (k - 1)
    else:
        v_max = h + 1
    r = pow(k, h)
    G = nx.Graph()
    root = Vertex(0, 0, 0, 0)

    # add root to G
    G.add_node(root)
    v_counter += 1

    # draw recursively
    draw_vertices(root, r, h, k, G)

    # address the positions in a dict and draw
    fig, ax = plt.subplots()
    pos = {v: v.coordinates for v in G}
    if color is True:
        color_map = [support.calc_hex_code() for v in G]
        color_map[0] = "#000000"
    else:
        color_map = ["#000000" for v in G]
    nx.draw(G,
            pos=pos,
            with_labels=False,
            node_color=color_map,
            edge_color="#333333",
            node_size=10,
            style=":"
            )

    # statistics
    _time = time.time() - _time
    _minutes = int(_time / 60)
    _seconds = _time % 60
    percentage = 0.0
    support.print_statistics(_minutes, _seconds, l_min, l_max) 

    #ax.set_facecolor("white")
    #ax.axis("off")
    #ax.set_aspect("equal")
    plt.savefig("query" + ".png", dpi=300)
    #fig.set_facecolor("white")
    return fig


if __name__ == "__main__":
    main()
