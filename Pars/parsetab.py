
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'ASSIGNMENT BOTTOM CALL CELL COMMA CONST DECIMAL DIV DOWN EQ FUNC GREATER LBRACKET LEFT LESS LQBRACKET MATRIX MINUS NDOWN NEWLINE NLEFT NOTEQ NRIGHT NTOP PLUS PROCENT RBRACKET RIGHT RQBRACKET SEMICOLON SHARP SIGNED STAR TESTONCE TESTREP TOP UNSIGNED VAR XRAYprogram : statestate : state statement\n                | statementstatement : declaration SEMICOLON NEWLINE\n                     | assignment SEMICOLON NEWLINE\n                     | compare SEMICOLON NEWLINE\n                     | prison SEMICOLON NEWLINE\n                     | if NEWLINE\n                     | while NEWLINE\n                     | operator SEMICOLON NEWLINE\n                     | function NEWLINE\n                     | function_call SEMICOLON NEWLINEstatement : declaration error NEWLINE\n                     | assignment error NEWLINE\n                     | compare error NEWLINE\n                     | prison error NEWLINE\n                     | operator error NEWLINE\n                     | function_call error NEWLINEdeclaration : type VAR\n                       | type VAR ASSIGNMENT expression\n                       | CONST type VAR ASSIGNMENT expression\n                       | MATRIX type VAR\n                       | MATRIX type VAR LBRACKET expression COMMA expression RBRACKETdeclaration : error VAR\n                        | error VAR ASSIGNMENT expression\n                        | CONST error VAR ASSIGNMENT expression\n                        | MATRIX error VAR\n                       | MATRIX error VAR LBRACKET expression COMMA expression RBRACKETtype : SIGNED\n                | UNSIGNED\n                | CELLexpression : math_expression\n                      | const\n                      | variable\n                      | side\n                      | compare\n                      | prison\n                      | LBRACKET expression RBRACKETside : LBRACKET directions RBRACKETdirections : direction COMMA directions\n                    | directiondirection : TOP\n                    | NTOP\n                    | LEFT\n                    | NLEFT\n                    | RIGHT\n                    | NRIGHT\n                    | DOWN\n                    | NDOWN\n                    | BOTTOMcompare : expression EQ expression\n                    | expression LESS expression\n                    | expression GREATER expression\n                    | expression NOTEQ expressionmath_expression : expression PLUS expression\n                        | expression MINUS expression\n                        | expression STAR expression\n                        | expression DIV expression\n                        | expression PROCENT expressionconst : DECIMALvariable : VAR\n                    | VAR LQBRACKET index RBRACKET LQBRACKET index RQBRACKETindex : UNSIGNEDprison : SHARP variableassignment : variable ASSIGNMENT expressionif : TESTONCE LBRACKET math_expression RBRACKET LBRACKET NEWLINE state RBRACKET\n              | TESTONCE LBRACKET compare RBRACKET LBRACKET NEWLINE state RBRACKETwhile : TESTREP LBRACKET math_expression RBRACKET LBRACKET NEWLINE state RBRACKET\n              | TESTREP LBRACKET compare RBRACKET LBRACKET NEWLINE state RBRACKEToperator : variable ASSIGNMENT robotrobot : direction\n                | XRAYfunction : FUNC VAR LBRACKET parameters RBRACKET LBRACKET NEWLINE state RBRACKETfunction_call : CALL VAR LBRACKET vars RBRACKETvars : vars\n                | VARparameters : type VAR COMMA parameters\n                        | type VAR'
    
