import ast
import inspect

import networkx as nx

from keklib.ast_visitor import ASTVisitor
from keklib.fib_numbers import fib_numbers


def print_ast(f, path):
    ast_visitor = ASTVisitor()
    ast_visitor.visit(ast.parse(inspect.getsource(f)))
    nx.drawing.nx_pydot.to_pydot(ast_visitor.graph).write_png(path)


if __name__ == '__main__':
    print_ast(fib_numbers, "../artifacts/fib_num_ast.png")
