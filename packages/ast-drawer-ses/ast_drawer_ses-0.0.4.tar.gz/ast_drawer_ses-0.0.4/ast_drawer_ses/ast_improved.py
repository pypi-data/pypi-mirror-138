# TODO make
import ast
from ast import parse, iter_child_nodes
from inspect import getsource
from os import makedirs
from os.path import exists
import networkx as nx
from ast_drawer_ses.fib import fib
import pprint
from networkx.drawing.nx_pydot import graphviz_layout

node_counter = 0


def handle_ast_node(ast_node, ast_parent_node_info, graph):
    t_ast_node = type(ast_node)
    if t_ast_node == ast.Load or t_ast_node == ast.Store:
        return

    ast_node_info = node_info(ast_node)

    graph.add_edge(ast_parent_node_info, ast_node_info)
    if t_ast_node != ast.Subscript:
        build_networkx_graph_from_ast(ast_node, ast_node_info, graph)


def node_info(ast_node):
    global node_counter
    node_info_dict = {
        ast.arguments:
            lambda arguments_ast: "Arguments",
        ast.arg:
            lambda argument_ast: "Function argument " + argument_ast.arg,
        ast.FunctionDef:
            lambda function_def_ast: "Function '" + function_def_ast.name + "' definition",
        ast.Assert:
            lambda assert_ast: "Assert",
        ast.Name:
            lambda name_ast: "Id: " + name_ast.id,
        ast.Constant:
            lambda constant_ast: "Constant " + str(constant_ast.value),
        ast.BinOp:
            lambda binop_ast: "Binary operation",
        ast.Add:
            lambda add_ast: "+",
        ast.Sub:
            lambda sub_ast: "-",
        ast.Mult:
            lambda mult_ast: "*",
        ast.Compare:
            lambda cmp_ast: "Compare",
        ast.GtE:
            lambda gte_ast: ">=",
        ast.List:
            lambda list_ast: "[]",
        ast.For:
            lambda for_loop_ast: "For loop",
        ast.Return:
            lambda return_kw_ast: "Return",
        ast.Assign:
            lambda assign_ast: "=",
        ast.Subscript:
            lambda subscript_ast: ast.unparse(subscript_ast),
        ast.Call:
            lambda func_call_ast: "Function call: " + ast.unparse(func_call_ast),
    }

    node_counter += 1

    if type(ast_node) in node_info_dict:
        return "Node " + str(node_counter) + ": " + node_info_dict[type(ast_node)](ast_node)

    return "Node " + str(node_counter) + ": " + str(type(ast_node))


def build_networkx_graph_from_ast(ast_node, ast_node_info, graph):
    for ast_node_child in iter_child_nodes(ast_node):
        handle_ast_node(ast_node_child, ast_node_info, graph)


def draw_ast(func):
    func_ast = parse(getsource(func)).body[0]
    g = nx.DiGraph()
    pprint.pprint(ast.dump(func_ast))
    build_networkx_graph_from_ast(func_ast, node_info(func_ast), g)
    g.remove_nodes_from(list(nx.isolates(g)))
    p = nx.drawing.nx_pydot.to_pydot(g)
    if not exists('../artifacts'):
        makedirs('../artifacts')
    # I think there is a bug in this function, probably later I will leave bugreport or something
    # It leaves me with some isolated vertices, which are not present in g before calling to_pydot function
    p.write_png('artifacts/ast_improved.png')


if __name__ == '__main__':
    draw_ast(fib)
