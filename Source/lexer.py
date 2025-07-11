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

    # Track newlines and function definitions
    consecutive_newlines = 0
    last_token_was_func = False
    # last_func_position = None

    while self.current_character is not None:
        if self.current_character in ' \t':
            self.advance()
        elif self.current_character == '#':
            # If we're right after a function and haven't seen a blank line,
            # insert a special token
            if last_token_was_func and consecutive_newlines < 2:
                tokens.append(Token(TT_NO_BLANK_LINE, position_start=self.position, position_end=self.position))
            self.skip_comment()
        elif self.current_character == '/' and self.check_next_character('/'):
            # If we're right after a function and haven't seen a blank line,
            # insert a special token
            if last_token_was_func and consecutive_newlines < 2:
                tokens.append(Token(TT_NO_BLANK_LINE, position_start=self.position, position_end=self.position))
            self.skip_double_slash_comment()
        elif self.current_character == '/' and self.check_next_character('*'):
            # If we're right after a function and haven't seen a blank line,
            # insert a special token
            if last_token_was_func and consecutive_newlines < 2:
                tokens.append(Token(TT_NO_BLANK_LINE, position_start=self.position, position_end=self.position))
            self.skip_block_comment()
        elif self.current_character in ';\n':
            tokens.append(Token(TT_NEWLINE, position_start=self.position))
            self.advance()
            consecutive_newlines += 1

            # If we've seen 2 or more consecutive newlines, reset the function flag
            if consecutive_newlines >= 2:
                last_token_was_func = False
        else:
            # Process actual code tokens
            if self.current_character in DIGITS:
                tokens.append(self.digitize())
                consecutive_newlines = 0
            elif self.current_character in LETTERS:
                token = self.identifize()
                tokens.append(token)

                # Check if this is a function definition
                if token.type == TT_KEYWORD and token.value == 'func':
                    last_token_was_func = True
                    # last_func_position = token.position_start.copy()

                consecutive_newlines = 0
            elif self.current_character == '}':
                tokens.append(Token(TT_RIGHT_BRACE, position_start=self.position))
                self.advance()

                # Mark that we just ended a function
                # This is a simplistic approach - in reality you'd need to track
                # if this brace is actually ending a function
                # last_token_was_func_end = True
                # last_func_end_position = self.position.copy()
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
            elif self.current_character == '.':
              tokens.append(Token(TT_DOT, position_start=self.position))
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

    while self.current_character is not None and self.current_character in DIGITS + '.':
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

    while self.current_character is not None and (self.current_character != '"' or escape_character):
      if escape_character:
        string += escape_characters.get(self.current_character, self.current_character)
      elif self.current_character != '\\':
        string += self.current_character
      self.advance()
      escape_character = False

    self.advance()
    return Token(TT_STRING, string, position_start, self.position)

  def identifize(self):
    identifier_string = ''
    position_start = self.position.copy()

    while self.current_character is not None and self.current_character in LETTERS_AND_DIGITS + '_':
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
    return None, ExpectedCharacterError(position_start, self.position, "'=' (after '!')")

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

  def skip_block_comment(self):
    self.advance()  # Skip the *
    self.advance()  # Skip the opening /

    nesting_level = 1

    while self.current_character is not None and nesting_level > 0:
      # Check for nested block comment start
      if self.current_character == '/' and self.check_next_character('*'):
        self.advance()  # Skip /
        self.advance()  # Skip *
        nesting_level += 1
      # Check for block comment end
      elif self.current_character == '*' and self.check_next_character('/'):
        self.advance()  # Skip *
        self.advance()  # Skip /
        nesting_level -= 1
      else:
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
    while self.current_character is not None:
        if self.current_character == '\n':
          self.advance()
          break
        self.advance()

  def make_doc_comment(self):
    comment = ''
    pos_start = self.pos.copy()

    # Consume the three slashes
    self.advance()
    self.advance()
    self.advance()

    # Collect the rest of the line
    while self.current_char is not None and self.current_char != '\n':
        comment += self.current_char
        self.advance()

    return Token(TT_COMMENT, '///' + comment, pos_start, self.pos)

  def make_doc_block_comment(self):
    comment = ''
    pos_start = self.pos.copy()

    # Consume the opening /**
    self.advance()
    self.advance()
    self.advance()

    # Collect until closing */
    while self.current_char is not None:
        if self.current_char == '*' and self.peek() == '/':
            self.advance()
            self.advance()
            break
        comment += self.current_char
        self.advance()

    return Token(TT_COMMENT, '/**' + comment + '*/', pos_start, self.pos)