_lr_action_items = {'CONST':([0,2,3,33,42,43,46,86,87,88,89,90,91,92,93,94,95,96,97,160,161,162,163,169,170,171,172,173,181,],[17,17,-3,-2,-8,-9,-11,-4,-13,-5,-14,-6,-15,-7,-16,-10,-17,-12,-18,17,17,17,17,17,17,17,17,17,17,]),'MATRIX':([0,2,3,33,42,43,46,86,87,88,89,90,91,92,93,94,95,96,97,160,161,162,163,169,170,171,172,173,181,],[18,18,-3,-2,-8,-9,-11,-4,-13,-5,-14,-6,-15,-7,-16,-10,-17,-12,-18,18,18,18,18,18,18,18,18,18,18,]),'error':([0,2,3,4,5,6,7,10,12,15,17,18,23,30,31,32,33,42,43,46,49,50,67,68,69,71,72,73,74,75,76,77,78,79,81,86,87,88,89,90,91,92,93,94,95,96,97,102,103,104,105,106,107,108,109,110,113,114,115,116,118,119,120,121,129,130,146,147,156,160,161,162,163,166,169,170,171,172,173,175,176,181,],[13,13,-3,35,37,39,41,45,48,-61,62,64,-32,-33,-35,-60,-2,-8,-9,-11,-24,-19,-34,-36,-37,-42,-43,-44,-45,-46,-47,-48,-49,-50,-64,-4,-13,-5,-14,-6,-15,-7,-16,-10,-17,-12,-18,-51,-52,-53,-54,-55,-56,-57,-58,-59,-22,-27,-38,-39,-65,-70,-71,-72,-25,-20,-21,-26,-74,13,13,13,13,-62,13,13,13,13,13,-23,-28,13,]),'SHARP':([0,2,3,19,33,42,43,46,52,53,54,55,56,57,58,59,60,80,82,83,86,87,88,89,90,91,92,93,94,95,96,97,98,99,132,133,134,135,158,159,160,161,162,163,169,170,171,172,173,181,],[21,21,-3,21,-2,-8,-9,-11,21,21,21,21,21,21,21,21,21,21,21,21,-4,-13,-5,-14,-6,-15,-7,-16,-10,-17,-12,-18,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,]),'TESTONCE':([0,2,3,33,42,43,46,86,87,88,89,90,91,92,93,94,95,96,97,160,161,162,163,169,170,171,172,173,181,],[22,22,-3,-2,-8,-9,-11,-4,-13,-5,-14,-6,-15,-7,-16,-10,-17,-12,-18,22,22,22,22,22,22,22,22,22,22,]),'TESTREP':([0,2,3,33,42,43,46,86,87,88,89,90,91,92,93,94,95,96,97,160,161,162,163,169,170,171,172,173,181,],[24,24,-3,-2,-8,-9,-11,-4,-13,-5,-14,-6,-15,-7,-16,-10,-17,-12,-18,24,24,24,24,24,24,24,24,24,24,]),'FUNC':([0,2,3,33,42,43,46,86,87,88,89,90,91,92,93,94,95,96,97,160,161,162,163,169,170,171,172,173,181,],[25,25,-3,-2,-8,-9,-11,-4,-13,-5,-14,-6,-15,-7,-16,-10,-17,-12,-18,25,25,25,25,25,25,25,25,25,25,]),'CALL':([0,2,3,33,42,43,46,86,87,88,89,90,91,92,93,94,95,96,97,160,161,162,163,169,170,171,172,173,181,],[26,26,-3,-2,-8,-9,-11,-4,-13,-5,-14,-6,-15,-7,-16,-10,-17,-12,-18,26,26,26,26,26,26,26,26,26,26,]),'SIGNED':([0,2,3,17,18,33,42,43,46,86,87,88,89,90,91,92,93,94,95,96,97,127,160,161,162,163,165,169,170,171,172,173,181,],[27,27,-3,27,27,-2,-8,-9,-11,-4,-13,-5,-14,-6,-15,-7,-16,-10,-17,-12,-18,27,27,27,27,27,27,27,27,27,27,27,27,]),'UNSIGNED':([0,2,3,17,18,33,42,43,46,51,86,87,88,89,90,91,92,93,94,95,96,97,127,145,160,161,162,163,165,169,170,171,172,173,181,],[28,28,-3,28,28,-2,-8,-9,-11,101,-4,-13,-5,-14,-6,-15,-7,-16,-10,-17,-12,-18,28,101,28,28,28,28,28,28,28,28,28,28,28,]),'CELL':([0,2,3,17,18,33,42,43,46,86,87,88,89,90,91,92,93,94,95,96,97,127,160,161,162,163,165,169,170,171,172,173,181,],[29,29,-3,29,29,-2,-8,-9,-11,-4,-13,-5,-14,-6,-15,-7,-16,-10,-17,-12,-18,29,29,29,29,29,29,29,29,29,29,29,29,]),'VAR':([0,2,3,13,14,19,21,25,26,27,28,29,33,42,43,46,52,53,54,55,56,57,58,59,60,61,62,63,64,80,82,83,86,87,88,89,90,91,92,93,94,95,96,97,98,99,128,132,133,134,135,142,158,159,160,161,162,163,169,170,171,172,173,181,],[15,15,-3,49,50,15,15,84,85,-29,-30,-31,-2,-8,-9,-11,15,15,15,15,15,15,15,15,15,111,112,113,114,15,15,15,-4,-13,-5,-14,-6,-15,-7,-16,-10,-17,-12,-18,15,15,143,15,15,15,15,155,15,15,15,15,15,15,15,15,15,15,15,15,]),'LBRACKET':([0,2,3,19,22,24,33,42,43,46,52,53,54,55,56,57,58,59,60,80,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,113,114,132,133,134,135,137,138,139,140,154,158,159,160,161,162,163,169,170,171,172,173,181,],[19,19,-3,19,82,83,-2,-8,-9,-11,19,19,19,19,19,19,19,19,19,19,19,19,127,128,-4,-13,-5,-14,-6,-15,-7,-16,-10,-17,-12,-18,19,19,134,135,19,19,19,19,150,151,152,153,164,19,19,19,19,19,19,19,19,19,19,19,19,]),'DECIMAL':([0,2,3,19,33,42,43,46,52,53,54,55,56,57,58,59,60,80,82,83,86,87,88,89,90,91,92,93,94,95,96,97,98,99,132,133,134,135,158,159,160,161,162,163,169,170,171,172,173,181,],[32,32,-3,32,-2,-8,-9,-11,32,32,32,32,32,32,32,32,32,32,32,32,-4,-13,-5,-14,-6,-15,-7,-16,-10,-17,-12,-18,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,]),'$end':([1,2,3,33,42,43,46,86,87,88,89,90,91,92,93,94,95,96,97,],[0,-1,-3,-2,-8,-9,-11,-4,-13,-5,-14,-6,-15,-7,-16,-10,-17,-12,-18,]),'RBRACKET':([3,15,23,30,31,32,33,42,43,46,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,81,86,87,88,89,90,91,92,93,94,95,96,97,100,101,102,103,104,105,106,107,108,109,110,115,116,122,123,125,126,136,141,143,144,155,166,167,168,169,170,171,172,174,181,],[-3,-61,-32,-33,-35,-60,-2,-8,-9,-11,115,116,-34,-36,-37,-41,-42,-43,-44,-45,-46,-47,-48,-49,-50,-64,-4,-13,-5,-14,-6,-15,-7,-16,-10,-17,-12,-18,131,-63,-51,-52,-53,-54,-55,-56,-57,-58,-59,-38,-39,137,138,139,140,-40,154,-76,156,-78,-62,175,176,177,178,179,180,-77,182,]),'SEMICOLON':([4,5,6,7,10,12,15,23,30,31,32,49,50,67,68,69,71,72,73,74,75,76,77,78,79,81,102,103,104,105,106,107,108,109,110,113,114,115,116,118,119,120,121,129,130,146,147,156,166,175,176,],[34,36,38,40,44,47,-61,-32,-33,-35,-60,-24,-19,-34,-36,-37,-42,-43,-44,-45,-46,-47,-48,-49,-50,-64,-51,-52,-53,-54,-55,-56,-57,-58,-59,-22,-27,-38,-39,-65,-70,-71,-72,-25,-20,-21,-26,-74,-62,-23,-28,]),'EQ':([6,7,15,16,20,23,30,31,32,65,67,68,69,81,102,103,104,105,106,107,108,109,110,115,116,118,122,123,124,125,126,129,130,146,147,148,149,166,167,168,],[-36,-37,-61,52,-34,-32,-33,-35,-60,52,-34,-36,-37,-64,52,52,52,52,52,52,52,52,52,-38,-39,52,-32,-36,52,-32,-36,52,52,52,52,52,52,-62,52,52,]),'LESS':([6,7,15,16,20,23,30,31,32,65,67,68,69,81,102,103,104,105,106,107,108,109,110,115,116,118,122,123,124,125,126,129,130,146,147,148,149,166,167,168,],[-36,-37,-61,53,-34,-32,-33,-35,-60,53,-34,-36,-37,-64,53,53,53,53,53,53,53,53,53,-38,-39,53,-32,-36,53,-32,-36,53,53,53,53,53,53,-62,53,53,]),'GREATER':([6,7,15,16,20,23,30,31,32,65,67,68,69,81,102,103,104,105,106,107,108,109,110,115,116,118,122,123,124,125,126,129,130,146,147,148,149,166,167,168,],[-36,-37,-61,54,-34,-32,-33,-35,-60,54,-34,-36,-37,-64,54,54,54,54,54,54,54,54,54,-38,-39,54,-32,-36,54,-32,-36,54,54,54,54,54,54,-62,54,54,]),'NOTEQ':([6,7,15,16,20,23,30,31,32,65,67,68,69,81,102,103,104,105,106,107,108,109,110,115,116,118,122,123,124,125,126,129,130,146,147,148,149,166,167,168,],[-36,-37,-61,55,-34,-32,-33,-35,-60,55,-34,-36,-37,-64,55,55,55,55,55,55,55,55,55,-38,-39,55,-32,-36,55,-32,-36,55,55,55,55,55,55,-62,55,55,]),'PLUS':([6,7,15,16,20,23,30,31,32,65,67,68,69,81,102,103,104,105,106,107,108,109,110,115,116,118,122,123,124,125,126,129,130,146,147,148,149,166,167,168,],[-36,-37,-61,56,-34,-32,-33,-35,-60,56,-34,-36,-37,-64,56,56,56,56,56,56,56,56,56,-38,-39,56,-32,-36,56,-32,-36,56,56,56,56,56,56,-62,56,56,]),'MINUS':([6,7,15,16,20,23,30,31,32,65,67,68,69,81,102,103,104,105,106,107,108,109,110,115,116,118,122,123,124,125,126,129,130,146,147,148,149,166,167,168,],[-36,-37,-61,57,-34,-32,-33,-35,-60,57,-34,-36,-37,-64,57,57,57,57,57,57,57,57,57,-38,-39,57,-32,-36,57,-32,-36,57,57,57,57,57,57,-62,57,57,]),'STAR':([6,7,15,16,20,23,30,31,32,65,67,68,69,81,102,103,104,105,106,107,108,109,110,115,116,118,122,123,124,125,126,129,130,146,147,148,149,166,167,168,],[-36,-37,-61,58,-34,-32,-33,-35,-60,58,-34,-36,-37,-64,58,58,58,58,58,58,58,58,58,-38,-39,58,-32,-36,58,-32,-36,58,58,58,58,58,58,-62,58,58,]),'DIV':([6,7,15,16,20,23,30,31,32,65,67,68,69,81,102,103,104,105,106,107,108,109,110,115,116,118,122,123,124,125,126,129,130,146,147,148,149,166,167,168,],[-36,-37,-61,59,-34,-32,-33,-35,-60,59,-34,-36,-37,-64,59,59,59,59,59,59,59,59,59,-38,-39,59,-32,-36,59,-32,-36,59,59,59,59,59,59,-62,59,59,]),'PROCENT':([6,7,15,16,20,23,30,31,32,65,67,68,69,81,102,103,104,105,106,107,108,109,110,115,116,118,122,123,124,125,126,129,130,146,147,148,149,166,167,168,],[-36,-37,-61,60,-34,-32,-33,-35,-60,60,-34,-36,-37,-64,60,60,60,60,60,60,60,60,60,-38,-39,60,-32,-36,60,-32,-36,60,60,60,60,60,60,-62,60,60,]),'NEWLINE':([8,9,11,34,35,36,37,38,39,40,41,44,45,47,48,150,151,152,153,164,177,178,179,180,182,],[42,43,46,86,87,88,89,90,91,92,93,94,95,96,97,160,161,162,163,173,-66,-67,-68,-69,-73,]),'ASSIGNMENT':([15,20,49,50,111,112,166,],[-61,80,98,99,132,133,-62,]),'COMMA':([15,23,30,31,32,67,68,69,70,71,72,73,74,75,76,77,78,79,81,102,103,104,105,106,107,108,109,110,115,116,148,149,155,166,],[-61,-32,-33,-35,-60,-34,-36,-37,117,-42,-43,-44,-45,-46,-47,-48,-49,-50,-64,-51,-52,-53,-54,-55,-56,-57,-58,-59,-38,-39,158,159,165,-62,]),'LQBRACKET':([15,131,],[51,145,]),'TOP':([19,80,117,],[71,71,71,]),'NTOP':([19,80,117,],[72,72,72,]),'LEFT':([19,80,117,],[73,73,73,]),'NLEFT':([19,80,117,],[74,74,74,]),'RIGHT':([19,80,117,],[75,75,75,]),'NRIGHT':([19,80,117,],[76,76,76,]),'DOWN':([19,80,117,],[77,77,77,]),'NDOWN':([19,80,117,],[78,78,78,]),'BOTTOM':([19,80,117,],[79,79,79,]),'XRAY':([80,],[121,]),'RQBRACKET':([101,157,],[-63,166,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'state':([0,160,161,162,163,173,],[2,169,170,171,172,181,]),'statement':([0,2,160,161,162,163,169,170,171,172,173,181,],[3,33,3,3,3,3,33,33,33,33,3,33,]),'declaration':([0,2,160,161,162,163,169,170,171,172,173,181,],[4,4,4,4,4,4,4,4,4,4,4,4,]),'assignment':([0,2,160,161,162,163,169,170,171,172,173,181,],[5,5,5,5,5,5,5,5,5,5,5,5,]),'compare':([0,2,19,52,53,54,55,56,57,58,59,60,80,82,83,98,99,132,133,134,135,158,159,160,161,162,163,169,170,171,172,173,181,],[6,6,68,68,68,68,68,68,68,68,68,68,68,123,126,68,68,68,68,68,68,68,68,6,6,6,6,6,6,6,6,6,6,]),'prison':([0,2,19,52,53,54,55,56,57,58,59,60,80,82,83,98,99,132,133,134,135,158,159,160,161,162,163,169,170,171,172,173,181,],[7,7,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,7,7,7,7,7,7,7,7,7,7,]),'if':([0,2,160,161,162,163,169,170,171,172,173,181,],[8,8,8,8,8,8,8,8,8,8,8,8,]),'while':([0,2,160,161,162,163,169,170,171,172,173,181,],[9,9,9,9,9,9,9,9,9,9,9,9,]),'operator':([0,2,160,161,162,163,169,170,171,172,173,181,],[10,10,10,10,10,10,10,10,10,10,10,10,]),'function':([0,2,160,161,162,163,169,170,171,172,173,181,],[11,11,11,11,11,11,11,11,11,11,11,11,]),'function_call':([0,2,160,161,162,163,169,170,171,172,173,181,],[12,12,12,12,12,12,12,12,12,12,12,12,]),'type':([0,2,17,18,127,160,161,162,163,165,169,170,171,172,173,181,],[14,14,61,63,142,14,14,14,14,142,14,14,14,14,14,14,]),'expression':([0,2,19,52,53,54,55,56,57,58,59,60,80,82,83,98,99,132,133,134,135,158,159,160,161,162,163,169,170,171,172,173,181,],[16,16,65,102,103,104,105,106,107,108,109,110,118,124,124,129,130,146,147,148,149,167,168,16,16,16,16,16,16,16,16,16,16,]),'variable':([0,2,19,21,52,53,54,55,56,57,58,59,60,80,82,83,98,99,132,133,134,135,158,159,160,161,162,163,169,170,171,172,173,181,],[20,20,67,81,67,67,67,67,67,67,67,67,67,67,67,67,67,67,67,67,67,67,67,67,20,20,20,20,20,20,20,20,20,20,]),'math_expression':([0,2,19,52,53,54,55,56,57,58,59,60,80,82,83,98,99,132,133,134,135,158,159,160,161,162,163,169,170,171,172,173,181,],[23,23,23,23,23,23,23,23,23,23,23,23,23,122,125,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,]),'const':([0,2,19,52,53,54,55,56,57,58,59,60,80,82,83,98,99,132,133,134,135,158,159,160,161,162,163,169,170,171,172,173,181,],[30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,]),'side':([0,2,19,52,53,54,55,56,57,58,59,60,80,82,83,98,99,132,133,134,135,158,159,160,161,162,163,169,170,171,172,173,181,],[31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,]),'directions':([19,117,],[66,136,]),'direction':([19,80,117,],[70,120,70,]),'index':([51,145,],[100,157,]),'robot':([80,],[119,]),'parameters':([127,165,],[141,174,]),'vars':([128,],[144,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> state','program',1,'p_program','parser.py',26),
  ('state -> state statement','state',2,'p_state','parser.py',30),
  ('state -> statement','state',1,'p_state','parser.py',31),
  ('statement -> declaration SEMICOLON NEWLINE','statement',3,'p_statement','parser.py',38),
  ('statement -> assignment SEMICOLON NEWLINE','statement',3,'p_statement','parser.py',39),
  ('statement -> compare SEMICOLON NEWLINE','statement',3,'p_statement','parser.py',40),
  ('statement -> prison SEMICOLON NEWLINE','statement',3,'p_statement','parser.py',41),
  ('statement -> if NEWLINE','statement',2,'p_statement','parser.py',42),
  ('statement -> while NEWLINE','statement',2,'p_statement','parser.py',43),
  ('statement -> operator SEMICOLON NEWLINE','statement',3,'p_statement','parser.py',44),
  ('statement -> function NEWLINE','statement',2,'p_statement','parser.py',45),
  ('statement -> function_call SEMICOLON NEWLINE','statement',3,'p_statement','parser.py',46),
  ('statement -> declaration error NEWLINE','statement',3,'p_statement_error','parser.py',50),
  ('statement -> assignment error NEWLINE','statement',3,'p_statement_error','parser.py',51),
  ('statement -> compare error NEWLINE','statement',3,'p_statement_error','parser.py',52),
  ('statement -> prison error NEWLINE','statement',3,'p_statement_error','parser.py',53),
  ('statement -> operator error NEWLINE','statement',3,'p_statement_error','parser.py',54),
  ('statement -> function_call error NEWLINE','statement',3,'p_statement_error','parser.py',55),
  ('declaration -> type VAR','declaration',2,'p_declaration','parser.py',60),
  ('declaration -> type VAR ASSIGNMENT expression','declaration',4,'p_declaration','parser.py',61),
  ('declaration -> CONST type VAR ASSIGNMENT expression','declaration',5,'p_declaration','parser.py',62),
  ('declaration -> MATRIX type VAR','declaration',3,'p_declaration','parser.py',63),
  ('declaration -> MATRIX type VAR LBRACKET expression COMMA expression RBRACKET','declaration',8,'p_declaration','parser.py',64),
  ('declaration -> error VAR','declaration',2,'p_declaration_error','parser.py',88),
  ('declaration -> error VAR ASSIGNMENT expression','declaration',4,'p_declaration_error','parser.py',89),
  ('declaration -> CONST error VAR ASSIGNMENT expression','declaration',5,'p_declaration_error','parser.py',90),
  ('declaration -> MATRIX error VAR','declaration',3,'p_declaration_error','parser.py',91),
  ('declaration -> MATRIX error VAR LBRACKET expression COMMA expression RBRACKET','declaration',8,'p_declaration_error','parser.py',92),
  ('type -> SIGNED','type',1,'p_type','parser.py',104),
  ('type -> UNSIGNED','type',1,'p_type','parser.py',105),
  ('type -> CELL','type',1,'p_type','parser.py',106),
  ('expression -> math_expression','expression',1,'p_expression','parser.py',110),
  ('expression -> const','expression',1,'p_expression','parser.py',111),
  ('expression -> variable','expression',1,'p_expression','parser.py',112),
  ('expression -> side','expression',1,'p_expression','parser.py',113),
  ('expression -> compare','expression',1,'p_expression','parser.py',114),
  ('expression -> prison','expression',1,'p_expression','parser.py',115),
  ('expression -> LBRACKET expression RBRACKET','expression',3,'p_expression','parser.py',116),
  ('side -> LBRACKET directions RBRACKET','side',3,'p_side','parser.py',123),
  ('directions -> direction COMMA directions','directions',3,'p_directions','parser.py',127),
  ('directions -> direction','directions',1,'p_directions','parser.py',128),
  ('direction -> TOP','direction',1,'p_direction','parser.py',135),
  ('direction -> NTOP','direction',1,'p_direction','parser.py',136),
  ('direction -> LEFT','direction',1,'p_direction','parser.py',137),
  ('direction -> NLEFT','direction',1,'p_direction','parser.py',138),
  ('direction -> RIGHT','direction',1,'p_direction','parser.py',139),
  ('direction -> NRIGHT','direction',1,'p_direction','parser.py',140),
  ('direction -> DOWN','direction',1,'p_direction','parser.py',141),
  ('direction -> NDOWN','direction',1,'p_direction','parser.py',142),
  ('direction -> BOTTOM','direction',1,'p_direction','parser.py',143),
  ('compare -> expression EQ expression','compare',3,'p_compare','parser.py',147),
  ('compare -> expression LESS expression','compare',3,'p_compare','parser.py',148),
  ('compare -> expression GREATER expression','compare',3,'p_compare','parser.py',149),
  ('compare -> expression NOTEQ expression','compare',3,'p_compare','parser.py',150),
  ('math_expression -> expression PLUS expression','math_expression',3,'p_math_expression','parser.py',155),
  ('math_expression -> expression MINUS expression','math_expression',3,'p_math_expression','parser.py',156),
  ('math_expression -> expression STAR expression','math_expression',3,'p_math_expression','parser.py',157),
  ('math_expression -> expression DIV expression','math_expression',3,'p_math_expression','parser.py',158),
  ('math_expression -> expression PROCENT expression','math_expression',3,'p_math_expression','parser.py',159),
  ('const -> DECIMAL','const',1,'p_const','parser.py',166),
  ('variable -> VAR','variable',1,'p_variable','parser.py',170),
  ('variable -> VAR LQBRACKET index RBRACKET LQBRACKET index RQBRACKET','variable',7,'p_variable','parser.py',171),
  ('index -> UNSIGNED','index',1,'p_index','parser.py',178),
  ('prison -> SHARP variable','prison',2,'p_prison','parser.py',182),
  ('assignment -> variable ASSIGNMENT expression','assignment',3,'p_assignment','parser.py',186),
  ('if -> TESTONCE LBRACKET math_expression RBRACKET LBRACKET NEWLINE state RBRACKET','if',8,'p_if','parser.py',191),
  ('if -> TESTONCE LBRACKET compare RBRACKET LBRACKET NEWLINE state RBRACKET','if',8,'p_if','parser.py',192),
  ('while -> TESTREP LBRACKET math_expression RBRACKET LBRACKET NEWLINE state RBRACKET','while',8,'p_for','parser.py',198),
  ('while -> TESTREP LBRACKET compare RBRACKET LBRACKET NEWLINE state RBRACKET','while',8,'p_for','parser.py',199),
  ('operator -> variable ASSIGNMENT robot','operator',3,'p_operator','parser.py',205),
  ('robot -> direction','robot',1,'p_robot','parser.py',209),
  ('robot -> XRAY','robot',1,'p_robot','parser.py',210),
  ('function -> FUNC VAR LBRACKET parameters RBRACKET LBRACKET NEWLINE state RBRACKET','function',9,'p_function','parser.py',224),
  ('function_call -> CALL VAR LBRACKET vars RBRACKET','function_call',5,'p_function_call','parser.py',230),
  ('vars -> vars','vars',1,'p_vars','parser.py',233),
  ('vars -> VAR','vars',1,'p_vars','parser.py',234),
  ('parameters -> type VAR COMMA parameters','parameters',4,'p_parameters','parser.py',238),
  ('parameters -> type VAR','parameters',2,'p_parameters','parser.py',239),
]