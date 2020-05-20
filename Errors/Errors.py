import sys
from STree.STree import Tree

class Errors:
    def __init__(self):
        self.type = None
        self.node = None
        self.types = ['RedeclarationError'

        ]

    def err(self, errors_type, node=None):
        self.type = errors_type
        self.node = node
        sys.stderr.write(f'Error {self.types[int(errors_type)]}: ')

        if self.type == 0:
            sys.stderr.write(f'Variant "{self.node.children.value}" at line {self.node.lineno} is already declared\n')

class InterpreterRedeclarationError(Exception):
    pass

class InterpreterUndeclaredError(Exception):
    pass

class InterpreterTypeError(Exception):
    pass

class InterpreterConvertationError(Exception):
    pass

