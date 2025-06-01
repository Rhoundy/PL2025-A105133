class Node:
    """Classe base para todos os nós da AST."""
    pass

class ProgramNode(Node):
    def __init__(self, id_node, block_node):
        self.id = id_node
        self.block = block_node
        self.lineno = id_node.lineno

class BlockNode(Node):
    def __init__(self, declarations_node, compound_statement_node):
        self.declarations = declarations_node
        self.compound_statement = compound_statement_node

class DeclarationsNode(Node):
    def __init__(self, items):
        self.items = items

class VarDeclNode(Node):
    def __init__(self, id_list, type_spec):
        self.ids = id_list
        self.type_spec = type_spec
        self.lineno = id_list[0].lineno if id_list else 0

class CompoundStatementNode(Node):
    def __init__(self, statements):
        self.statements = statements

class AssignmentNode(Node):
    def __init__(self, var_node, expr_node):
        self.var = var_node
        self.expr = expr_node
        self.lineno = var_node.lineno

class IfStatementNode(Node):
    def __init__(self, condition_expr, then_statement, else_statement=None):
        self.condition = condition_expr
        self.then_statement = then_statement
        self.else_statement = else_statement
        self.lineno = condition_expr.lineno

class WhileStatementNode(Node):
    def __init__(self, condition_expr, do_statement):
        self.condition = condition_expr
        self.do_statement = do_statement
        self.lineno = condition_expr.lineno

class ForStatementNode(Node):
    def __init__(self, initial_assignment, direction, limit_expr, do_statement):
        self.initial_assignment = initial_assignment
        self.direction = direction
        self.limit_expr = limit_expr
        self.do_statement = do_statement
        self.lineno = initial_assignment.lineno

class ReadLnCallNode(Node):
    def __init__(self, args):
        self.args = args
        self.lineno = args[0].lineno if args else 0

class WriteLnCallNode(Node):
    def __init__(self, args):
        self.args = args
        self.lineno = args[0].lineno if args else 0

class FunctionCallNode(Node):
    def __init__(self, id_node, args):
        self.id = id_node
        self.args = args
        self.lineno = id_node.lineno

class FunctionDeclarationNode(Node):
    def __init__(self, id_node, params, return_type, block):
        self.id = id_node
        self.params = params
        self.return_type = return_type
        self.block = block
        self.lineno = id_node.lineno

class ParameterNode(Node):
    def __init__(self, id_list, type_spec):
        self.ids = id_list
        self.type_spec = type_spec
        self.lineno = id_list[0].lineno if id_list else 0

class BinOpNode(Node):
    def __init__(self, left, op, right, lineno):
        self.left = left
        self.op = op
        self.right = right
        self.lineno = lineno

class UnaryOpNode(Node):
    def __init__(self, op, operand, lineno):
        self.op = op
        self.operand = operand
        self.lineno = lineno

class NumberNode(Node):
    def __init__(self, value, lineno):
        self.value = value
        self.lineno = lineno

class IDNode(Node):
    def __init__(self, name, lineno):
        self.name = name
        self.lineno = lineno

class StringLiteralNode(Node):
    def __init__(self, value, lineno):
        self.value = value
        self.lineno = lineno

class ArrayAccessNode(Node):
    def __init__(self, id_node, index_expr):
        self.id = id_node
        self.index_expr = index_expr
        self.lineno = id_node.lineno