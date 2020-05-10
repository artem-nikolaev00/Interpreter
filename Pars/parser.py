import sys
import os

import ply.yacc as yacc
from ply.lex import LexError
from Lex.lexer import Lexer
from STree.STree import Tree

class Parser():
    tokens = Lexer().tokens

    def __init__(self):
        self.ok = True
        self.lexer = Lexer()
        self.parser = yacc.yacc(module=self, optimize=1, debug=False, write_tables=False)


    def parse(self, t):
        try:
            res = self.parser.parse(t)
            return res
        except LexError:
            sys.stderr.write(f'Illegal token {t}\n')

    def p_program(self, p):
        """program : state"""
        p[0] = Tree('program', children=p[1], lineno=p.lineno(1), lexpos=p.lexpos(1))

    def p_state(self, p):
        """state : state statement
                | statement"""
        if len(p) == 2:
            p[0] = Tree('state', children=[p[1]])
        else:
            p[0] = Tree('state', children=[p[1], p[2]])

    def p_statement(self, p):
        """statement : declaration SEMICOLON NEWLINE"""
                    # | assignment NEWLINE
                    # | while NEWLINE
                    # | if NEWLINE
                    # | operator NEWLINE
                    # | function NEWLINE
                    # | function_call NEWLINE"""
        p[0] = p[1]

    def p_declaration(self, p):

        """declaration : type VAR
                       | type VAR ASSIGNMENT expression
                       | CONST type VAR ASSIGNMENT expression"""
        if len(p) == 3:
            p[0] = Tree('declaration', value=p[1],
                        children=[Tree('init', value=p[2], lineno=p.lineno(2), lexpos=p.lexpos(2))],
                        lineno=p.lineno(2), lexpos=p.lexpos(2))

        elif len(p) == 5:
            p[0] = Tree('declaration', value=p[1],
                        children=[Tree('init', value=p[2], lineno=p.lineno(2), lexpos=p.lexpos(2)), p[4]],
                        lineno=p.lineno(2), lexpos=p.lexpos(2))
        else:
            p[0] = Tree('declaration', value=[p[2], p[1]],
                        children=[Tree('init', value=p[3], lineno=p.lineno(3), lexpos=p.lexpos(3)), p[5]],
                        lineno=p.lineno(3), lexpos=p.lexpos(3))

    def p_type(self, p):
        """type : SIGNED
                | UNSIGNED
                | CELL
                | MATRIX"""
        p[0] = p[1]

    def p_expression(self, p):
        """expression : math_expression
                      | const
                      | variable"""
        p[0] = Tree('expression', children=p[1], lineno=p.lineno(1), lexpos=p.lexpos(1))

    def p_math_expression(self, p):
        """math_expression : expression PLUS expression
                        | expression MINUS expression"""
        # if len(p) == 3 and p[2] == '+':
        #     p[0] = Tree('bin_op', value=p[2], children=[p[1], p[3]], lineno=p.lineno(1), lexpos=p.lexpos(1))
        # else:
        p[0] = Tree('bin_op', value=p[2], children=[p[1], p[3]], lineno=p.lineno(2), lexpos=p.lexpos(2))

    def p_const(self, p):
        """const : DECIMAL"""
        p[0] = Tree('const', value=p[1], lineno=p.lineno(1), lexpos=p.lexpos(1))

    def p_variable(self, p):
        """variable : VAR
                    | VAR LBRACKET index RBRACKET LBRACKET index RBRACKET"""
        if len(p) == 2:
            p[0] = Tree('variable', p[1], lineno=p.lineno(1), lexpos=p.lexpos(1))
        else:
            p[0] = Tree('indexing', p[1], children=[p[3], p[6]], lineno=p.lineno(1), lexpos=p.lexpos(1))

    def p_index(self, p):
        """index : UNSIGNED"""
        p[0] = p[1]

data = '''unsigned a <- 1 + 1;
'''

lexer = Lexer()
lexer.input(data)
while True:
    token = lexer.token()
    if token is None:
        break
    else:
        print(token)

parser = Parser()
tree = parser.parse(data)
tree.print()