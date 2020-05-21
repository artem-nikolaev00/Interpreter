import sys
from STree.STree import Tree

class Errors:
    def __init__(self):
        self.type = None
        self.node = None
        self.types = ['UnexpectedError',
                        'RedeclarationError',
                        'TypeError',
                        'IndexError']

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
            sys.stderr.write(f'Bad type for declaration "{self.node.children[0].value}" at line '
                            f'{self.node.lineno}\n')
        elif self.type == 3:
            sys.stderr.write(f'List index is out of range at line '
                             f'{self.node.value[0].lineno}\n')


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

