from typing import Dict, List

import ast

import networkx as nx


def get_color(node: ast.expr) -> str:
    if isinstance(node, ast.Constant):
        return 'tab:purple'
    if isinstance(node, ast.Call):
        return 'tab:olive'
    if isinstance(node, ast.Name):
        return 'tab:green'
    if isinstance(node, ast.Load):
        return 'tab:blue'
    return 'tab:orange'


def get_label(node) -> str:
    label = type(node).__name__
    if isinstance(node, ast.Constant):
        return f'{label}\n{node.value}'
    if isinstance(node, ast.Name):
        return f'{label}\n{node.id}'
    if isinstance(node, ast.arg):
        return f'{label}\n{node.arg}'
    if isinstance(node, ast.FunctionDef):
        return f'{label}\n{node.name}'
    return label


class SimpleVisitor(ast.NodeVisitor):
    def __init__(self):
        self.graph = nx.DiGraph()
        self.labels: Dict = {}
        self.colors: List = []
        self.sizes: List = []

        self.parent: str = None

    def get_next_name(self) -> str:
        return str(len(self.colors))

    def generic_visit(self, node: ast.expr):
        name = self.get_next_name()
        label = get_label(node)

        self.labels[name] = label
        self.colors.append(get_color(node))
        self.sizes.append(160 * (3 + len(label)))

        self.graph.add_node(name)
        if self.parent:
            self.graph.add_edge(self.parent, name)

        temp = self.parent
        self.parent = name

        super().generic_visit(node)

        self.parent = temp
