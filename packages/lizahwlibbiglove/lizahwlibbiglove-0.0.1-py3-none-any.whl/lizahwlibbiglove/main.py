import ast
import inspect
import networkx as nx

from lizahwlibbiglove.ast_graph import AstGraph
from lizahwlibbiglove.fibonacci import fibonacci

def draw_ast():
    ast_object = ast.parse(inspect.getsource(fibonacci))
    ast_graph = AstGraph()
    ast_graph.visit(ast_object)
    nx.drawing.nx_pydot.to_pydot(ast_graph.graph).write_png("artifacts/ast.png")

if __name__ == "__main__":
    draw_ast()
