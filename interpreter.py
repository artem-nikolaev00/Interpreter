import sys
import re
import copy
from numpy import uint, dtype
from STree.STree import Tree
from Pars.parser import Parser
from Errors.Errors import Errors
from Errors.Errors import InterpreterRedeclarationError
from Errors.Errors import InterpreterTypeError
from Errors.Errors import InterpreterConvertationError
from Errors.Errors import InterpreterIndexError
from Errors.Errors import InterpreterNameError
from Errors.Errors import InterpreterSidesError
from Errors.Errors import InterpreterConstError
from Errors.Errors import InterpreterNoneError
from Errors.Errors import InterpreterUnsignedInitError
from Errors.Errors import InterpreterDivError
from Errors.Errors import InterpreterParametrError
from Errors.Errors import InterpreterRecursionError


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

        if isinstance(c_left, bool):
            if c_left:
                self.left = True
            else:
                self.left = False

        if isinstance(c_top, bool):
            if c_top:
                self.top = True
            else:
                self.top = False

        if isinstance(c_down, bool):
            if c_down:
                self.down = True
            else:
                self.down = False

    def __repr__(self):
        return f'{self.top} {self.left} {self.right} {self.down}'



class Matrix:

    def __init__(self, m_type, m_lines=None, m_column=None):
        self.const = False
        self.type = m_type
        self.lines = m_lines
        self.column = m_column
        self.value = []
        if self.lines is not None and self.column is not None:
           for i in range(m_lines):
               buf = []
               for j in range(m_column):
                   buf.append(None)
               self.value.append(buf)

    def __repr__(self):
        return f'{self.type} {self.lines} {self.column}'


