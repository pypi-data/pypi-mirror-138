from ast import parse, iter_child_nodes, unparse
import ast
from inspect import getsource
import networkx as nx
from fib import fib
from os.path import exists
from os import makedirs


def build_networkx_graph_from_ast(ast_node, graph):
    # if we do not manually create a node there may be weird effects
    graph.add_node(type(ast_node))
    for ast_node_child in iter_child_nodes(ast_node):
        graph.add_edge(type(ast_node), type(ast_node_child))
        build_networkx_graph_from_ast(ast_node_child, graph)


def draw_ast(func):
    func_ast = parse(getsource(func)).body[0]
    g = nx.DiGraph()
    build_networkx_graph_from_ast(func_ast, g)
    p = nx.drawing.nx_pydot.to_pydot(g)
    if not exists('../artifacts'):
        makedirs('../artifacts')
    p.write_png('artifacts/ast_basic.png')


if __name__ == '__main__':
    draw_ast(fib)
