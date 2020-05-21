import sys
import ply.lex as lex
import re
from numpy import uint

reserved = {
    'signed': 'SIGNED',
    'unsigned': 'UNSIGNED',
    'const': 'CONST',
    'cell': 'CELL',

    'top': 'TOP',
    'right': 'RIGHT',
    'left': 'LEFT',
    'down': 'DOWN',
    'ntop': 'NTOP',
    'nright': 'NRIGHT',
    'nleft': 'NLEFT',
    'ndown': 'NDOWN',

    'matrix': 'MATRIX',

    'testrep': 'TESTREP',
    'testonce': 'TESTONCE',

    'func': 'FUNC',
    'call': 'CALL',

    'bottom': 'BOTTOM',
    'xray': 'XRAY',
}

class Lexer(object):

    def __init__(self):
        self.lexer = lex.lex(module=self)

    tokens = ['VAR', 'UDECIMAL', 'DECIMAL', 'ASSIGNMENT','PLUS', 'MINUS', 'STAR', 'PROCENT', 'DIV',
              'LBRACKET', 'RBRACKET',
              'LESS', 'GREATER', 'EQ', 'NOTEQ', 'COMMA',
              'SHARP', 'SEMICOLON', 'NEWLINE'] + list(reserved.values())

    t_ASSIGNMENT = r'\<\-'
    t_PLUS = r'\+'
    t_MINUS = r'\-'
    t_STAR = r'\*'
    t_PROCENT = r'\%'
    t_DIV = r'\/'
    t_LBRACKET = r'\('
    t_RBRACKET = r'\)'
    t_LESS = r'\<'
    t_GREATER = r'\>'
    t_COMMA = r'\,'
    t_EQ = r'\='
    t_NOTEQ = r'\<\>'
    t_SEMICOLON = r'\;'
    t_SHARP = r'\#'

    t_ignore = ' \t'

    def t_VAR(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = reserved.get(t.value, 'VAR')
        return t

    def t_UDECIMAL(self, t):
        r'\d+u'
        t.value = re.findall(r'\d+', t.value)
        t.value = uint(t.value[0])
        return t

    def t_DECIMAL(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_NEWLINE(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)
        return t

    def t_error(self, t):
        sys.stderr.write(f'Illegal character: {t.value[0]} at line {t.lexer.lineno}\n')
        t.lexer.skip(1)

    def input(self, data):
        return self.lexer.input(data)

    def token(self):
        return self.lexer.token()

# data = '''
# 123u ;
# '''
#
# lexer = Lexer()
#
# lexer.input(data)
# while True:
#     token = lexer.token()
#     if token is None:
#         break
#     else:
#         print(token)