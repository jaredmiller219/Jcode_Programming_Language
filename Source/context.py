#######################################
# CONTEXT
#######################################
from typing import Optional

from symbol_table import SymbolTable

class Context:
  symbol_table: Optional['SymbolTable']
  def __init__(self, display_name, parent=None, parent_entry_position=None):
    self.display_name = display_name
    self.parent = parent
    self.parent_entry_position = parent_entry_position
    self.symbol_table = None
