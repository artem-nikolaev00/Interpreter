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
                     | prison SEMICOLON NEWLINE
                     | if NEWLINE
                     | while NEWLINE
                     | operator SEMICOLON NEWLINE
                     | function NEWLINE
                     | function_call SEMICOLON NEWLINE
                     | function_return SEMICOLON NEWLINE"""
        p[0] = p[1]

    def p_statement_error(self, p):
        """statement : declaration error NEWLINE
                     | assignment error NEWLINE
                     | compare error NEWLINE
                     | prison error NEWLINE
                     | operator error NEWLINE
                     | function_call error NEWLINE
                     | function_return error NEWLINE"""
        p[0] = Tree('error', value="SEMICOLON is absent", children=p[1], lineno=p.lineno(1), lexpos=p.lexpos(1))
        sys.stderr.write(f'-> SEMICOLON is absent <-\n')

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

    def p_declaration_error(self, p):
        """declaration : error VAR
                        | error VAR ASSIGNMENT expression
                        | CONST error VAR ASSIGNMENT expression
                        | MATRIX error VAR
                       | MATRIX error VAR LBRACKET expression COMMA expression RBRACKET"""
        if p[1] == 'const':
            p[0] = Tree('error', value='TYPE ERROR', lineno=p.lineno(2), lexpos=p.lexpos(2))
            sys.stderr.write(f'-> Error in TYPE of declarated varible <-\n')
        elif p[1] == 'matrix':
            p[0] = Tree('error', value='TYPE ERROR', lineno=p.lineno(2), lexpos=p.lexpos(2))
            sys.stderr.write(f'-> Error in TYPE of declarated varible <-\n')
        else:
            p[0] = Tree('error', value='TYPE ERROR', lineno=p.lineno(1), lexpos=p.lexpos(1))
            sys.stderr.write(f'-> Error in TYPE of declarated varible <-\n')

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
                      | function_call
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
                    | NDOWN
                    | BOTTOM"""
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

    def p_if(self, p):
        """if : TESTONCE LBRACKET math_expression RBRACKET LBRACKET NEWLINE state RBRACKET
              | TESTONCE LBRACKET compare RBRACKET LBRACKET NEWLINE state RBRACKET"""
        p[0] = Tree('if', children={
            'cond_exp': Tree('condition', children=p[3], lineno=p.lineno(3),
                                    lexpos=p.lexpos(3)), 'body_exp': Tree('body', children=p[7], lineno=p.lineno(7),
                                    lexpos=p.lexpos(7))}, lineno=p.lineno(1), lexpos=p.lexpos(1))

    def p_for(self, p):
        """while : TESTREP LBRACKET math_expression RBRACKET LBRACKET NEWLINE state RBRACKET
              | TESTREP LBRACKET compare RBRACKET LBRACKET NEWLINE state RBRACKET"""
        p[0] = Tree('while', children={
            'cond_exp': Tree('condition', children=p[3], lineno=p.lineno(3),
                                    lexpos=p.lexpos(3)), 'body_exp': Tree('body', children=p[7], lineno=p.lineno(7),
                                    lexpos=p.lexpos(7))}, lineno=p.lineno(1), lexpos=p.lexpos(1))

    def p_operator(self, p):
        """operator : variable ASSIGNMENT robot"""
        p[0] = Tree('operator', value=p[1], children=p[3], lineno=p.lineno(1), lexpos=p.lexpos(1))

    def p_robot(self, p):
        """robot : direction
                | XRAY"""
        if p[1] == 'xray':
            p[0] = Tree('scan', value=p[1], lineno=p.lineno(1), lexpos=p.lexpos(1))
        else:
            p[0] = Tree('direction', value=p[1], children=p[1], lineno=p.lineno(1), lexpos=p.lexpos(1))

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
            p[0] = Tree('function', value=p[2], children={
                'par_body': Tree('par', value=p[4], children=p[4], lineno=p.lineno(4),
                                  lexpos=p.lexpos(4)),
                                 'func_body': Tree('body', value=p[8], children=p[8], lineno=p.lineno(8),
                                lexpos=p.lexpos(8))}, lineno=p.lineno(2), lexpos=p.lexpos(2))
        else:
            p[0] = Tree('function', value=p[2], children={
                                 'func_body': Tree('body', value=p[7], children=p[7], lineno=p.lineno(7),
                                lexpos=p.lexpos(7))}, lineno=p.lineno(2), lexpos=p.lexpos(2))

    def p_function_return(self, p):
        """function_return : VAR"""
        p[0] = Tree('var', value=p[1], lineno=p.lineno(1),  lexpos=p.lexpos(1))

    def p_function_call(self, p):
        """function_call : CALL VAR LBRACKET vars RBRACKET
                        | CALL VAR LBRACKET RBRACKET"""
        if len(p) == 6:
            p[0] = Tree('call',  value=p[2],
                    children=Tree('var', value=p[4], children=p[4], lineno=p.lineno(4),  lexpos=p.lexpos(4)),
                    lineno=p.lineno(2), lexpos=p.lexpos(2))
        else:
            p[0] = Tree('call', value=p[2], lineno=p.lineno(2), lexpos=p.lexpos(2))

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

data = '''func factorial(cell a)(
	signed result;
	testonce (n = 1)(
		result <- 1;
	)
	testonce (n > 1)(
		x = n - 1;
		result <- call factorial(x) * n;
	)
	result;
)	

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