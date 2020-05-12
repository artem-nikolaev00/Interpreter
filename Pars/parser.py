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
        self.parser = yacc.yacc(module=self)


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
        """statement : declaration SEMICOLON NEWLINE
                     | assignment SEMICOLON NEWLINE
                     | compare SEMICOLON NEWLINE
                     | prison SEMICOLON NEWLINE"""
                    # | while SEMICOLON NEWLINE
                    # | if SEMICOLON NEWLINE
                    # | operator SEMICOLON NEWLINE
                    # | function SEMICOLON NEWLINE
                    # | function_call SEMICOLON NEWLINE"""
        p[0] = p[1]

    def p_declaration(self, p):

        """declaration : type VAR
                       | type VAR ASSIGNMENT expression
                       | CONST type VAR ASSIGNMENT expression
                       | MATRIX type VAR
                       | MATRIX type VAR LBRACKET expression COMMA expression RBRACKET"""
        if len(p) == 3:
            p[0] = Tree('declaration', value=p[1],
                        children=[Tree('init', value=p[2], lineno=p.lineno(2), lexpos=p.lexpos(2))],
                        lineno=p.lineno(2), lexpos=p.lexpos(2))
        elif len(p) == 5:
            p[0] = Tree('declaration', value=p[1],
                        children=[Tree('init', value=p[2], lineno=p.lineno(2), lexpos=p.lexpos(2)), p[4]],
                        lineno=p.lineno(2), lexpos=p.lexpos(2))
        elif len(p) == 6:
            p[0] = Tree('declaration', value=[p[2], p[1]],
                        children=[Tree('init', value=p[3], lineno=p.lineno(3), lexpos=p.lexpos(3)), p[5]],
                        lineno=p.lineno(3), lexpos=p.lexpos(3))
        elif len(p) == 4:
            p[0] = Tree('declaration', value=[p[2], p[1]],
                        children=[Tree('init', value=p[3], lineno=p.lineno(3), lexpos=p.lexpos(3))],
                        lineno=p.lineno(3), lexpos=p.lexpos(3))
        else:
            p[0] = Tree('declaration', value=[p[2], p[1]],
                        children=[Tree('init', value=p[3], lineno=p.lineno(3), lexpos=p.lexpos(3)), p[5], p[7]],
                        lineno=p.lineno(3), lexpos=p.lexpos(3))

    def p_type(self, p):
        """type : SIGNED
                | UNSIGNED
                | CELL"""
        p[0] = p[1]

    def p_expression(self, p):
        """expression : math_expression
                      | const
                      | variable
                      | side
                      | compare
                      | prison
                      | LBRACKET expression RBRACKET"""
        if len(p) == 2:
            p[0] = Tree('expression', children=p[1], lineno=p.lineno(1), lexpos=p.lexpos(1))
        else:
            p[0] = Tree('brackets', value=p[2], children=p[2], lineno=p.lineno(2), lexpos=p.lexpos(2))

    def p_side(self, p):
        """side : LBRACKET directions RBRACKET"""
        p[0] = Tree('diractions', children=p[2], lineno=p.lineno(2), lexpos=p.lexpos(2))

    def p_directions(self, p):
        """directions : direction COMMA directions
                    | direction"""
        if len(p) == 4:
            p[0] = Tree('directions', children=[p[1], p[3]], lineno=p.lineno(1), lexpos=p.lexpos(1))
        else:
            p[0] = Tree('directions', children=p[1], lineno=p.lineno(1), lexpos=p.lexpos(1))

    def p_direction(self, p):
        """direction : TOP
                    | NTOP
                    | LEFT
                    | NLEFT
                    | RIGHT
                    | NRIGHT
                    | DOWN
                    | NDOWN"""
        p[0] = Tree('direction', value=p[1], lineno=p.lineno(1), lexpos=p.lexpos(1))

    def p_compare(self, p):
        """compare : expression EQ expression
                    | expression LESS expression
                    | expression GREATER expression
                    | expression NOTEQ expression"""
        p[0] = Tree('bin_op', value=p[2], children=[p[1], p[3]], lineno=p.lineno(2), lexpos=p.lexpos(2))


    def p_math_expression(self, p):
        """math_expression : expression PLUS expression
                        | expression MINUS expression
                        | expression STAR expression
                        | expression DIV expression
                        | expression PROCENT expression"""
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

    def p_error(self, p):
        try:
            sys.stderr.write(f'Error at {p.lineno} line\n')
        except:
            sys.stderr.write(f'Error\n')
        self.ok = False

    def p_prison(self, p):
        """prison : SHARP variable"""
        p[0] = Tree('prison', value=p[1], children=p[2], lineno=p.lineno(2), lexpos=p.lexpos(2))

    def p_assignment(self, p):
        """assignment : variable ASSIGNMENT expression"""
        if len(p) == 4:
            p[0] = Tree('assignment', value=p[1], children=p[3], lineno=p.lineno(1), lexpos=p.lexpos(1))

data = '''matrix cell a (3,3);
const unsigned a <- 1 + 1;
a <- 1 + 1;
a <- (1 + 1) + 1;
a > b;
#a;
a <- #r;

cell a <- (top);
unsigned b <- 3;
a <- b + 3;


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