#######################################
# POSITION
#######################################

class Position:
  def __init__(self, index, line_number, column, function_name, function_text):
    self.index = index
    self.line_number = line_number
    self.column = column
    self.function_name = function_name
    self.function_text = function_text

  def advance(self, current_character=None):
    self.index += 1
    self.column += 1

    if current_character == '\n':
      self.line_number += 1
      self.column = 0

    return self

  def copy(self):
    return Position(self.index, self.line_number, self.column, self.function_name, self.function_text)
