import argparse

def create_parser():
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
    return parser