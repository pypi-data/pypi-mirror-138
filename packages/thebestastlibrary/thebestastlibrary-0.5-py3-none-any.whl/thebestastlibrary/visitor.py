import ast
import networkx


class ASTVisitor(ast.NodeVisitor):

    def __init__(self):
        self.graph = networkx.DiGraph()
        self.count = 0

    def visit_Module(self, node):
        self.visit(node.body[0])

    def visit_args(self, arguments):
        cur_count = self.count
        self.count += 1
        self.graph.add_node(cur_count, label="Arguments", fillcolor='#AAF0C8', style='filled')
        for arg in arguments:
            self.graph.add_node(self.count, label=f'name: {arg.arg}', shape='s', fillcolor='#80E7EA', style='filled')
            self.graph.add_edge(cur_count, self.count)
            self.count += 1
        return cur_count

    def visit_targets(self, node):
        cur_count = self.count
        self.count += 1
        self.graph.add_node(cur_count, label="Targets", fillcolor='#7C81F0', style='filled')
        for tar in node.targets:
            self.graph.add_edge(cur_count, self.visit(tar))
        return cur_count

    def visit_value(self, node):
        cur_count = self.count
        self.count += 1
        self.graph.add_node(cur_count, label="Value", fillcolor='#B470F5', style='filled')
        self.graph.add_edge(cur_count, self.visit(node.value))
        return cur_count

    def visit_body(self, node):
        cur_count = self.count
        self.count += 1
        self.graph.add_node(cur_count, label="body", fillcolor='#E54E2A', style='filled')
        for item in node.body:
            self.graph.add_edge(cur_count, self.visit(item))
        return cur_count

    def visit_target(self, node):
        cur_count = self.count
        self.count += 1
        self.graph.add_node(cur_count, label="Target", fillcolor='#F8EB90', style='filled')
        self.graph.add_edge(cur_count, self.visit(node.target))
        return cur_count

    def visit_Assign(self, node):
        cur_count = self.count
        self.count += 1
        self.graph.add_node(cur_count, label="Assign", shape='s', fillcolor='#EF7D58', style='filled')
        self.graph.add_edge(cur_count, self.visit_targets(node))
        self.graph.add_edge(cur_count, self.visit_value(node))
        return cur_count

    def visit_Name(self, node):
        self.graph.add_node(self.count, label=f'name: {node.id}', shape='s', fillcolor='#80E7EA', style='filled')
        self.count += 1
        return self.count - 1

    def visit_Num(self, node):
        self.graph.add_node(self.count, label=f'number \n value: {str(node.n)}', shape='s', fillcolor='#F7D8F4',
                            style='filled')
        self.count += 1
        return self.count - 1

    def visit_BinOp(self, node):
        cur_count = self.count
        self.count += 1
        self.graph.add_node(cur_count, label=f'BinaryOperation: \n {node.op.__class__.__name__}', shape='s',
                            fillcolor='#C0B6F0', style='filled')
        self.graph.add_edge(cur_count, self.visit(node.left))
        self.graph.add_edge(cur_count, self.visit(node.right))
        return cur_count

    def visit_For(self, node):
        cur_count_node = self.count
        self.count += 1
        cur_count_iter = self.count
        self.count += 1
        self.graph.add_node(cur_count_node, label="For", shape='s', fillcolor='#F5A845', style='filled')
        self.graph.add_node(cur_count_iter, label="iteration", fillcolor='#D6F5A7', style='filled')
        self.graph.add_edge(cur_count_node, cur_count_iter)
        self.graph.add_edge(cur_count_iter, self.visit_target(node))
        self.graph.add_edge(cur_count_iter, self.visit(node.iter))
        self.graph.add_edge(cur_count_node, self.visit_body(node))
        return cur_count_node

    def visit_Call(self, node):
        cur_count = self.count
        self.count += 1
        self.graph.add_node(cur_count, label="Call", fillcolor='#F37BD4', style='filled')
        self.graph.add_edge(cur_count, self.visit(node.func), label="function")
        for item in node.args:
            self.graph.add_edge(cur_count, self.visit(item), label="argument")
        return cur_count

    def visit_Tuple(self, node):
        cur_count = self.count
        self.count += 1
        self.graph.add_node(cur_count, label="Tuple", fillcolor='#87F38B', style='filled')
        for num, item in enumerate(node.elts):
            self.graph.add_edge(cur_count, self.visit(item), label=f'{num + 1} arg')
        return cur_count

    def visit_Expr(self, node):
        cur_count = self.count
        self.count += 1
        self.graph.add_node(cur_count, label="Expression", shape='s', fillcolor='#F9A354', style='filled')
        self.graph.add_edge(cur_count, self.visit(node.value))
        return cur_count

    def visit_Attribute(self, node):
        cur_count = self.count
        self.count += 1
        self.graph.add_node(cur_count, label=f'Attribute \n name: {node.attr}', shape='s', fillcolor='#F7FC5C',
                            style='filled')
        self.graph.add_edge(cur_count, self.visit(node.value))
        return cur_count

    def visit_List(self, node):
        cur_count = self.count
        self.count += 1
        self.graph.add_node(cur_count, label="List", fillcolor='#87F38B', style='filled')
        for num, item in enumerate(node.elts):
            self.graph.add_edge(cur_count, self.visit(item), label=f'elem {num + 1}')
        return cur_count

    def visit_FunctionDef(self, node):
        cur_count = self.count
        self.count += 1
        self.graph.add_node(cur_count, label=f'function name: {node.name}', shape='s', fillcolor='#E2A8F0',
                            style='filled')
        self.graph.add_edge(cur_count, self.visit_args(node.args.args))
        self.graph.add_edge(cur_count, self.visit_body(node))
        return cur_count

    def visit_Return(self, node):
        cur_count = self.count
        self.count += 1
        self.graph.add_node(cur_count, label="Return", shape='s', fillcolor='#F85A62', style='filled')
        self.graph.add_edge(cur_count, self.visit(node.value))
        return cur_count
