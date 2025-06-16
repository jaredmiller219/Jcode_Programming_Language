#######################################
# PARSE RESULT
#######################################
from typing import Optional

from tokens import *
from position import *

class ParseResult:
  current_tok: Optional['Token']
  last_advanced_position: Optional['Position']
  def __init__(self):
    self.error = None
    self.node = None
    self.last_registered_advance_count = 0
    self.advance_count = 0
    self.to_reverse_count = 0
    self.last_advanced_position = None

  def register_advancement(self):
    self.last_registered_advance_count = 1
    self.advance_count += 1
    # Track the last position advanced to
    if hasattr(self, 'current_token') and self.current_token:
      self.last_advanced_position = self.current_token.position_end

  def register(self, result):
    self.last_registered_advance_count = result.advance_count
    self.advance_count += result.advance_count
    if result.error:
        # Replace only if we don't already have a better error
        if self.error is None or result.error.position_start.index > self.error.position_start.index:
            self.error = result.error
    return result.node

  def try_register(self, result):
    if result.error:
      self.to_reverse_count = result.advance_count
      return None
    return self.register(result)

  def success(self, node):
    self.node = node
    return self

  def failure(self, error):
    # Only overwrite if this error is further in the file
    if not self.error or self.last_registered_advance_count == 0 or (error.position_end.index > self.error.position_end.index):
      self.error = error
    return self
