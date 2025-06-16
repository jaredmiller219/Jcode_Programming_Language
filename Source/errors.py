#######################################
# ERRORS
#######################################

from utils import string_with_arrows

class Error:
  def __init__(self, position_start, position_end, error_name, details):
    self.position_start = position_start
    self.position_end = position_end
    self.error_name = error_name
    self.details = details

  def as_string(self):
    result  = f'{self.error_name}: {self.details}\n'
    result += f'File {self.position_start.function_name}, line {self.position_start.line_number + 1}'
    result += '\n\n' + string_with_arrows(self.position_start.function_text, self.position_start, self.position_end)
    return result

class IllegalCharacterError(Error):
  def __init__(self, position_start, position_end, details):
    super().__init__(position_start, position_end, 'Illegal Character', details)

class ExpectedCharacterError(Error):
  def __init__(self, position_start, position_end, details):
    super().__init__(position_start, position_end, 'Expected Character', details)

class InvalidSyntaxError(Error):
  def __init__(self, position_start, position_end, details=''):
    super().__init__(position_start, position_end, 'Invalid Syntax', details)

class RuntimeError(Error):
  def __init__(self, position_start, position_end, details, context):
    super().__init__(position_start, position_end, 'Runtime Error', details)
    self.context = context

  def as_string(self):
    result  = self.generate_traceback()
    result += f'{self.error_name}: {self.details}'
    result += '\n\n' + string_with_arrows(self.position_start.function_text, self.position_start, self.position_end)
    return result

  def generate_traceback(self):
    result = ''
    position = self.position_start
    context = self.context

    while context:
      result = f'  File {position.function_name}, line {str(position.line_number + 1)}, in {context.display_name}\n' + result
      position = context.parent_entry_position
      context = context.parent

    return 'Traceback (most recent call last):\n' + result
