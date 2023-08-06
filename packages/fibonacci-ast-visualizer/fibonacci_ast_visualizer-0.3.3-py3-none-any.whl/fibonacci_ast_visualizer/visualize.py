#!/usr/bin/python3
import ast
import astunparse
from inspect import getsource

import networkx as nx
import matplotlib.pyplot as plt
from hw_1.src.fibonacci_ast_visualizer.fibonacci import fibonacci as fib


class NetworkxGraphBuilder(ast.NodeVisitor):
    def __init__(self):
        self.graph = nx.DiGraph()
        self.stack = []

    def _visit_any(self, node):
        node_label = astunparse.unparse(node)
        if isinstance(node, ast.FunctionDef):
            node_label = f" Fun {node.name}"
        paren_label = None
        if self.stack:
            paren_label = self.stack[-1]
        self.stack.append(node_label)
        self.graph.add_node(node_label)
        if paren_label:
            self.graph.add_edge(node_label, paren_label)
        super(self.__class__, self).generic_visit(node)
        self.stack.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self._visit_any(node)

    def visit_Assign(self, node: ast.Assign):
        self._visit_any(node)

    def visit_Tuple(self, node: ast.Tuple):
        self._visit_any(node)

    def visit_Name(self, node: ast.Name):
        self._visit_any(node)

    def visit_Constant(self, node: ast.Constant):
        self._visit_any(node)

    def visit_For(self, node: ast.For):
        self._visit_any(node)

    def visit_Call(self, node: ast.Call):
        self._visit_any(node)

    def visit_Yield(self, node: ast.Yield):
        self._visit_any(node)

    def visit_BinOp(self, node: ast.BinOp):
        self._visit_any(node)


def visualize_and_save(directory='.', filename='fib.jpg', verbose=False):
    node = ast.parse(getsource(fib))
    gb = NetworkxGraphBuilder()
    gb.visit(node)

    if verbose:
        print(astunparse.dump(node))

    plt.figure(figsize=(16.53, 11.69))
    nx.draw(gb.graph, with_labels=True)
    plt.savefig(f"{directory}/{filename}")


if __name__ == "__main__":
    visualize_and_save()
