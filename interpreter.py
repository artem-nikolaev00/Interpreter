import sys
from STree.STree import Tree
from Pars.parser import Parser
from Errors.Errors import Errors
from Errors.Errors import InterpreterRedeclarationError


class Converter:
    def __init__(self):
        pass


class Interpreter:

    def __init__(self, parser=Parser(), converter=Converter()):
        self.parser = parser
        self.converter = converter
        self.program = None
        self.symbol_table = [dict()]
        self.tree = None
        self.functions = None
        self.scope = 0
        self.error = Errors()
        self.error_types = {

        }

    def interpreter(self, program=None):
        self.program = program
        self.symbol_table = [dict()]
        self.tree, tmp, self.functions = self.parser.parse(self.program)
        if tmp:
            self.interpreter_tree(self.tree)
            self.interpreter_node(self.tree)
        else:
            sys.stderr.write(f'Can\'t interpretate this program. Incorrect syntax!\n')

    def interpreter_tree(self, tree):
        print("Program tree:\n")
        tree.print()
        print('\n')

    def interpreter_node(self, node):
        if node is None:
            return

        if node.type == 'error':
            self.error.err()

        elif node.type == 'program':
            self.interpreter_node(node.children)

        elif node.type == 'state':
            for child in node.children:
                self.interpreter_node(child)
        elif node.type == 'statement':
            self.interpreter_node(node.children)

        elif node.type == 'declaration':
            declaration_type = node.value.value
            declaration_child = node.children
            try:
                self.declare_variable(declaration_type, declaration_child)
            except InterpreterRedeclarationError:
                self.error.err(self.error_types['RedeclarationError'], node)

    def declare_variable(self, type, child):
        if child[1].type == 'expression':
            variable = child[0].value
            expression = self.interpreter_node(child[1])
            self.declare(type, variable, expression)