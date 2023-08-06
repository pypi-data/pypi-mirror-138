import networkx as nx
import matplotlib.pyplot as plt
import ast
import os


def str_node(node):
    if isinstance(node, ast.AST):
        fields = [(name, str_node(val)) for name, val in ast.iter_fields(node) if name not in ('left', 'right')]

        rv = '%s(%s' % (node.__class__.__name__, ', '.join('%s=%s' % field for field in fields))
        return rv + ')'
    else:
        return repr(node)


def ast_visit(node, G, level=0):
    G.add_node(str_node(node)[0:10])
    for field, value in ast.iter_fields(node):
        if isinstance(value, list):
            for item in value:
                if isinstance(item, ast.AST):
                    G.add_edge(str_node(node)[0:10], str_node(item)[0:10])
                    ast_visit(item, G, level=level + 1)
        elif isinstance(value, ast.AST):
            G.add_edge(str_node(node)[0:10], str_node(value)[0:10])
            ast_visit(value, G, level=level + 1)


def generate_image(source_code_filename="fib.py"):
    G = nx.Graph()
    with open(source_code_filename, "r") as source:
        tree = ast.parse(source.read())
        ast_visit(tree, G)

    nx.draw(G, with_labels=True, font_weight='bold')
    plt.savefig("Graph.png", format="PNG")
