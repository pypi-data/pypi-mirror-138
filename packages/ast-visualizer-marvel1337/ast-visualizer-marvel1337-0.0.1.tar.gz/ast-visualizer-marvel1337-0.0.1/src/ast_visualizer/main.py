import ast
import inspect
import networkx as nx
from matplotlib import pyplot as plt


def fib(n: int) -> list[int]:
    ans: list[int] = [0, 1]

    for i in range(n - 2):
        ans.append(ans[-1] + ans[-2])

    return ans[0:n]


class Walker(ast.NodeVisitor):
    def __init__(self):
        self.count: int = 0
        self.stack: list[int] = []
        self.graph: nx.DiGraph = nx.DiGraph()
        self.labels: dict[int, str] = {}
        self.colors: list[str] = []
        self.sizes: list[int] = []

    def generic_visit(self, node):
        node_name: int = self.count
        node_label: str = get_label(node)
        self.labels[self.count] = node_label
        self.colors.append(get_color(node))
        self.sizes.append(len(node_label) * 300)
        parent_name = None

        if self.stack:
            parent_name = self.stack[-1]

        self.stack.append(node_name)
        self.graph.add_node(node_name)

        if parent_name is not None:
            self.graph.add_edge(parent_name, node_name)

        self.count += 1
        super().generic_visit(node)

        self.stack.pop()


def get_label(node) -> str:
    if isinstance(node, ast.Name):
        return 'Name ' + node.id
    elif isinstance(node, ast.arg):
        return 'Argument ' + node.arg
    elif isinstance(node, ast.Constant):
        return 'Constant ' + str(node.value)
    elif isinstance(node, ast.FunctionDef):
        return 'Function ' + node.name
    else:
        return node.__class__.__name__


def get_color(node) -> str:
    color = "blue"
    if isinstance(node, ast.Constant):
        color = "yellow"
    elif isinstance(node, (ast.BinOp, ast.BoolOp, ast.UnaryOp)):
        color = "red"
    elif isinstance(node, ast.Call):
        color = "orange"
    elif isinstance(node, ast.Name):
        color = "green"
    elif isinstance(node, (ast.Load, ast.Store, ast.Del)):
        color = "brown"
    return color


def get_ast() -> ast.AST:
    return ast.parse(inspect.getsource(fib))


def print_ast(path="artifacts/ast.png", my_ast: ast.AST = get_ast()):
    walker: Walker = Walker()
    walker.visit(my_ast)
    plt.figure(1, (19, 11))
    nx.draw(
        walker.graph,
        nx.drawing.nx_pydot.graphviz_layout(walker.graph, prog='dot'),
        node_size=walker.sizes,
        labels=walker.labels,
        node_color=walker.colors,
        font_size=9
    )
    plt.savefig(path)
