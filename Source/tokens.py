#######################################
# TOKENS
#######################################

TT_INT			            = 'INT'
TT_FLOAT    	          = 'FLOAT'
TT_STRING		            = 'STRING'
TT_IDENTIFIER	          = 'IDENTIFIER'
TT_KEYWORD		          = 'KEYWORD'
TT_PLUS     	          = 'PLUS'
TT_MINUS    	          = 'MINUS'
TT_MULTIPLY             = 'MULTIPLY'
TT_DIVIDE               = 'DIVIDE'
TT_POWER		 	          = 'POWER'
TT_EQUAL			          = 'EQUAL'
TT_LEFT_PAREN   	      = 'LEFT_PAREN'
TT_RIGHT_PAREN   	      = 'RIGHT_PAREN'
TT_LEFT_SQUARE          = 'LEFT_SQUARE'
TT_RIGHT_SQUARE         = 'RIGHT_SQUARE'
TT_LEFT_BRACE           = 'LEFT_BRACE'
TT_RIGHT_BRACE          = 'RIGHT_BRACE'
TT_COLON                = 'COLON'
TT_EQUAL_EQUAL			    = 'EQUAL_EQUAL'
TT_NOT_EQUAL			      = 'NOT_EQUAL'
TT_LESS_THAN  		      = 'LEFT_THAN'
TT_GREATER_THAN		      = 'GREATER_THAN'
TT_LESS_THAN_EQUAL      = 'LESS_THAN_EQUAL'
TT_GREATER_THAN_EQUAL   = 'GREATER_THAN_EQUAL'
TT_COMMA		            = 'COMMA'
TT_ARROW		            = 'ARROW'
TT_ASSIGN               = 'ASSIGN'
TT_NEWLINE		          = 'NEWLINE'
TT_END_OF_FILE			    = 'END_OF_FILE'
TT_NO_BLANK_LINE        = 'NO_BLANK_LINE'
TT_COMMENT              = 'COMMENT'

KEYWORDS = [
  'var',
  'and',
  'or',
  'not',
  'if',
  'elif',
  'else',
  'for',
  'to',
  'step',
  'while',
  'func',
  'end',
  'return',
  'continue',
  'break',
]

class Token:
  def __init__(self, type_, value=None, position_start=None, position_end=None):
    self.type = type_
    self.value = value

    if position_start:
      self.position_start = position_start.copy()
      self.position_end = position_start.copy()
      self.position_end.advance()

    if position_end:
      self.position_end = position_end.copy()

  def matches(self, type_, value):
    return self.type == type_ and self.value == value

  def __repr__(self):
    if self.value: return f'{self.type}:{self.value}'
    return f'{self.type}'
