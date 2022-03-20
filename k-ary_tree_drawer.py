import math
import networkx as nx
import matplotlib.pyplot as plot
import time
import logging as log
import argparse


class Vertex:
    def __init__(self, x, y, h):
        self.coordinates = (x, y)
        self.height = h

    def __repr__(self):
        return "coordinates are: " \
               + str(self.coordinates[0]) + "," + str(self.coordinates[1]) +\
               "\n Height equals: " + str(self.height)


integer_grid = False
k = 2
h = 3

v_max = 0
v_counter = 0
l_max = 0
l_min = float("inf")


def main():
    parser = argparse.ArgumentParser(description="Draws a k-ary tree with parameters k and height h")
    parser.add_argument("-k",
                        nargs=1,
                        type=int,
                        dest="k",
                        help="maximum amount of children for any vertex"
                        )
    parser.add_argument("--height",
                        "-he",
                        nargs=1,
                        type=int,
                        dest="h",
                        help="height of the k-ary tree")
    parser.add_argument("--integer",
                        "-i",
                        dest="integer",
                        help="Places the vertices on integer grid points by rounding the coordinates")
    args = parser.parse_args()

    # further initializations

    global k, h, integer_grid
    k = args.k[0]
    h = args.h[0]
    integer_grid = args.integer

    log.info("Parameters:")
    log.info(f"k = {k}, h = {h}, integer grid = {integer_grid}")

    _time = time.time()
    timestamp = time.gmtime()

    log.basicConfig(filename=f"{timestamp.tm_year}-{timestamp.tm_mon}-{timestamp.tm_mday}_"
                             f"{timestamp.tm_hour}h{timestamp.tm_min}m{timestamp.tm_sec}s_"
                             f"{k}-ary_tree_with_h={h}.log", encoding='utf-8', level=log.DEBUG)

    global v_counter, v_max
    v_max = (pow(k, h + 1) - 1) / (k - 1)
    v_counter += 1

    r = pow(k, h)
    G = nx.Graph()
    root = Vertex(0, 0, 0)

    # add root to G

    G.add_node(root)

    # draw recursively

    draw_vertices(root, r, h, k, G)

    # address the positions in a dict and draw

    pos = {v: v.coordinates for v in G}
    nx.draw(G,
            pos=pos,
            with_labels=False,
            node_color="black",
            edge_color="lightblue",
            node_size=10,
            style="-.",
            )

    # print results

    print("########################################")
    log.debug("l_min: " + str(l_min))
    print("l_min: " + str(l_min))
    print("l_max: " + str(l_max))
    print("Ratio of resulting drawing: " + str(l_max / l_min))
    log.debug("l_max: " + str(l_max))
    log.debug("Ratio of resulting drawing: " + str(l_max / l_min))

    _time = time.time() - _time
    _minutes = int(_time / 60)
    _seconds = _time % 60
    print(f"The process took {_minutes:.0f} minutes and {_seconds:.3f} seconds!")
    print("integer grid: " + str(integer_grid))
    plot.show()


def draw_vertices(v, r, h, k, G):
    if v.height <= h-1:
        d = 2*pow(k, h-v.height-1)
        x_start = v.coordinates[0] - (k-1)*pow(k, h-v.height-1)
        for i in range(k):
            x_coord = x_start + i * d
            y_coord = v.coordinates[1] - math.sqrt(r*r - (x_coord - v.coordinates[0])*(x_coord - v.coordinates[0]))
            if integer_grid == True:
                y_coord = round(y_coord, 0)
                print("y rounded")
            v_child = Vertex(x_coord, y_coord, v.height+1)

            G.add_node(v_child)
            global v_counter, v_max
            v_counter += 1

            G.add_edge(v, v_child)
            global l_min, l_max
            edge_length = math.sqrt(
                (v.coordinates[0] - v_child.coordinates[0])**2
                +
                (v.coordinates[1] - v_child.coordinates[1])**2)
            if edge_length < l_min:
                l_min = edge_length
            if edge_length > l_max:
                l_max = edge_length
            print("Percentage of vertices covered: " +
                  str(round((v_counter / v_max) * 100, 3)) + "%")
            draw_vertices(v_child, r, h, k, G)


if __name__ == "__main__":
    main()
