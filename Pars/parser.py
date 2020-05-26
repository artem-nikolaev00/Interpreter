import sys
import os

import ply.yacc as yacc
from ply.lex import LexError
from Lex.lexer import Lexer
from STree.STree import Tree

class Parser():
    tokens = Lexer().tokens
    precedence = Lexer.precedence

    def __init__(self):
        self.ok = True
        self.lexer = Lexer()
        self.parser = yacc.yacc(module=self)
        self.functions = dict()


    def parse(self, t):
        try:
            res = self.parser.parse(t)
            return res,  self.ok, self.functions
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
                     | prison SEMICOLON NEWLINE
                     | if NEWLINE
                     | while NEWLINE
                     | robot SEMICOLON NEWLINE
                     | function NEWLINE
                     | function_call SEMICOLON NEWLINE
                     | function_return SEMICOLON NEWLINE"""
        p[0] = p[1]

    def p_statement_error_no_nl(self, p):
        """statement : declaration SEMICOLON
                     | assignment SEMICOLON
                     | compare SEMICOLON
                     | prison SEMICOLON
                     | if
                     | while
                     | robot SEMICOLON
                     | function
                     | function_call SEMICOLON
                     | function_return SEMICOLON """
        p[0] = Tree('error', value="NEWLINE is absent", lineno=p.lineno(1), lexpos=p.lexpos(1))
        sys.stderr.write(f'-> NEWLINE is absent. <-\n')

    def p_statement_error(self, p):
        """statement : declaration error NEWLINE
                     | assignment error NEWLINE
                     | compare error NEWLINE
                     | prison error NEWLINE
                     | robot error NEWLINE
                     | function_call error NEWLINE
                     | function_return error NEWLINE"""
        p[0] = Tree('error', value="SEMICOLON is absent", children=p[2], lineno=p.lineno(1), lexpos=p.lexpos(1))
        sys.stderr.write(f'-> SEMICOLON is absent <-\n')

    def p_declaration(self, p):

        """declaration : type VAR
                       | type VAR ASSIGNMENT expression
                       | CONST type VAR ASSIGNMENT expression
                       | MATRIX type VAR
                       | MATRIX type VAR LBRACKET expression COMMA expression RBRACKET"""
        if len(p) == 3:
            p[0] = Tree('decl_without_init', value=p[1],
                        children=[Tree('init', value=p[2], lineno=p.lineno(2), lexpos=p.lexpos(2))],
                        lineno=p.lineno(2), lexpos=p.lexpos(2))
        elif len(p) == 5:
            p[0] = Tree('declaration', value=p[1],
                        children=[Tree('init', value=p[2], lineno=p.lineno(2), lexpos=p.lexpos(2)), p[4]],
                        lineno=p.lineno(2), lexpos=p.lexpos(2))
        elif len(p) == 6:
            p[0] = Tree('const_declaration', value=[p[2], p[1]],
                        children=[Tree('init', value=p[3], lineno=p.lineno(3), lexpos=p.lexpos(3)), p[5]],
                        lineno=p.lineno(3), lexpos=p.lexpos(3))
        elif len(p) == 4:
            p[0] = Tree('matrix_decl_without_init', value=[p[2], p[1]],
                        children=[Tree('init', value=p[3], lineno=p.lineno(3), lexpos=p.lexpos(3))],
                        lineno=p.lineno(3), lexpos=p.lexpos(3))
        else:
            p[0] = Tree('matrix_declaration', value=[p[2], p[1]],
                        children=[Tree('init', value=p[3], lineno=p.lineno(3), lexpos=p.lexpos(3)), p[5], p[7]],
                        lineno=p.lineno(3), lexpos=p.lexpos(3))

    def p_declaration_error(self, p):
        """declaration : error VAR
                        | error VAR ASSIGNMENT expression
                        | CONST error VAR ASSIGNMENT expression
                        | MATRIX error VAR
                       | MATRIX error VAR LBRACKET expression COMMA expression RBRACKET"""
        if p[1] == 'const':
            p[0] = Tree('error', value='TYPE ERROR', children=p[2], lineno=p.lineno(2), lexpos=p.lexpos(2))
            sys.stderr.write(f'-> Error in TYPE of declarated varible <-\n')
        elif p[1] == 'matrix':
            p[0] = Tree('error', value='TYPE ERROR', children=p[2], lineno=p.lineno(2), lexpos=p.lexpos(2))
            sys.stderr.write(f'-> Error in TYPE of declarated varible <-\n')
        else:
            p[0] = Tree('error', value='TYPE ERROR',  children=p[1], lineno=p.lineno(1), lexpos=p.lexpos(1))
            sys.stderr.write(f'-> Error in TYPE of declarated varible <-\n')

    def p_type(self, p):
        """type : SIGNED
                | UNSIGNED
                | CELL"""
        p[0] = Tree('type', value=p[1], children=[], lineno=p.lineno(1), lexpos=p.lexpos(1))

    def p_expression(self, p):
        """expression : math_expression
                      | const
                      | variable
                      | side
                      | compare
                      | robot
                      | prison
                      | function_call
                      | LBRACKET expression RBRACKET"""
        if len(p) == 2:
            p[0] = Tree('expression', children=p[1], lineno=p.lineno(1), lexpos=p.lexpos(1))
        else:
            p[0] = Tree('brackets', value=p[2], children=p[2], lineno=p.lineno(2), lexpos=p.lexpos(2))

    def p_side(self, p):
        """side : LBRACKET directions RBRACKET"""
        p[0] = Tree('side', children=p[2], lineno=p.lineno(2), lexpos=p.lexpos(2))

    def p_side_error(self, p):
        """side : LBRACKET error RBRACKET"""
        p[0] = Tree('error', value='SIDE ERROR', children=p[2], lineno=p.lineno(2), lexpos=p.lexpos(2))
        sys.stderr.write(f'-> Error in SIDE of declarated varible <-\n')

    def p_directions(self, p):
        """directions : direction COMMA directions
                    | direction"""
        if len(p) == 4:
            p[0] = Tree('directions', children=[p[1], p[3]], lineno=p.lineno(1), lexpos=p.lexpos(1))
        else:
            p[0] = Tree('direction', children=p[1], lineno=p.lineno(1), lexpos=p.lexpos(1))

    def p_direction(self, p):
        """direction : TOP
                    | NTOP
                    | LEFT
                    | NLEFT
                    | RIGHT
                    | NRIGHT
                    | DOWN
                    | NDOWN
                    | BOTTOM"""
        p[0] = Tree('dir', value=p[1], lineno=p.lineno(1), lexpos=p.lexpos(1))

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
        p[0] = Tree('bin_op', value=p[2], children=[p[1], p[3]], lineno=p.lineno(2), lexpos=p.lexpos(2))

    def p_const(self, p):
        """const : DECIMAL
                | UDECIMAL
                | MINUS DECIMAL"""
        if len(p) == 2:
            p[0] = Tree('const', value=p[1], lineno=p.lineno(1), lexpos=p.lexpos(1))
        else:
            p[0] = Tree('const', value=[p[1], p[2]], lineno=p.lineno(1), lexpos=p.lexpos(1))

    def p_variable(self, p):
        """variable : VAR
                    | VAR LBRACKET index COMMA index RBRACKET"""
        if len(p) == 2:
            p[0] = Tree('variable', p[1], lineno=p.lineno(1), lexpos=p.lexpos(1))
        else:
            p[0] = Tree('indexing', p[1], children=[p[3], p[5]], lineno=p.lineno(1), lexpos=p.lexpos(1))

    def p_index(self, p):
        """index : expression"""
        p[0] = p[1]

    def p_prison(self, p):
        """prison : SHARP variable"""
        p[0] = Tree('prison', value=p[1], children=p[2], lineno=p.lineno(2), lexpos=p.lexpos(2))

    def p_assignment(self, p):
        """assignment : variable ASSIGNMENT expression"""
        if len(p) == 4:
            p[0] = Tree('assignment', value=p[1], children=[p[1], p[3]], lineno=p.lineno(1), lexpos=p.lexpos(1))

    def p_assignment_err(self, p):
        """assignment : variable ASSIGNMENT error"""
        p[0] = Tree('error', value="Wrong assignment", lineno=p.lineno(1), lexpos=p.lexpos(1))
        sys.stderr.write(f'-> Wrong assignment <-\n')

    def p_if(self, p):
        """if : TESTONCE LBRACKET math_expression RBRACKET LBRACKET NEWLINE state RBRACKET
              | TESTONCE LBRACKET compare RBRACKET LBRACKET NEWLINE state RBRACKET"""
        p[0] = Tree('if', children={'condition': p[3], 'body': p[7]}, lineno=p.lineno(1), lexpos=p.lexpos(1))

    def p_if_error(self, p):
        """if : TESTONCE error"""
        p[0] = Tree('error', value="Incorrect if", lineno=p.lineno(2), lexpos=p.lexpos(2))
        sys.stderr.write(f'-> Incorrect if <-\n')

    def p_while(self, p):
        """while : TESTREP LBRACKET math_expression RBRACKET LBRACKET NEWLINE state RBRACKET
              | TESTREP LBRACKET compare RBRACKET LBRACKET NEWLINE state RBRACKET"""
        p[0] = Tree('while', children={'condition': p[3], 'body': p[7]}, lineno=p.lineno(1), lexpos=p.lexpos(1))

    def p_while_error(self, p):
        """while : TESTREP error"""
        p[0] = Tree('error', value="Incorrect for", lineno=p.lineno(2), lexpos=p.lexpos(2))
        sys.stderr.write(f'-> Incorrect for <-\n')

    def p_robot(self, p):
        """robot : direction
                | XRAY"""
        if p[1] == 'xray':
            p[0] = Tree('xray', value=p[1], lineno=p.lineno(1), lexpos=p.lexpos(1))
        else:
            p[0] = Tree('robot', value=p[1], children=p[1], lineno=p.lineno(1), lexpos=p.lexpos(1))

    def p_error(self, p):
        try:
            sys.stderr.write(f'Error at {p.lineno} line\n')
        except:
            sys.stderr.write(f'Error\n')
        self.ok = False

    def p_function(self, p):
        """function : FUNC VAR LBRACKET parameters RBRACKET LBRACKET NEWLINE state RBRACKET
                    | FUNC VAR LBRACKET RBRACKET LBRACKET NEWLINE state RBRACKET"""
        if len(p) == 10:
            self.functions[p[2]] = Tree('function', children={'param': p[4], 'body': p[8]}, lineno=p.lineno(1),
                                             lexpos=p.lexpos(1))
            p[0] = Tree('func', value=p[2], lineno=p.lineno(1), lexpos=p.lexpos(2))
        else:
            self.functions[p[2]] = Tree('function', children={'body': p[7]}, lineno=p.lineno(1),
                                             lexpos=p.lexpos(1))
            p[0] = Tree('func', value=p[2], lineno=p.lineno(1), lexpos=p.lexpos(2))

    def p_function_return(self, p):
        """function_return : variable"""
        p[0] = Tree('return', children=p[1], lineno=p.lineno(1),  lexpos=p.lexpos(1))

    def p_function_call(self, p):
        """function_call : CALL VAR LBRACKET vars RBRACKET
                        | CALL VAR LBRACKET RBRACKET"""
        if len(p) == 6:
            p[0] = Tree('function_call',  value={'name': p[2]}, children=p[4], lineno=p.lineno(2), lexpos=p.lexpos(2))
        else:
            p[0] = Tree('function_call', value={'name': p[2]}, lineno=p.lineno(2), lexpos=p.lexpos(2))

    def p_function_call_error(self, p):
        """function_call : VAR LBRACKET vars RBRACKET error
                        | VAR LBRACKET RBRACKET error"""
        if len(p) == 5:
            p[0] = Tree('error', value="Incorrect call", lineno=p.lineno(2), lexpos=p.lexpos(2))
            sys.stderr.write(f'-> Incorrect call <-\n')
        else:
            p[0] = Tree('error', value="Incorrect call",  lineno=p.lineno(2), lexpos=p.lexpos(2))
            sys.stderr.write(f'-> Incorrect call <-\n')

    def p_function_call_var_error(self, p):
        """function_call : CALL VAR LBRACKET error RBRACKET"""
        p[0] = Tree('error', value="Incorrect call", lineno=p.lineno(1), lexpos=p.lexpos(1))
        sys.stderr.write(f'-> Incorrect call <-\n')

    def p_vars(self, p):
        """vars : VAR vars
                | VAR"""
        if len(p) == 3:
            p[0] = Tree('var', value=p[1], children=p[2], lineno=p.lineno(1),  lexpos=p.lexpos(1))
        else:
            p[0] = Tree('var', value=p[1], lineno=p.lineno(1),  lexpos=p.lexpos(1))

    def p_parameters(self, p):
        """parameters : type VAR COMMA parameters
                        | type VAR"""
        if len(p) == 5:
            p[0] = Tree('parameters', value=[p[2], p[1]], children=[p[4], p[1]], lineno=p.lineno(4), lexpos=p.lexpos(4))
        else:
            p[0] = Tree('parameters', value=[p[2], p[1]], children=p[1], lineno=p.lineno(1), lexpos=p.lexpos(1))

# data = '''a <- top;
#
# '''
#
#
#
# lexer = Lexer()
# lexer.input(data)
# while True:
#     token = lexer.token()
#     if token is None:
#         break
#     else:
#         print(token)
#
# parser = Parser()
# tree, ok, functions = parser.parse(data)
# tree.print()
# print(ok)
#functions['a'].children['body'].print()
