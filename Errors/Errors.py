import sys
from STree.STree import Tree

class Errors:
    def __init__(self):
        self.type = None
        self.node = None
        self.types = ['UnexpectedError',
                        'RedeclarationError',
                        'TypeError',
                        'IndexError',
                        'UndeclaredError',
                        'SidesError',
                        'ConstError',
                        'NoneError',
                        'UnsignedInitError',
                        'DivError',
                        'ParametrError',
                        'RecursionError']

    def err(self, errors_type, node=None):
        self.type = errors_type
        self.node = node
        sys.stderr.write(f'Error {self.types[int(errors_type)]}: ')

        if self.type == 0:
            sys.stderr.write(f' incorrect syntax at '
                            f'{self.node.children[0].lineno} line \n')
            return
        elif self.type == 1:
            sys.stderr.write(f'Variable "{node.children[0].value}" at line '
                             f'{self.node.lineno} is already declared\n')
        elif self.type == 2:
            if node.type == 'declaration':
                sys.stderr.write(f'Bad type for declaration "{self.node.children[0].value}" at line '
                            f'{self.node.children[0].lineno} or init is not correct\n')
            elif node.type == 'assignment':
                sys.stderr.write(f'non-matching types at line '
                                 f'{self.node.children[0].lineno}\n')
        elif self.type == 3:
            if node.type == 'assignment':
                sys.stderr.write(f'List index is out of range at line '
                                 f'{self.node.children[0].lineno} (Indexing in matrix from 0 to n-1)\n')
            else:
                sys.stderr.write(f'List index is out of range at line '
                             f'{self.node.value[0].lineno} \n')
        elif self.type == 4:
            if node.type == 'if':
                sys.stderr.write(f'Variable for declaration at line "testonce" not very good\n')
            elif node.type == 'while':
                sys.stderr.write(f'Variable for declaration at line "testrep" not very good\n')
            elif node.type == 'assignment':
                sys.stderr.write(f'Variable for declaration at line '
                                 f'{self.node.children[0].lineno} is not used before\n')
            elif node.type == 'function_call':
                sys.stderr.write(f'Variable for declaration at line '
                                 f'{self.node.lineno} is not used before\n')
            else:
                sys.stderr.write(f'Variable for declaration at line '
                                 f'{self.node.children[0].lineno} is not used before\n')
        elif self.type == 5:
            if node.type == 'assignment':
                sys.stderr.write(f'Error at sides of "{self.node.children[0].value}" at line '
                             f'{self.node.children[0].lineno}\n')
            else:
                sys.stderr.write(f'Error at sides of "{self.node.children[0].value}" at line '
                                 f'{self.node.lineno}\n')
        elif self.type == 6:
            sys.stderr.write(f'Impossible reinitialize const variable "{self.node.children[0].value}" at line '
                         f'{self.node.children[0].lineno}\n')
        elif self.type == 7:
            sys.stderr.write(f'Variable "{self.node.value.value}" at line '
                         f'{self.node.value.lineno} initialized by uninitialized variable\n')
        elif self.type == 8:
            sys.stderr.write(f'Impossible to initialize unsigned "{self.node.children[0].value}" at line '
                            f'{self.node.children[0].lineno} because value < 0\n')
        elif self.type == 9:
            sys.stderr.write(f'Div by zero!!!!!  at line '
                            f'{self.node.lineno} because value < 0\n')
        elif self.type == 10:
            sys.stderr.write(f'Parametrs error \n')
        elif self.type == 11:
            sys.stderr.write(f'Recursion error at {self.node.lineno} line\n')






class InterpreterRedeclarationError(Exception):
    pass


class InterpreterUndeclaredError(Exception):
    pass


class InterpreterTypeError(Exception):
    pass


class InterpreterConvertationError(Exception):
    pass


class InterpreterIndexError(Exception):
    pass


class InterpreterNameError(Exception):
    pass


class InterpreterSidesError(Exception):
    pass


class InterpreterConstError(Exception):
    pass


class InterpreterNoneError(Exception):
    pass


class InterpreterUnsignedInitError(Exception):
    pass


class InterpreterDivError(Exception):
    pass


class InterpreterParametrError(Exception):
    pass


class InterpreterRecursionError(Exception):
    pass