class Converter:

    def __init__(self):
        pass

    def converse(self, type, var, const=False):
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
                if type == 'cell':
                    return Cell(c_top=var.top, c_right=var.right, c_left=var.left, c_down=var.down)
                else:
                    return Variable(var.type, var.value)
            elif type == 'signed':
                if var.type == 'unsigned':
                    return self.unsigned_to_signed(var)
                elif var.type == 'cell':
                    return self.cell_to_signed(var)
            elif type == 'unsigned':
                if var.type == 'signed':
                    return self.signed_to_unsigned(var)
                elif var.type == 'cell':
                    return self.cell_to_unsigned(var)
            elif type == 'cell':
                if var.type == 'signed':
                    return self.signed_to_cell(var)
                elif var.type == 'unsigned':
                    return self.unsigned_to_cell(var)
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
        self.cell_scope = 0
        self.program = None
        self.symbol_table = [dict()]
        self.tree = None
        self.functions = None
        self.correct = True
        self.scope = 0
        self.error = Errors()
        self.error_types = {'UnexpectedError': 0,
                            'RedeclarationError': 1,
                            'TypeError': 2,
                            'IndexError': 3,
                            'UndeclaredError': 4,
                            'SidesError': 5,
                            'ConstError': 6,
                            'NoneError': 7,
                            'UnsignedInitError': 8,
                            'DivError': 9,
                            'ParametrError': 10,
                            'RecursionError': 11}

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
            except InterpreterSidesError:
                self.error.err(self.error_types['SidesError'], node)
            except InterpreterDivError:
                self.error.err(self.error_types['DivError'], node)

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
            except InterpreterDivError:
                self.error.err(self.error_types['DivError'], node)

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
            except InterpreterDivError:
                self.error.err(self.error_types['DivError'], node)

        elif node.type == 'expression':
            return self.interpreter_node(node.children)

        elif node.type == 'brackets':
            return self.interpreter_node(node.children)

        elif node.type == 'side':
            return self.interpreter_node(node.children)

        elif node.type == 'directions':
            if self.check_cell == 0:
                self.check_cell = 1
            tmp = self.direct(node)
            if self.cell_scope == 0:
                return self.sides(tmp)
            else:
                return tmp

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

        elif node.type == 'indexing':
            var = node.value
            if var not in self.symbol_table[self.scope].keys():
                self.error.err(self.error_types['UndeclaredError'], node)
            index1 = self.interpreter_node(node.children[0])
            index2 = self.interpreter_node(node.children[1])
            return self.symbol_table[self.scope][var].value[index1.value][index2.value]

        elif node.type == 'variable':
            return self.get_value(node)

        elif node.type == 'assignment':
            var = node.value.value
            index1 = None
            index2 = None
            _const = False
            if var not in self.symbol_table[self.scope].keys():
                self.error.err(self.error_types['UndeclaredError'], node)
            else:
                if node.value.type == 'indexing':
                    index1 = self.interpreter_node(node.value.children[0])
                    index2 = self.interpreter_node(node.value.children[1])
                try:
                    _type = self.symbol_table[self.scope][var].type
                    if node.value.type != 'indexing':
                        _const = self.symbol_table[self.scope][var].const
                    expression = self.interpreter_node(node.children[1])
                    if not isinstance(self.symbol_table[self.scope][var], Matrix) and\
                            _type == 'unsigned' and expression.value < 0:
                        raise InterpreterUnsignedInitError
                    if node.value.type == 'indexing':
                        self.assign(_type, _const, var, expression, index1.value, index2.value)
                    else:
                        if isinstance(self.symbol_table[self.scope][var], Matrix):
                            self.symbol_table[self.scope][var] = expression
                        else:
                            self.assign(_type, _const, var, expression)
                except InterpreterNameError:
                        self.error.err(self.error_types['UndeclaredError'], node)
                except InterpreterConstError:
                    self.error.err(self.error_types['ConstError'], node)
                except InterpreterNoneError:
                    self.error.err(self.error_types['NoneError'], node)
                except InterpreterIndexError:
                    self.error.err(self.error_types['IndexError'], node)
                except InterpreterUnsignedInitError:
                    self.error.err(self.error_types['UnsignedInitError'], node)
                except InterpreterTypeError:
                    self.error.err(self.error_types['TypeError'], node)
                except InterpreterDivError:
                    self.error.err(self.error_types['DivError'], node)

        elif node.type == 'bin_op':
            try:
                if node.value == '+':
                    return self.bin_plus(node.children[0], node.children[1])
                elif node.value == '-':
                    return self.bin_minus(node.children[0], node.children[1])
                elif node.value == '*':
                    return self.bin_mul(node.children[0], node.children[1])
                elif node.value == '/':
                    return self.bin_div(node.children[0], node.children[1])
                elif node.value == '%':
                    return self.bin_mod(node.children[0], node.children[1])
                elif node.value == '<':
                    return self.logic_less(node.children[0], node.children[1])
                elif node.value == '>':
                    return self.logic_greater(node.children[0], node.children[1])
                elif node.value == '=':
                    return self.logic_eq(node.children[0], node.children[1])
                elif node.value == '<>':
                    return self.logic_noteq(node.children[0], node.children[1])
            except InterpreterDivError:
                raise InterpreterDivError
            except InterpreterTypeError:
                raise InterpreterTypeError
            except InterpreterNameError:
                raise InterpreterNameError

        elif node.type == 'prison':
            try:
                var = node.children.value
                if isinstance(self.symbol_table[self.scope][var], Matrix):
                    if self.symbol_table[self.scope][var].type == 'signed' \
                            or self.symbol_table[self.scope][var].type == 'unsigned':
                        self.average(self.symbol_table[self.scope][var])
                    elif self.symbol_table[self.scope][var].type == 'cell':
                        self.unification(self.symbol_table[self.scope][var])
            except InterpreterTypeError:
                raise InterpreterTypeError

        elif node.type == 'if':
            try:
                self.op_if(node)
            except InterpreterConvertationError:
                self.error.err(self.error_types['ConvertationError'], node)
            except InterpreterTypeError:
                self.error.err(self.error_types['TypeError'], node)
            except InterpreterNameError:
                self.error.err(self.error_types['UndeclaredError'], node)

        elif node.type == 'while':
            try:
                self.op_while(node)
            except InterpreterConvertationError:
                self.error.err(self.error_types['ConvertationError'], node)
            except InterpreterTypeError:
                self.error.err(self.error_types['TypeError'], node)
            except InterpreterNameError:
                self.error.err(self.error_types['UndeclaredError'], node)

        elif node.type == 'var':
            val1 = None
            if node.children is not None:
                val1 = self.interpreter_node(node.children)
            val2 = [node.value]
            if val1 is not None:
                val2 += val1
            return val2

        elif node.type == 'func':
            if self.scope != 0:
                self.correct = False
                self.error.err(self.error_types['FuncDescriptionError'], node)

        elif node.type == 'function_call':
            if node.children is not None:
                param = self.interpreter_node(node.children)
                if isinstance(param, list):
                    res = self.func_call(node.value['name'], param)
            else:
                param = None
                try:
                    res = self.func_call(node.value['name'], param)
                except InterpreterParametrError:
                    self.error.err(self.error_types['ParametrError'], node)
                    self.correct = False
                    res = 0
            return res

        elif node.type == 'return':
            if self.scope == 0:
                self.error.err(self.error_types['FuncStatementsError'], node)
                self.correct = False
            elif '#RETURN' in self.symbol_table[self.scope].keys():
                pass
            else:
                self.symbol_table[self.scope]['#RETURN'] = self.interpreter_node(node.children)



        return ''

    def func_call(self, name, parametr=None):
        if name not in self.functions.keys():
            raise InterpreterNameError
        self.scope += 1
        if self.scope > 100:
            self.scope -= 1
            raise InterpreterRecursionError
        self.symbol_table.append(dict())
        if parametr is not None:
            self.symbol_table[self.scope]['PARAM'] = parametr
        self.interpreter_node(self.functions[name].children['body'])
        if '#RETURN' in self.symbol_table[self.scope].keys():
            result = copy.deepcopy(self.symbol_table[self.scope]['#RETURN'])
        else:
            result = None
        self.symbol_table.pop()
        self.scope -= 1
        return result

    def op_if(self, node):
        condition = self.interpreter_node(node.children['condition'])
        if condition != 0:
            self.interpreter_node(node.children['body'])

    def op_while(self, node):
        condition = self.interpreter_node(node.children['condition'])
        while condition != 0:
            self.interpreter_node(node.children['body'])
            condition = self.interpreter_node(node.children['condition'])


    def unification(self, matr):
        for i in range(matr.lines):
            for j in range(matr.column):
                if matr.value[i][j] is not None:
                    if i - 1 > -1:
                        if matr.value[i][j].top == True:
                            if matr.value[i - 1][j] is not None:
                                matr.value[i - 1][j].down = True
                            else:
                                matr.value[i - 1][j] = Cell(c_down=True)
                    if i + 1 < matr.lines:
                        if matr.value[i][j].down == True:
                            if matr.value[i + 1][j] is not None:
                                matr.value[i + 1][j].top = True
                            else:
                                matr.value[i + 1][j] = Cell(c_top=True)
                    if j -1  > -1:
                        if matr.value[i][j].left == True:
                            if matr.value[i][j - 1] is not None:
                                matr.value[i][j - 1].right = True
                            else:
                                matr.value[i][j - 1] = Cell(c_right=True)
                    if j + 1 < matr.lines:
                        if matr.value[i][j].right == True:
                            if matr.value[i][j + 1] is not None:
                                matr.value[i][j + 1].left = True
                            else:
                                matr.value[i][j + 1] = Cell(c_left=True)

    def average(self, matr):
        tmp = 0
        count = 0
        for i in range(matr.lines):
            for j in range(matr.column):
                if matr.value[i][j] is not None:
                    tmp += matr.value[i][j].value
                    count += 1
        if count > 0:
            tmp = tmp // count
        for i in range(matr.lines):
            for j in range(matr.column):
                matr.value[i][j] = tmp

    def logic_noteq(self, var1, var2):
        expr1 = self.interpreter_node(var1)
        expr2 = self.interpreter_node(var2)
        if isinstance(expr1, Matrix) or isinstance(expr2, Matrix):
            raise InterpreterTypeError
        elif expr1.type == 'cell' or expr2.type == 'cell':
            raise InterpreterTypeError
        else:
            if expr1.value != expr2.value:
                return 1
            else:
                return 0

    def logic_eq(self, var1, var2):
        expr1 = self.interpreter_node(var1)
        expr2 = self.interpreter_node(var2)
        if isinstance(expr1, Matrix) or isinstance(expr2, Matrix):
            raise InterpreterTypeError
        elif expr1.type == 'cell' or expr2.type == 'cell':
            raise InterpreterTypeError
        else:
            if expr1.value == expr2.value:
                return 1
            else:
                return 0

    def logic_less(self, var1, var2):
        expr1 = self.interpreter_node(var1)
        expr2 = self.interpreter_node(var2)
        if isinstance(expr1, Matrix) or isinstance(expr2, Matrix):
            raise InterpreterTypeError
        elif expr1.type == 'cell' or expr2.type == 'cell':
            raise InterpreterTypeError
        else:
            if expr1.value < expr2.value:
                return 1
            else:
                return 0

    def logic_greater(self, var1, var2):
        expr1 = self.interpreter_node(var1)
        expr2 = self.interpreter_node(var2)
        if isinstance(expr1, Matrix) or isinstance(expr2, Matrix):
            raise InterpreterTypeError
        elif expr1.type == 'cell' or expr2.type == 'cell':
            raise InterpreterTypeError
        else:
            if expr1.value > expr2.value:
                return 1
            else:
                return 0

    def bin_plus(self, var1, var2):
        expr1 = self.interpreter_node(var1)
        expr2 = self.interpreter_node(var2)
        if isinstance(expr1, Matrix) and isinstance(expr2, Matrix):
            if expr1.lines <= expr2.lines:
                lines = expr1.lines
            else:
                lines = expr2.lines
            if expr1.column <= expr2.column:
                column = expr1.column
            else:
                column = expr2.column
            tmp = Matrix('signed', lines, column)
            val = []
            for i in range(lines):
                buf = []
                for j in range(column):
                    if expr1.value[i][j] is not None and expr2.value[i][j] is not None:
                        num = expr1.value[i][j].value + expr2.value[i][j].value
                        buf.append(Variable('signed', num))
                    elif expr1.value[i][j] is not None:
                        buf.append(expr1.value[i][j])
                    elif expr2.value[i][j] is not None:
                        buf.append(expr2.value[i][j])
                    else:
                        buf.append(None)
                val.append(buf)
            tmp.value = val
            return tmp
        elif (expr1.type == 'signed' or expr1.type == 'unsigned') and\
                (expr2.type == 'signed' or expr2.type == 'unsigned')\
                and isinstance(expr1, Variable) and isinstance(expr2, Variable):
            expr1 = self.converter.converse('signed', self.interpreter_node(var1))
            expr2 = self.converter.converse('signed', self.interpreter_node(var2))
            return Variable('signed', expr1.value + expr2.value)
        elif expr1.type == 'cell' and expr2.type == 'cell':
            top = expr1.top or expr2.top
            left = expr1.left or expr2.left
            right = expr1.right or expr2.right
            down = expr1.down or expr2.down
            return Cell(c_top=top, c_down=down, c_left=left, c_right=right)
        else:
            raise InterpreterTypeError

    def bin_minus(self, var1, var2):
        expr1 = self.interpreter_node(var1)
        expr2 = self.interpreter_node(var2)
        if isinstance(expr1, Matrix) and isinstance(expr2, Matrix):
            if expr1.lines <= expr2.lines:
                lines = expr1.lines
            else:
                lines = expr2.lines
            if expr1.column <= expr2.column:
                column = expr1.column
            else:
                column = expr2.column
            tmp = Matrix('signed', lines, column)
            val = []
            for i in range(lines):
                buf = []
                for j in range(column):
                    if expr1.value[i][j] is not None and expr2.value[i][j] is not None:
                        if expr1.value[i][j].type == 'unsigned':
                            num = expr1.value[i][j].value - expr2.value[i][j].value
                            if num < 0:
                                raise InterpreterUnsignedInitError
                        else:
                            num = expr1.value[i][j].value - expr2.value[i][j].value
                        buf.append(Variable('signed', num))
                    elif expr1.value[i][j] is not None:
                        buf.append(expr1.value[i][j])
                    elif expr2.value[i][j] is not None:
                        buf.append(expr2.value[i][j])
                    else:
                        buf.append(None)
                val.append(buf)
            tmp.value = val
            return tmp
        elif (expr1.type == 'signed' or expr1.type == 'unsigned') and \
                (expr2.type == 'signed' or expr2.type == 'unsigned') \
                and isinstance(expr1, Variable) and isinstance(expr2, Variable):
            expr1 = self.converter.converse('signed', self.interpreter_node(var1))
            expr2 = self.converter.converse('signed', self.interpreter_node(var2))
            return Variable('signed', expr1.value - expr2.value)
        elif expr1.type == 'cell' and expr2.type == 'cell':
            top = expr1.top ^ expr2.top
            left = expr1.left ^ expr2.left
            right = expr1.right ^ expr2.right
            down = expr1.down ^expr2.down
            return Cell(c_top=top, c_down=down, c_left=left, c_right=right)
        else:
            raise InterpreterTypeError

    def bin_mul(self, var1, var2):
        expr1 = self.interpreter_node(var1)
        expr2 = self.interpreter_node(var2)
        if isinstance(expr1, Matrix) and isinstance(expr2, Matrix):
            if expr1.lines <= expr2.lines:
                lines = expr1.lines
            else:
                lines = expr2.lines
            if expr1.column <= expr2.column:
                column = expr1.column
            else:
                column = expr2.column
            tmp = Matrix('signed', lines, column)
            val = []
            for i in range(lines):
                buf = []
                for j in range(column):
                    if expr1.value[i][j] is not None and expr2.value[i][j] is not None:
                        if expr1.value[i][j].type == 'unsigned':
                            num = expr1.value[i][j].value * expr2.value[i][j].value
                            if num < 0:
                                raise InterpreterUnsignedInitError
                        else:
                            num = expr1.value[i][j].value * expr2.value[i][j].value
                        buf.append(Variable('signed', num))
                    elif expr1.value[i][j] is not None:
                        buf.append(expr1.value[i][j])
                    elif expr2.value[i][j] is not None:
                        buf.append(expr2.value[i][j])
                    else:
                        buf.append(None)
                val.append(buf)
            tmp.value = val
            return tmp
        elif (expr1.type == 'signed' or expr1.type == 'unsigned') and \
                (expr2.type == 'signed' or expr2.type == 'unsigned')\
                and isinstance(expr1, Variable) and isinstance(expr2, Variable):
            expr1 = self.converter.converse('signed', self.interpreter_node(var1))
            expr2 = self.converter.converse('signed', self.interpreter_node(var2))
            return Variable('signed', expr1.value * expr2.value)
        elif expr1.type == 'cell' and expr2.type == 'cell':
            top = expr1.top and expr2.top
            left = expr1.left and expr2.left
            right = expr1.right and expr2.right
            down = expr1.down and expr2.down
            return Cell(c_top=top, c_down=down, c_left=left, c_right=right)
        else:
            raise InterpreterTypeError

    def bin_div(self, var1, var2):
        expr1 = self.interpreter_node(var1)
        expr2 = self.interpreter_node(var2)
        if isinstance(expr1, Matrix) and isinstance(expr2, Matrix):
            if expr1.lines <= expr2.lines:
                lines = expr1.lines
            else:
                lines = expr2.lines
            if expr1.column <= expr2.column:
                column = expr1.column
            else:
                column = expr2.column
            tmp = Matrix('signed', lines, column)
            val = []
            for i in range(lines):
                buf = []
                for j in range(column):
                    if expr1.value[i][j] is not None and expr2.value[i][j] is not None:
                        if expr2.value[i][j].value == 0:
                            raise InterpreterDivError
                        if expr1.value[i][j].type == 'unsigned':
                            num = expr1.value[i][j].value // expr2.value[i][j].value
                            if num < 0:
                                raise InterpreterUnsignedInitError
                        else:
                            num = expr1.value[i][j].value // expr2.value[i][j].value
                        buf.append(Variable('signed', num))
                    elif expr1.value[i][j] is not None:
                        buf.append(expr1.value[i][j])
                    elif expr2.value[i][j] is not None:
                        buf.append(expr2.value[i][j])
                    else:
                        buf.append(None)
                val.append(buf)
            tmp.value = val
            return tmp
        elif (expr1.type == 'signed' or expr1.type == 'unsigned') and \
                (expr2.type == 'signed' or expr2.type == 'unsigned')\
                and isinstance(expr1, Variable) and isinstance(expr2, Variable):
            expr1 = self.converter.converse('signed', self.interpreter_node(var1))
            expr2 = self.converter.converse('signed', self.interpreter_node(var2))
            if expr2.value == 0:
                raise InterpreterDivError
            return Variable('signed', expr1.value / expr2.value)
        elif expr1.type == 'cell' and expr2.type == 'cell':
            top = expr1.top ^ expr2.top
            left = expr1.left ^ expr2.left
            right = expr1.right ^ expr2.right
            down = expr1.down ^expr2.down
            return Cell(c_top=top, c_down=down, c_left=left, c_right=right)
        else:
            raise InterpreterTypeError

    def bin_mod(self, var1, var2):
        expr1 = self.interpreter_node(var1)
        expr2 = self.interpreter_node(var2)
        if isinstance(expr1, Matrix) and isinstance(expr2, Matrix):
            if expr1.lines <= expr2.lines:
                lines = expr1.lines
            else:
                lines = expr2.lines
            if expr1.column <= expr2.column:
                column = expr1.column
            else:
                column = expr2.column
            tmp = Matrix('signed', lines, column)
            val = []
            for i in range(lines):
                buf = []
                for j in range(column):
                    if expr1.value[i][j] is not None and expr2.value[i][j] is not None:
                        if expr2.value[i][j].value == 0:
                            raise InterpreterDivError
                        if expr1.value[i][j].type == 'unsigned':
                            num = expr1.value[i][j].value % expr2.value[i][j].value
                            if num < 0:
                                raise InterpreterUnsignedInitError
                        else:
                            num = expr1.value[i][j].value % expr2.value[i][j].value
                        buf.append(Variable('signed', num))
                    elif expr1.value[i][j] is not None:
                        buf.append(expr1.value[i][j])
                    elif expr2.value[i][j] is not None:
                        buf.append(expr2.value[i][j])
                    else:
                        buf.append(None)
                val.append(buf)
            tmp.value = val
            return tmp
        elif (expr1.type == 'signed' or expr1.type == 'unsigned') and \
                (expr2.type == 'signed' or expr2.type == 'unsigned')\
                and isinstance(expr1, Variable) and isinstance(expr2, Variable):
            expr1 = self.converter.converse('signed', self.interpreter_node(var1))
            expr2 = self.converter.converse('signed', self.interpreter_node(var2))
            if expr2.value == 0:
                raise InterpreterDivError
            return Variable('signed', expr1.value % expr2.value)
        elif expr1.type == 'cell' and expr2.type == 'cell':
            top = expr1.top ^ expr2.top
            left = expr1.left ^ expr2.left
            right = expr1.right ^ expr2.right
            down = expr1.down ^ expr2.down
            return Cell(c_top=top, c_down=down, c_left=left, c_right=right)
        else:
            raise InterpreterTypeError

    def direct(self, node):
        if isinstance(node.children, list):
            val1 = self.interpreter_node(node.children[0])
            self.cell_scope += 1
            val2 = self.interpreter_node(node.children[1])
            self.cell_scope -= 1
            val1 += val2
            return val1
        else:
            val1 = self.interpreter_node(node.children)
            return val1

    def sides(self, lst):
        if isinstance(lst, list):
            if len(lst) > 4:
                raise InterpreterSidesError
            for flag in lst:
                if flag == 'top':
                    for flag in lst:
                        if flag == 'ntop':
                            raise InterpreterSidesError
                if flag == 'left':
                    for flag in lst:
                        if flag == 'nleft':
                            raise InterpreterSidesError
                if flag == 'fight':
                    for flag in lst:
                        if flag == 'nright':
                            raise InterpreterSidesError
                if flag == 'down':
                    for flag in lst:
                        if flag == 'ndown':
                            raise InterpreterSidesError
            else:
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
        if isinstance(expression, int) or isinstance(expression, float):
            expression = Variable(type, expression, const)
        if not isinstance(expression, Matrix) and \
                type == 'unsigned' and expression.value < 0:
            raise InterpreterUnsignedInitError
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

    def assign(self, type, const, var, expression, index1=None, index2=None):
        if const:
            raise InterpreterConstError
        if isinstance(self.symbol_table[self.scope][var], Matrix):
            try:
                self.add_to_matr(type, var, expression, index1, index2)
            except InterpreterIndexError:
                raise InterpreterIndexError
        elif type == expression.type:
            if expression.value is None:
                raise InterpreterNoneError
            else:
                self.symbol_table[self.scope][var] = expression
        elif (type == 'signed' or type == 'unsigned' or type == 'cell') and \
                (expression.type == 'signed' or expression.type == 'unsigned' or type == 'cell'):
            self.symbol_table[self.scope][var] = self.check_var(type, expression)

    def add_to_matr(self, type, var, expression, index1, index2):
        if index1 < self.symbol_table[self.scope][var].lines:
            if index2 < self.symbol_table[self.scope][var].column:
                if type == expression.type:
                    self.symbol_table[self.scope][var].value[index1][index2] = expression
                elif type == 'signed':
                    if expression.type == 'unsigned':
                        tmp = self.converter.unsigned_to_signed(expression)
                        self.symbol_table[self.scope][var].value[index1][index2] = tmp
                    elif expression.type == 'cell':
                        tmp = self.converter.cell_to_signed(expression)
                        self.symbol_table[self.scope][var].value[index1][index2] = tmp
                elif type == 'unsigned':
                    if expression.type == 'signed':
                        tmp = self.converter.signed_to_unsigned(expression)
                        self.symbol_table[self.scope][var].value[index1][index2] = tmp
                    elif expression.type == 'cell':
                        tmp = self.converter.cell_to_unsigned(expression)
                        self.symbol_table[self.scope][var].value[index1][index2] = tmp
                elif type == 'cell':
                    if expression.type == 'signed':
                        tmp = self.converter.signed_to_cell(expression)
                        self.symbol_table[self.scope][var].value[index1][index2] = tmp
                    elif expression.type == 'unsigned':
                        tmp = self.converter.unsigned_to_cell(expression)
                        self.symbol_table[self.scope][var].value[index1][index2] = tmp
            else:
                raise InterpreterIndexError
        elif index1 >= self.symbol_table[self.scope][var].lines:
            raise InterpreterIndexError

    def check_var(self, type, exp, const=False):
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

#TODO разобраться с unsigned матрицами(если обе un, то пусть возвр un)

data = '''matrix signed a(3, 3);
signed i <- 0;
signed j <- 0;
testrep(i < 3)(
    testrep(j < 3)(
        a(i, j) <- i + j;
        j <- j + 1;
    )
    i <- i + 1;
    j <- 0;
)

i <- 0;
j <- 0;
signed tmp;
signed len <- 9;

testrep(i < 3)(
    testrep(j < 3)(
        testonce(a(
    )
    i <- i + 1;
    j <- 0;
)

'''

a = Interpreter()
a.interpreter(data)
pass