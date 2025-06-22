#######################################
# SYMBOL TABLE
#######################################

class SymbolTable:
  def __init__(self, parent=None):
    self.symbols = {}
    self.constants = set()  # Track which symbols are constants
    self.parent = parent

  def get(self, name):
    value = self.symbols.get(name, None)
    if value is None and self.parent:
      return self.parent.get(name)
    return value

  def set(self, name, value, is_constant=False):
    # Check if trying to reassign a constant in the current scope
    if name in self.constants:
      # We'll raise a custom error that will be caught and converted to a proper error with position info
      raise Exception(f"CONSTANT_REASSIGNMENT:{name}")

    # Check parent scopes for constants with the same name
    if self.parent and name not in self.symbols:
      parent = self.parent
      while parent:
        if name in parent.constants:
          raise Exception(f"CONSTANT_REASSIGNMENT:{name}")
        parent = parent.parent

    self.symbols[name] = value

    # If this is a constant, mark it
    if is_constant:
      self.constants.add(name)

  def remove(self, name):
    # Don't allow removing constants
    if name in self.constants:
      raise Exception(f"CONSTANT_REASSIGNMENT:{name}")

    del self.symbols[name]
