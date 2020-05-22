import sys
import re
from numpy import uint, dtype
from STree.STree import Tree
from Pars.parser import Parser
from Errors.Errors import Errors
from Errors.Errors import InterpreterRedeclarationError
from Errors.Errors import InterpreterTypeError
from Errors.Errors import InterpreterConvertationError
from Errors.Errors import InterpreterIndexError
from Errors.Errors import InterpreterNameError


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


class Cell:

    def __init__(self, c_top=False, c_right=False, c_left=False, c_down=False, c_const=False):
        self.type = 'cell'
        self.const = c_const
        if isinstance(c_right, bool):
            if c_right:
                self.right = True
            else:
                self.right = False
        elif c_right == 'nright':
            self.right = False
        elif c_right == 'right':
            self.right = True

        if isinstance(c_left, bool):
            if c_left:
                self.left = True
            else:
                self.left = False
        elif c_left == 'nleft':
            self.left = False
        elif c_left == 'left':
            self.left = True

        if isinstance(c_top, bool):
            if c_top:
                self.top = True
            else:
                self.top = False
        elif c_top == 'ntop':
            self.top = False
        elif c_top == 'top':
            self.top = True

        if isinstance(c_down, bool):
            if c_down:
                self.down = True
            else:
                self.down = False
        elif c_down == 'ndown':
            self.down = False
        elif c_down == 'down':
            self.down = True

    def __repr__(self):
        return f'{self.top} {self.left} {self.right} {self.down}'



class Matrix:

    def __init__(self, m_type, m_lines=None, m_column=None):
        self.type = m_type
        self.lines = m_lines
        self.column = m_column
        self.value = []
        if self.lines is not None and self.column is not None:
           for i in range(m_lines):
               for j in range(m_column):
                   self.value.append(None)

    def __repr__(self):
        return f'{self.type} {self.lines} {self.column}'


class Converter:

    def __init__(self):
        pass

    def converse(self, type, var, const):
        if const is True:
            if type == var.type:
                if type == 'cell':
                    return Cell(c_top=var.top, c_right=var.right, c_left=var.left, c_down=var.down, c_const=const)
                else:
                    return Variable(var.type, var.value, const)
            elif type == 'signed':
                if var.type == 'unsigned':
                    return self.unsigned_to_signed(var, const)
                elif var.type == 'cell':
                    return self.cell_to_signed(var, const)
            elif type == 'unsigned':
                if var.type == 'signed':
                    return self.signed_to_unsigned(var, const)
                elif var.type == 'cell':
                    return self.cell_to_unsigned(var, const)
            elif type == 'cell':
                if var.type == 'signed':
                    return self.signed_to_cell(var, const)
                elif var.type == 'unsigned':
                    return self.unsigned_to_cell(var, const)
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
    def signed_to_cell(var, const=False):
        if var.value == 0:
            return Cell()
        elif var.value != 0:
            return Cell(True, True, True, True, const)

    @staticmethod
    def unsigned_to_cell(var, const=False):
        if var.value == 0:
            return Cell()
        elif var.value != 0:
            return Cell(True, True, True, True, const)

    @staticmethod
    def cell_to_signed(var, const=False):
        if not var.top and not var.right and not var.left and not var.down:
            val = int(0)
            return Variable('signed', val, const)
        else:
            val = int(1)
            return Variable('signed', val, const)

    @staticmethod
    def cell_to_unsigned(var, const=False):
        if not var.top and not var.right and not var.left and not var.down:
            val = uint(0)
            return Variable('unsigned', val, const)
        else:
            val = uint(1)
            return Variable('unsigned', val, const)

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

    @staticmethod
    def neg_to_int(lst):
        if len(lst) == 2:
            sign = lst[0]
            value = lst[1]
            if isinstance(value, int):
                value = str(value)
            else:
                raise InterpreterConvertationError
            sign += value
            sign = int(sign)
            return sign
        else:
            raise InterpreterConvertationError



