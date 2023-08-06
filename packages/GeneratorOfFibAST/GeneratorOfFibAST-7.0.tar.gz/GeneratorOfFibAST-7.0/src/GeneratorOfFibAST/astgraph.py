import networkx as nx
import ast


class AstVisitor(ast.NodeVisitor):
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_edges(self, node_from, nodes: list):
        for node_to in nodes:
            self.graph.add_edge(node_from, node_to)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.graph.add_node(node, shape='box', label=f"Function '{node.name}'", fillcolor='brown3', style='filled')
        self.add_edges(node, self.visit(node.args))
        for body in node.body:
            self.add_edges(node, self.visit(body))
        return [node]

    def visit_Assign(self, node: ast.AnnAssign):
        self.graph.add_node(node, shape='box', label='Assign', fillcolor='palevioletred', style='filled')
        for target in node.targets:
            self.add_edges(node, self.visit(target))
        self.add_edges(node, self.visit(node.value))
        return [node]

    def visit_For(self, node: ast.For):
        self.graph.add_node(node, shape='box', label='For cycle', fillcolor='hotpink3', style='filled')
        self.add_edges(node, self.visit(node.target))
        self.add_edges(node, self.visit(node.iter))
        for body in node.body:
            self.add_edges(node, self.visit(body))
        return [node]

    def visit_arguments(self, node: ast.arguments):
        self.graph.add_node(node, shape='egg', label='Arguments', fillcolor='mediumorchid', style='filled')
        for arg in node.args:
            self.add_edges(node, self.visit(arg))
        return [node]

    def visit_Return(self, node: ast.Return):
        self.graph.add_node(node, shape='egg', label='Return', fillcolor='violetred', style='filled')
        self.add_edges(node, self.visit(node.value))
        return [node]

    def visit_BinOp(self, node: ast.BinOp):
        self.graph.add_node(node, shape='box', label=f"BinOp '{type(node.op).__name__}'", fillcolor='slateblue',
                            style='filled')
        self.add_edges(node, self.visit(node.left))
        self.add_edges(node, self.visit(node.right))
        return [node]

    def visit_Subscript(self, node: ast.Subscript):
        self.graph.add_node(node, shape='box', label='Subscript', fillcolor='mediumpurple', style='filled')
        self.add_edges(node, self.visit(node.value))
        self.add_edges(node, self.visit(node.slice))
        return [node]

    def visit_Constant(self, node: ast.Constant):
        self.graph.add_node(node, shape='egg', label=f"Constant '{node.value}'", fillcolor='skyblue', style='filled')
        return [node]

    def visit_List(self, node: ast.List):
        self.graph.add_node(node, shape='box', label='List', fillcolor='lightskyblue', style='filled')
        for elt in node.elts:
            self.add_edges(node, self.visit(elt))
        return [node]

    def visit_Call(self, node: ast.Call):
        self.graph.add_node(node, shape='box', label='Call', fillcolor='lightcoral', style='filled')
        self.add_edges(node, self.visit(node.func))
        for arg in node.args:
            self.add_edges(node, self.visit(arg))
        return [node]

    def visit_Name(self, node: ast.Name):
        self.graph.add_node(node, shape='egg', label=f"Var '{node.id}'", fillcolor='lavender', style='filled')
        return [node]

    def visit_arg(self, node: ast.arg):
        self.graph.add_node(node, shape='egg', label=f"Arg '{node.arg}'", fillcolor='lightcyan', style='filled')
        return [node]
