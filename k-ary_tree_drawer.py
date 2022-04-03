import math
import os
import networkx as nx
import matplotlib.pyplot as plot
import time
import logging as log
import argparse
from datetime import datetime


class Vertex:
    def __init__(self, x, y, h, id):
        self.coordinates = (x, y)
        self.height = h
        self.id = id

    def __repr__(self):
        return "coordinates are: " \
               + str(self.coordinates[0]) + "," + str(self.coordinates[1]) + \
               "\n Height equals: " + str(self.height)


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
    parser = argparse.ArgumentParser(description="Draws a k-ary tree with parameters k and height h")
    parser.add_argument("-k",
                        type=int,
                        dest="k",
                        default=2,
                        help="Maximum amount of children for any vertex, defaults to 2"
                        )
    parser.add_argument("--height",
                        "-he",
                        type=int,
                        dest="h",
                        default=3,
                        help="Height of the k-ary tree, defaults to 3")
    parser.add_argument("--integer",
                        "-i",
                        dest="integer",
                        type=bool,
                        action=argparse.BooleanOptionalAction,
                        default=False,
                        help="Places the vertices on integer grid points by rounding the coordinates")
    parser.add_argument("--logging",
                        "-l",
                        dest="logging",
                        default=False,
                        type=bool,
                        action=argparse.BooleanOptionalAction,
                        help="Enable / Disable a log of the graph drawn"
                        )
    parser.add_argument("--color",
                        "-c",
                        dest="color",
                        default=False,
                        type=bool,
                        action=argparse.BooleanOptionalAction,
                        help="Enable / Disable coloring of the vertices"
                        )
    args = parser.parse_args()

    # global variable initializations

    global k, h, integer_grid

    k = args.k
    h = args.h
    integer_grid = args.integer

    # time init

    _time = time.time()

    # logging init

    if args.logging is True:
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
        v_max = h+1
    r = pow(k, h)
    G = nx.Graph()
    root = Vertex(0, 0, 0, 0)

    # add root to G

    G.add_node(root)
    v_counter += 1
    # draw recursively

    draw_vertices(root, r, h, k, G)

    # address the positions in a dict and draw

    fig, ax = plot.subplots()
    pos = {v: v.coordinates for v in G}
    if args.color is True:
        color_map = [calc_hex_code() for v in G]
    else:
        color_map = ["#ffffff" for v in G]
    nx.draw(G,
            pos=pos,
            with_labels=False,
            node_color=color_map,
            edge_color="#333333",
            node_size=10,
            style=":"
            )

    # print results

    _time = time.time() - _time
    _minutes = int(_time / 60)
    _seconds = _time % 60

    print("########################################")
    print("l_min: " + str(l_min))
    print("l_max: " + str(l_max))
    print("Ratio of resulting drawing: " + str(l_max / l_min))

    if args.logging is True:
        log.debug("l_min: " + str(l_min))
        log.debug("l_max: " + str(l_max))
        log.debug("Ratio of resulting drawing: " + str(l_max / l_min))

    print(f"The process took {_minutes:.0f} minutes and {_seconds:.3f} seconds!")

    ax.set_facecolor("black")
    ax.axis("off")
    fig.set_facecolor("black")

    plot.show()


def calc_hex_code():
    global k, h
    interval = min(k, h) * 255 / pow(k, h)
    global col_b, col_g, col_r
    if col_r == 255 and 0 <= col_g < 255 and col_b == 0:
        col_g += interval
        if col_g > 255:
            col_g = 255
    elif 0 < col_r <= 255 and col_g == 255 and col_b == 0:
        col_r -= interval
        if col_r < 0:
            col_r = 0
    elif 0 == col_r and col_g == 255 and 0 <= col_b < 255:
        col_b += interval
        if col_b > 255:
            col_b = 255
    elif 0 == col_r and 0 < col_g <= 255 and col_b == 255:
        col_g -= interval
        if col_g < 0:
            col_g = 0
    elif 0 <= col_r < 255 and 0 == col_g and col_b == 255:
        col_r += interval
        if col_r > 255:
            col_r = 255
    elif col_r == 255 and col_g == 0 and 0 < col_b <= 255:
        col_b -= interval
        if col_b < 0:
            col_b = 0
    return "#" + ('%02x%02x%02x' % (round(col_r), round(col_g), round(col_b)))


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


if __name__ == "__main__":
    main()
