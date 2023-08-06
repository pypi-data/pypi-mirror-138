import ast
import networkx as nx


class ASTVisitor(ast.NodeVisitor):
    def __init__(self):
        self.graph = nx.DiGraph()

    def visit_FunctionDef(self, node):
        self.graph.add_node(node, shape='box', label=f'FunctionDef: {node.name}', fillcolor='#A49393', style='filled')
        for arg in self.visit(node.args):
            self.graph.add_edge(node, arg)
        for body_item in node.body:
            self.graph.add_edge(node, self.visit(body_item))
        return node

    def visit_arguments(self, node):
        self.graph.add_node(node, shape='box', label='arguments', fillcolor='#B27883', style='filled')
        for arg in node.args:
            self.graph.add_node(arg, shape='box', label=f'arg: {arg.arg}', fillcolor='grey', style='filled')
            self.graph.add_edge(node, arg)
        return [node]

    # body
    def visit_Assign(self, node):
        self.graph.add_node(node, shape='box', label='Assign', fillcolor='#EF7C8E', style='filled')
        for t in node.targets:
            self.graph.add_edge(node, self.visit(t))
        self.graph.add_edge(node, self.visit(node.value))
        return node

    def visit_Name(self, node):
        self.graph.add_node(node, shape='box', label=f'Name: {node.id}', fillcolor='#FAE8E0', style='filled')
        return node

    def visit_Constant(self, node):
        self.graph.add_node(node, shape='box', label=f'Constant: {node.value}', fillcolor='#FFC2C7', style='filled')
        return node

    def visit_For(self, node):
        self.graph.add_node(node, shape='box', label='For', fillcolor='#EBE0D0', style='filled')
        self.graph.add_edge(node, self.visit(node.target))
        self.graph.add_edge(node, self.visit(node.iter))

        for body_item in node.body:
            self.graph.add_edge(node, self.visit(body_item))
        return node

    def visit_Call(self, node):
        self.graph.add_node(node, shape='box', label='Call', fillcolor='#F79489', style='filled')
        self.graph.add_edge(node, self.visit(node.func))
        for arg in node.args:
            self.graph.add_edge(node, self.visit(arg))
        return node

    def visit_BinOp(self, node):
        self.graph.add_node(node, shape='box', label=f'BinOp: {type(node.op).__name__}', fillcolor='#E6E7E8',
                            style='filled')
        self.graph.add_edge(node, self.visit(node.left))
        self.graph.add_edge(node, self.visit(node.right))
        return node

    def visit_Return(self, node):
        self.graph.add_node(node, shape='box', label='Return', fillcolor='#EC9EC0', style='filled')
        self.graph.add_edge(node, self.visit(node.value))
        return node

    def visit_Expr(self, node):
        self.graph.add_node(node, shape='box', label="Expr", fillcolor='#D8A7B1', style='filled')
        self.graph.add_edge(node, self.visit(node.value))
        return node

    def visit_Attribute(self, node):
        self.graph.add_node(node, shape='box', label=f'Attribute: {node.attr}', fillcolor='#B6E2D3', style='filled')
        self.graph.add_edge(node, self.visit(node.value))
        return node

    def visit_List(self, node):
        self.graph.add_node(node, shape='box', label='List', fillcolor='#95DED6', style='filled')
        for elt in node.elts:
            self.graph.add_edge(node, self.visit(elt))
        return node

    # def visit_Load(self, node):
    #     self.graph.add_node(node, shape='box', label='Load')
    #     return node

    # def visit_Store(self, node):
    #     self.graph.add_node(node, shape='box', label='Store')
    #     return node
