import sys
from STree.STree import Tree

class Errors:
    def __init__(self):
        self.type = None
        self.node = None
        self.types = [

        ]

    def err(self, errors_type, node=None):
        self.type = errors_type
        self.node = node
        sys.stderr.write(f'Error {self.types[int(errors_type)]}: ')

        if self.type == 0:
            sys.stderr.write(f' incorrect syntax at '
                             f'{self.node.children[0].lineno} line \n')
            return

class InterpreterRedeclarationError(Exception):
    pass

class InterpreterUndeclaredError(Exception):
    pass

