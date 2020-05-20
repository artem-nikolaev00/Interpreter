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

    def __init__(self, var_type, var_value=None, var_const=False):
        self.type = var_type
        self.value = var_value
        self.const = var_const

    def __repr__(self):
        return f'{self.type} {self.value} {self.const}'

    def __eq__(self, other):
        if isinstance(other, Variable):
            return (self.type == other.type and
                    self.value == other.value)
        return NotImplemented


class Matrix:

    def __init__(self, m_type, m_lines=None, m_column=None):
        self.type = m_type
        self.lines = m_lines
        self.column = m_column
        # if self.lines is None and self.column is None:
        #     self.size = None
        # else:
        #     self.size = m_lines * m_column

    def __repr__(self):
        return f'{self.type} {self.lines} {self.column}'


class Converter:

    def __init__(self):
        pass

    def converse(self, type, var, const):
        if const is True:
            if type == var.type:
                return Variable(var.type, var.value, const)
            elif type == 'signed':
                if var.type == 'unsigned':
                    return self.unsigned_to_signed(var, const)
            elif type == 'unsigned':
                if var.type == 'signed':
                    return self.signed_to_unsigned(var, const)
            elif type.find(var.type) != -1:
                return Variable(type, var.value)
        else:
            if type == var.type:
                return var
            elif type == 'signed':
                if var.type == 'unsigned':
                    return self.unsigned_to_signed(var)
            elif type == 'unsigned':
                if var.type == 'signed':
                    return self.signed_to_unsigned(var)
            elif type.find(var.type) != -1:
                return Variable(type, var.value)

    @staticmethod
    def signed_to_unsigned(var, const=False):
        val = uint(var.value)
        return Variable('unsigned', val, const)

    @staticmethod
    def unsigned_to_signed(var, const=False):
        val = int(var.value)
        return Variable('signed', val, const)

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

        elif node.type == 'decl_without_init':
            declaration_type = node.value.value
            declaration_child = node.children
            try:
                self.declare_variable_without_init(declaration_type, declaration_child)
            except InterpreterRedeclarationError:
                self.error.err(self.error_types['RedeclarationError'], node)

        elif node.type == 'declaration':
            declaration_type = node.value.value
            declaration_child = node.children
            try:
                self.declare_variable(declaration_type, declaration_child)
            except InterpreterRedeclarationError:
                self.error.err(self.error_types['RedeclarationError'], node)

        elif node.type == 'const_declaration':
            declaration_const = True
            declaration_type = node.value[0].value
            declaration_child = node.children
            try:
                self.declare_variable(declaration_type, declaration_child, declaration_const)
            except InterpreterRedeclarationError:
                self.error.err(self.error_types['RedeclarationError'], node)

        elif node.type == 'matrix_decl_without_init':
            declaration_type = node.value[0].value
            declaration_child = node.children
            try:
                self.declare_matrix_without_init(declaration_type, declaration_child)
            except InterpreterRedeclarationError:
                self.error.err(self.error_types['RedeclarationError'], node)

        elif node.type == 'expression':
            return self.interpreter_node(node.children)

        elif node.type == 'const':
            return self.const_val(node.value)

        elif node.type == 'variable':
            return self.get_value(node)

        return ''

    def declare_matrix_without_init(self, type, child):
        variable = child[0].value
        expression = Matrix(type)
        self.symbol_table[self.scope][variable] = expression

    def declare_variable_without_init(self, type, child):
        variable = child[0].value
        expression = Variable(type)
        self.symbol_table[self.scope][variable] = expression


    def declare_variable(self, type, child, const=False):
        if len(child) == 2:
            variable = child[0].value
            expression = self.interpreter_node(child[1])
            self.declare(type, variable, expression, const)
        #elif child[1] == 'expression' and child[2] == 'expression':

    def declare(self, type, var, expression, const):
        expression = self.check_type(type, expression, const)
        if var in self.symbol_table[self.scope].keys():
            raise InterpreterRedeclarationError
        else:
            self.symbol_table[self.scope][var] = expression

    def check_type(self, type, exp, const):
        var = ['signed', 'unsigned']
        if type in var and exp.type in var:
            return self.check_var(type, exp, const)
        else:
            raise InterpreterTypeError

    def check_var(self, type, exp, const):
        exp = self.converter.converse(type, exp, const)
        return exp

    def const_val(self, value):
        if type(value) == int:
            return Variable('signed', value)
        elif type(value) == str:
            val = self.converter.string_to_uint(value)
            return Variable('unsigned', val)

    def get_value(self, node):
        if node.value in self.symbol_table[self.scope].keys():
            return self.symbol_table[self.scope][node.value]


data = '''matrix signed a;

'''

a = Interpreter()
a.interpreter(data)
pass