import ast
import inspect

import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout

from fibonacci import fib
from simple_visitor import SimpleVisitor


class GraphDescription:
    def __init__(self, graph, labels, colors, sizes):
        self.graph = graph
        self.labels = labels
        self.colors = colors
        self.sizes = sizes


def get_description(tree) -> GraphDescription:
    visitor = SimpleVisitor()
    visitor.visit(tree)
    return GraphDescription(
        visitor.graph,
        visitor.labels,
        visitor.colors,
        visitor.sizes
    )


def draw(function):
    tree = ast.parse(inspect.getsource(function))
    description = get_description(tree)
    plt.figure(1, (15, 10))
    nx.draw(
        G=description.graph,
        pos=graphviz_layout(description.graph, prog="dot"),
        labels=description.labels,
        node_size=description.sizes,
        node_color=description.colors,
        font_size=8
    )
    plt.savefig("artifacts/tree.png")


if __name__ == "__main__":
    draw(fib)
