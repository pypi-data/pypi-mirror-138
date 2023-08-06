import ast
import networkx as nx


class AstGraph(ast.NodeVisitor):
    def __init__(self):
        self.graph = nx.DiGraph()
        self.count = 0

    def visit_Module(self, node):
        self.graph.add_node(node, shape='box', label=f'Module', fillcolor='deeppink', style='filled')
        self.graph.add_edge(node, self.visit(node.body[0]))
        return node

    def visit_FunctionDef(self, node):
        self.graph.add_node(node, shape='box', label=f'Function: {node.name}', fillcolor='purple', style='filled')
        for arg in self.visit(node.args):
            self.graph.add_edge(node, arg)
        for b in node.body:
            self.graph.add_edge(node, self.visit(b))
        return node

    def visit_arguments(self, node):
        self.graph.add_node(node, shape='box', label='arguments', fillcolor='limegreen', style='filled')
        for arg in node.args:
            self.graph.add_node(arg, shape='box', label=f'Arg: {arg.arg}', fillcolor='royalblue', style='filled')
            self.graph.add_edge(node, arg)
        return [node]

    def visit_Assign(self, node):
        self.graph.add_node(node, shape='box', label='Assign', fillcolor='gold', style='filled')
        for target in node.targets:
            self.graph.add_edge(node, self.visit(target))
        self.graph.add_edge(node, self.visit(node.value))
        return node

    def visit_Name(self, node):
        self.graph.add_node(node, shape='box', label=f'Name: {node.id}', fillcolor='pink', style='filled')
        return node

    def visit_List(self, node):
        self.graph.add_node(node, shape='box', label='List', fillcolor='rosybrown', style='filled')
        for element in node.elts:
            self.graph.add_edge(node, self.visit(element))
        return node

    def visit_Num(self, node):
        self.graph.add_node(node, shape='box', label=f'Constant: {node.n}', fillcolor='gray', style='filled')
        return node

    def visit_For(self, node):
        self.graph.add_node(node, shape='box', label='For', fillcolor='darkkhaki', style='filled')
        self.graph.add_edge(node, self.visit(node.target))
        self.graph.add_edge(node, self.visit(node.iter))
        for b in node.body:
            self.graph.add_edge(node, self.visit(b))
        return node

    def visit_Call(self, node):
        self.graph.add_node(node, shape='box', label='Call', fillcolor='lightyellow', style='filled')
        self.graph.add_edge(node, self.visit(node.func))
        for arg in node.args:
            self.graph.add_edge(node, self.visit(arg))
        return node

    def visit_Expr(self, node):
        self.graph.add_node(node, shape='box', label="expr", fillcolor='coral', style='filled')
        self.graph.add_edge(node, self.visit(node.value))
        return node

    def visit_Attribute(self, node):
        self.graph.add_node(node, shape='box', label=f'Attribute: {node.attr}', fillcolor='magenta', style='filled')
        self.graph.add_edge(node, self.visit(node.value))
        return node

    def visit_BinOp(self, node):
        self.graph.add_node(node, shape='box', label='BinOp', fillcolor='cyan', style='filled')
        self.graph.add_edge(node, self.visit(node.left))
        self.graph.add_edge(node, self.visit(node.right))
        self.count += 1
        self.graph.add_node(str(node.op) + str(self.count), shape='box', label=f'{type(node.op).__name__}',
                            fillcolor='lightskyblue', style='filled')
        self.graph.add_edge(node, str(node.op) + str(self.count))
        return node

    def visit_Subscript(self, node):
        self.graph.add_node(node, shape='box', label='Subscript', fillcolor='powderblue', style='filled')
        self.graph.add_edge(node, self.visit(node.value))
        self.graph.add_edge(node, self.visit(node.slice))
        return node

    def visit_Index(self, node):
        self.graph.add_node(node, shape='box', label="index", fillcolor='green', style='filled')
        self.graph.add_edge(node, self.visit(node.value))
        return node

    def visit_Return(self, node):
        self.graph.add_node(node, shape='box', label='Return', fillcolor='tomato', style='filled')
        self.graph.add_edge(node, self.visit(node.value))
        return node
