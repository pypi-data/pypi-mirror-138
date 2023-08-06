import ast
import networkx as nx


_operations = {
    "Add": "ADD",
    "Sub": "SUB",
    "Mult": "MULT",
    "Div": "DIV",
    "Mod": "MOD",
    "Pow": "POW"
}


class AstGraphGenerator(object):
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_edge(self, node_a, nodes_b, edge_name):
        for node_b in nodes_b:
            self.graph.add_edge(node_a, node_b, label=edge_name)

    def visit(self, node):
        """Visit a node."""
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def visit_Constant(self, node):
        self.graph.add_node(str(node), label=f'Constant({node.value})', color='blue')
        return [str(node)]

    def visit_Name(self, node):
        self.graph.add_node(str(node), label=f'Name({node.id})', color='yellow')
        return [str(node)]

    def visit_Module(self, node):
        self.visit(node.body[0])

    def visit_FunctionDef(self, node):
        self.graph.add_node(str(node), label=f'Function({node.name})', color='red')
        self.add_edge(str(node), self.visit(node.args), 'args')
        for item in node.body:
            self.add_edge(str(node), self.visit(item), 'body')
        return str(node)

    def visit_arguments(self, node):
        node_results = []
        for item in node.args:
            node_results.append(str(item))
            self.graph.add_node(str(item), label=f'Argument({item.arg})', color='yellow')
        return node_results

    def visit_List(self, node):
        self.graph.add_node(str(node), label=f'List', color='blue')
        for item in node.elts:
            self.add_edge(str(node), self.visit(item), 'elts')
        return [str(node)]

    def visit_Assign(self, node):
        self.graph.add_node(str(node), label=f'Assign', color='green')
        for item in node.targets:
            self.add_edge(str(node), self.visit(item), 'target')
        self.add_edge(str(node), self.visit(node.value), 'value')
        return [str(node)]

    def visit_BinOp(self, node):
        for key, value in _operations.items():
            if key in str(node.op):
                node.op = value
        self.graph.add_node(str(node), label=f'BinOp({node.op})', color='green')
        self.add_edge(str(node), self.visit(node.left), 'left')
        self.add_edge(str(node), self.visit(node.right), 'right')
        return [str(node)]

    def visit_For(self, node):
        self.graph.add_node(str(node), label=f'For', color='green')
        self.add_edge(str(node), self.visit(node.target), 'target')
        self.add_edge(str(node), self.visit(node.iter), 'iter')
        for item in node.body:
            self.add_edge(str(node), self.visit(item), 'body')
        return [str(node)]

    def visit_Call(self, node):
        self.graph.add_node(str(node), label=f'Call', color='green')
        self.add_edge(str(node), self.visit(node.func), 'func')
        for item in node.args:
            self.add_edge(str(node), self.visit(item), 'args')
        return [str(node)]

    def visit_Subscript(self, node):
        self.graph.add_node(str(node), label=f'Subscript', color='green')
        self.add_edge(str(node), self.visit(node.value), 'value')
        self.add_edge(str(node), self.visit(node.slice), 'slice')
        return [str(node)]

    def visit_Return(self, node):
        self.graph.add_node(str(node), label=f'Return', color='green')
        self.add_edge(str(node), self.visit(node.value), 'value')
        return [str(node)]

    def generic_visit(self, node):
        raise NotImplementedError


if __name__ == '__main__':
    ast_object = ast.parse("""def fib(n):
        res = [0] * n
        res[0] = res[1] = 1
        for i in range(2, n):
            res[i] = res[i-1] + res[i-2]
        return res""")
    v = AstGraphGenerator()
    v.visit(ast_object)
    G = v.graph
    p = nx.drawing.nx_pydot.to_pydot(G)
    p.write_png('artifacts/example.png')
