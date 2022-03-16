import sys
import math
import networkx as nx
import matplotlib.pyplot as plot


class Vertex:
    def __init__(self, x, y, h):
        self.coordinates = (x, y)
        self.height = h

    def __repr__(self):
        return "coordinates are: " \
               + str(self.coordinates[0]) + "," + str(self.coordinates[1]) +\
               "\n Height equals: " + str(self.height)


v_max = 0
v_counter = 0
l_max = 0
l_min = float("inf")


def main():
    k = 2
    h = 3
    args = sys.argv[1:]
    if len(args) >= 2:
        if args[0] == "-k":
            k = int(args[1])
        if args[0] == "-h":
            h = int(args[1])
    if len(args) >= 4:
        if args[2] == "-k":
            k = int(args[3])
        if args[2] == "-h":
            h = int(args[3])

    # further initializations

    root = Vertex(0, 0, 0)
    r = pow(k, h)
    print("k: " + str(k))
    print("height: " + str(h))
    print("radius: " + str(r))

    G = nx.Graph()
    G.add_node(root)

    global v_counter, v_max
    v_max = (pow(k, h + 1) - 1) / (k - 1)
    v_counter += 1

    draw_vertices(root, r, h, k, G)
    pos = {v: v.coordinates for v in G}
    nx.draw(G,
            pos=pos,
            with_labels=False,
            node_color="black",
            edge_color="lightblue",
            node_size=10,
            style="-.",
            )
    print("########################################")
    print("l_min: " + str(l_min))
    print("l_max: " + str(l_max))
    print("Ratio of resulting drawing: " + str(l_max / l_min))
    plot.show()


def draw_vertices(v, r, h, k, G):
    if v.height <= h-1:
        d = 2*pow(k, h-v.height-1)
        x_start = v.coordinates[0] - (k-1)*pow(k, h-v.height-1)
        for i in range(k):
            print(i)
            x_coord = x_start + i * d
            print("x_coord: "+str(x_coord))
            print("v.coordinates: " + str(v.coordinates[1]))
            y_coord = v.coordinates[1] - math.sqrt(r*r - (x_coord - v.coordinates[0])*(x_coord - v.coordinates[0]))
            y_coord = round(y_coord, 0)
            v_child = Vertex(x_coord, y_coord, v.height+1)
            print(v_child)

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
            print("\n Percentage of vertices covered: " +
                  str(round((v_counter / v_max) * 100, 2)) + "%")
            draw_vertices(v_child, r, h, k, G)


if __name__ == "__main__":
    main()
