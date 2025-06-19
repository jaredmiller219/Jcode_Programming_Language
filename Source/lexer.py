#######################################
# LEXER
#######################################

from position import *
from constants import *
from tokens import *
from errors import *

class Lexer:
  def __init__(self, function, text):
    self.function = function
    self.text = text
    self.position = Position(-1, 0, -1, function, text)
    self.current_character = None
    self.advance()

  def advance(self):
    self.position.advance(self.current_character)
    if self.position.index < len(self.text):
      self.current_character = self.text[self.position.index]
    else: self.current_character = None

  def Tokenize(self):
    tokens = []

    while self.current_character != None:
        if self.current_character in ' \t':
            self.advance()
        elif self.current_character == '#':
            self.skip_comment()
        elif self.current_character == '/' and self.check_next_character('/'):
            self.skip_double_slash_comment()
        elif self.current_character in ';\n':
            tokens.append(Token(TT_NEWLINE, position_start=self.position))
            self.advance()
        elif self.current_character in DIGITS:
          tokens.append(self.digitize())
        elif self.current_character in LETTERS:
          tokens.append(self.identifize())
        elif self.current_character == ':':
          tokens.append(Token(TT_COLON, position_start=self.position))
          self.advance()
        elif self.current_character == '"':
          tokens.append(self.stringify())
        elif self.current_character == '+':
          tokens.append(Token(TT_PLUS, position_start=self.position))
          self.advance()
        elif self.current_character == '-':
          tokens.append(Token(TT_MINUS, position_start=self.position))
          self.advance()
        elif self.current_character == '*':
          tokens.append(Token(TT_MULTIPLY, position_start=self.position))
          self.advance()
        elif self.current_character == '/':
          tokens.append(Token(TT_DIVIDE, position_start=self.position))
          self.advance()
        elif self.current_character == '^':
          tokens.append(Token(TT_POWER, position_start=self.position))
          self.advance()
        elif self.current_character == '(':
          tokens.append(Token(TT_LEFT_PAREN, position_start=self.position))
          self.advance()
        elif self.current_character == ')':
          tokens.append(Token(TT_RIGHT_PAREN, position_start=self.position))
          self.advance()
        elif self.current_character == '[':
          tokens.append(Token(TT_LEFT_SQUARE, position_start=self.position))
          self.advance()
        elif self.current_character == ']':
          tokens.append(Token(TT_RIGHT_SQUARE, position_start=self.position))
          self.advance()
        elif self.current_character == '{':
          tokens.append(Token(TT_LEFT_BRACE, position_start=self.position))
          self.advance()
        elif self.current_character == '}':
          tokens.append(Token(TT_RIGHT_BRACE, position_start=self.position))
          self.advance()
        elif self.current_character == '!':
          token, error = self.not_equals()
          if error: return [], error
          tokens.append(token)
        elif self.current_character == '=':
          tokens.append(self.equalize())
        elif self.current_character == '<':
          tokens.append(self.less_than())
        elif self.current_character == '>':
          tokens.append(self.greater_than())
        elif self.current_character == ',':
          tokens.append(Token(TT_COMMA, position_start=self.position))
          self.advance()
        else:
          position_start = self.position.copy()
          char = self.current_character
          self.advance()
          return [], IllegalCharacterError(position_start, self.position, "'" + char + "'")

    tokens.append(Token(TT_END_OF_FILE, position_start=self.position))
    return tokens, None

  def digitize(self):
    number_string = ''
    dot_count = 0
    position_start = self.position.copy()

    while self.current_character != None and self.current_character in DIGITS + '.':
      if self.current_character == '.':
        if dot_count == 1: break
        dot_count += 1
      number_string += self.current_character
      self.advance()

    if dot_count == 0:
      return Token(TT_INT, int(number_string), position_start, self.position)
    else:
      return Token(TT_FLOAT, float(number_string), position_start, self.position)

  def stringify(self):
    string = ''
    position_start = self.position.copy()
    escape_character = False
    self.advance()

    escape_characters = {
      'n': '\n',
      't': '\t'
    }

    while self.current_character != None and (self.current_character != '"' or escape_character):
      if escape_character:
        string += escape_characters.get(self.current_character, self.current_character)
      else:
        if self.current_character == '\\':
          escape_character = True
        else:
          string += self.current_character
      self.advance()
      escape_character = False

    self.advance()
    return Token(TT_STRING, string, position_start, self.position)

  def identifize(self):
    identifier_string = ''
    position_start = self.position.copy()

    while self.current_character != None and self.current_character in LETTERS_AND_DIGITS + '_':
      identifier_string += self.current_character
      self.advance()

    token_type = TT_KEYWORD if identifier_string in KEYWORDS else TT_IDENTIFIER
    return Token(token_type, identifier_string, position_start, self.position)

  def not_equals(self):
    position_start = self.position.copy()
    self.advance()

    if self.current_character == '=':
      self.advance()
      return Token(TT_NOT_EQUAL, position_start=position_start, position_end=self.position), None

    self.advance()
    return None, ExpectedCharError(position_start, self.position, "'=' (after '!')")

  def equalize(self):
    token_type = TT_EQUAL
    position_start = self.position.copy()
    self.advance()

    if self.current_character == '=':
      self.advance()
      token_type = TT_EQUAL_EQUAL

    elif self.current_character == '>':
      self.advance()
      token_type = TT_ARROW

    return Token(token_type, position_start=position_start, position_end=self.position)

  def less_than(self):
    token_type = TT_LESS_THAN
    position_start = self.position.copy()
    self.advance()

    if self.current_character == '=':
      self.advance()
      token_type = TT_LESS_THAN_EQUAL

    return Token(token_type, position_start=position_start, position_end=self.position)

  def greater_than(self):
    token_type = TT_GREATER_THAN
    position_start = self.position.copy()
    self.advance()

    if self.current_character == '=':
      self.advance()
      token_type = TT_GREATER_THAN_EQUAL

    return Token(token_type, position_start=position_start, position_end=self.position)

  def skip_comment(self):
    self.advance()
    while self.current_character != '\n': self.advance()
    self.advance()

  def check_next_character(self, string):
    for offset, character in enumerate(string):
        next_character_position = self.position.index + 1 + offset
        if next_character_position >= len(self.text): return False
        if self.text[next_character_position] != character: return False
    return True

  def skip_double_slash_comment(self):
    self.advance()
    self.advance()
    while self.current_character != None:
        if self.current_character == '\n':
          self.advance()
          break
        self.advance()
