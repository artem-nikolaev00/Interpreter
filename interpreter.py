import sys
import re
from numpy import uint, dtype
from STree.STree import Tree
from Pars.parser import Parser
from Errors.Errors import Errors
from Errors.Errors import InterpreterRedeclarationError
from Errors.Errors import InterpreterTypeError
from Errors.Errors import InterpreterConvertationError



class Variable:
    def __init__(self, var_type, var_value = None):
        self.type = var_type
        self.value = var_value

    def __repr__(self):
        return f'{self.type} {self.value}'

    def __eq__(self, other):
        if isinstance(other, Variable):
            return (self.type == other.type and
                    self.value == other.value)
        return NotImplemented


class Converter:
    def __init__(self):
        pass

    def converse(self, type, var):
        if type == var.type:
            return var
        elif type == 'signed':
            if var.type == 'unsigned':
                val = self.string_to_int(var)
                return Variable('signed', val)
        elif type == 'unsigned':
            if var.type == 'signed':
                val = self.string_to_uint(var)
                return Variable('unsigned', val)
        elif type.find(var.type) != -1:
            return Variable(type, var.value)

    @staticmethod
    def string_to_int(val):
        res = re.findall(r'\d+', val)
        if len(res) != 0:
            return int(res[0])
        else:
            raise InterpreterConvertationError

    @staticmethod
    def string_to_uint(val):
        res = re.findall(r'\d+', val)
        if len(res) != 0:
            return uint(res[0])
        else:
            raise InterpreterConvertationError


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

        elif node.type == 'declaration':
            declaration_type = node.value.value
            declaration_child = node.children
            try:
                self.declare_variable(declaration_type, declaration_child)
            except InterpreterRedeclarationError:
                self.error.err(self.error_types['RedeclarationError'], node)


        return ''

    def declare_variable(self, type, child):
        if child[1] is None:
            variable = child[0].value
            expression = None
            self.declare(type, variable, expression)
        elif child[1] == 'expression' and child[2] is None:
            variable = child[0].value
            expression = self.interpreter_node(child[1])
            self.declare(type, variable, expression)
        elif child[1] == 'expression' and child[2] == 'expression':


    def declare(self, type, var, expression):
        expression = self.check_type(type, expression)
        if var in self.symbol_table[self.scope].keys():
            raise InterpreterRedeclarationError
        else:
            self.symbol_table[self.scope][var] = expression

    def check_type(self, type, exp):
        var = ['signed', 'unsigned']
        if type.find('m') != -1 and exp.type.find('m') != -1:
            return self.check_matrix(type, exp)
        elif type in var and exp.type in var:
            return self.check_var(type, exp)
        else:
            raise InterpreterTypeError

    def check_var(self, type, exp):
        exp = self.converter.converse(type, exp)
        return exp