class Interpreter:

    def __init__(self, parser=Parser(), converter=Converter()):
        self.parser = parser
        self.converter = converter
        self.check_cell = 0
        self.program = None
        self.symbol_table = [dict()]
        self.tree = None
        self.functions = None
        self.scope = 0
        self.error = Errors()
        self.error_types = {'UnexpectedError': 0,
                            'RedeclarationError': 1,
                            'TypeError': 2,
                            'IndexError': 3,
                            'UndeclaredError': 4}

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
            except InterpreterTypeError:
                self.error.err(self.error_types['TypeError'], node)

        elif node.type == 'declaration':
            declaration_type = node.value.value
            declaration_child = node.children
            try:
                self.declare_variable(declaration_type, declaration_child)
            except InterpreterRedeclarationError:
                self.error.err(self.error_types['RedeclarationError'], node)
            except InterpreterTypeError:
                self.error.err(self.error_types['TypeError'], node)
            except InterpreterNameError:
                self.error.err(self.error_types['UndeclaredError'], node)

        elif node.type == 'const_declaration':
            declaration_const = True
            declaration_type = node.value[0].value
            declaration_child = node.children
            try:
                self.declare_variable(declaration_type, declaration_child, declaration_const)
            except InterpreterRedeclarationError:
                self.error.err(self.error_types['RedeclarationError'], node)
            except InterpreterTypeError:
                self.error.err(self.error_types['TypeError'], node)
            except InterpreterNameError:
                self.error.err(self.error_types['UndeclaredError'], node)

        elif node.type == 'matrix_decl_without_init':
            declaration_type = node.value[0].value
            declaration_child = node.children
            try:
                self.declare_matrix_without_init(declaration_type, declaration_child)
            except InterpreterRedeclarationError:
                self.error.err(self.error_types['RedeclarationError'], node)
            except InterpreterTypeError:
                self.error.err(self.error_types['TypeError'], node)

        elif node.type == 'matrix_declaration':
            declaration_type = node.value[0].value
            declaration_child = node.children
            try:
                self.declare_matrix(declaration_type, declaration_child)
            except InterpreterRedeclarationError:
                self.error.err(self.error_types['RedeclarationError'], node)
            except InterpreterTypeError:
                self.error.err(self.error_types['TypeError'], node)
            except InterpreterIndexError:
                self.error.err(self.error_types['IndexError'], node)
            except InterpreterNameError:
                self.error.err(self.error_types['UndeclaredError'], node)

        elif node.type == 'expression':
            return self.interpreter_node(node.children)

        elif node.type == 'side':
            return self.interpreter_node(node.children)

        elif node.type == 'directions':
            if self.check_cell == 0:
                self.check_cell = 1
            tmp = self.direct(node)
            return self.sides(tmp)

        elif node.type == 'direction':
            if self.check_cell == 0:
                tmp = self.direct(node)
                return self.sides(tmp)
            else:
                return self.interpreter_node(node.children)

        elif node.type == 'dir':
            return [node.value]

        elif node.type == 'const':
            return self.const_val(node.value)

        elif node.type == 'variable':
            return self.get_value(node)

        return ''

    def direct(self, node):
        if isinstance(node.children, list):
            val1 = self.interpreter_node(node.children[0])
            val2 = self.interpreter_node(node.children[1])
            val1 += val2
            return val1
        else:
            val1 = self.interpreter_node(node.children)
            return val1

    def sides(self, lst):
        if isinstance(lst, list):
            tmp_top = False
            tmp_right = False
            tmp_left = False
            tmp_down = False
            for flag in lst:
                if flag == 'top':
                    tmp_top = True
                if flag == 'right':
                    tmp_right = True
                if flag == 'left':
                    tmp_left = True
                if flag == 'down':
                    tmp_down = True
            return Cell(c_top=tmp_top, c_right=tmp_right, c_left=tmp_left, c_down=tmp_down)

    def declare_matrix_without_init(self, type, child):
        var = child[0].value
        if var in self.symbol_table[self.scope].keys():
            raise InterpreterRedeclarationError
        else:
            expression = Matrix(type)
            self.symbol_table[self.scope][var] = expression

    def declare_matrix(self, type, child):
        variable = child[0].value
        expression1 = child[1].children.value
        if isinstance(expression1, str):
            tmp = self.get_value(child[1].children)
            expression1 = tmp.value
        expression2 = child[2].children.value
        if isinstance(expression2, str):
            tmp = self.get_value(child[1].children)
            expression2 = tmp.value
        self.declare_m(type, variable, expression1, expression2)

    def declare_variable_without_init(self, type, child):
        var = child[0].value
        if var in self.symbol_table[self.scope].keys():
            raise InterpreterRedeclarationError
        else:
            if type == 'cell':
                expression = Cell()
            else:
                expression = Variable(type)
            self.symbol_table[self.scope][var] = expression

    def declare_m(self, type, var, exp1, exp2):
        if var in self.symbol_table[self.scope].keys():
            raise InterpreterRedeclarationError
        else:
            try:
                expression = self.check_matrix_index(type, exp1, exp2)
            except InterpreterIndexError:
                raise InterpreterIndexError
            self.symbol_table[self.scope][var] = expression

    def declare_variable(self, type, child, const=False):
        variable = child[0].value
        expression = self.interpreter_node(child[1])
        try:
            self.declare(type, variable, expression, const)
        except InterpreterRedeclarationError:
            raise InterpreterRedeclarationError

    def declare(self, type, var, expression, const):
        expression = self.check_type(type, expression, const)
        if var in self.symbol_table[self.scope].keys():
            raise InterpreterRedeclarationError
        else:
            self.symbol_table[self.scope][var] = expression

    def check_type(self, type, exp, const):
        var = ['signed', 'unsigned', 'cell']
        if type in var and exp.type in var:
            return self.check_var(type, exp, const)
        else:
            raise InterpreterTypeError

    def check_matrix_index(self, type, exp1, exp2):
        if isinstance(exp1, (int, uint)):
            if isinstance(exp2, (int, uint)):
                if exp1 > 0 and exp2 > 0:
                    return Matrix(type, exp1, exp2)
        else:
            raise InterpreterIndexError

    def check_var(self, type, exp, const):
        exp = self.converter.converse(type, exp, const)
        return exp

    def const_val(self, value):
        if type(value) == int:
            return Variable('signed', value)
        elif type(value) == uint:
            return Variable('unsigned', value)
        elif isinstance(value, list):
            if value[0] == '-':
                exp = self.converter.neg_to_int(value)
            return Variable('signed', exp)

    def get_value(self, node):
        if node.value in self.symbol_table[self.scope].keys():
            return self.symbol_table[self.scope][node.value]
        else:
            raise InterpreterNameError

#TODO невозможность (top, ntop), список не больше 4 сторон

data = '''cell a <- (top, down);
'''

a = Interpreter()
a.interpreter(data)
pass