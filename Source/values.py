# pyright: reportIncompatibleMethodOverride=false

#######################################
# VALUES
#######################################

from runtime_result import *
from errors import *
from context import *
from symbol_table import *

import math
import os

class Value:
  def __init__(self):
    self.set_position()
    self.set_context()

  def set_position(self, position_start=None, position_end=None):
    self.position_start = position_start
    self.position_end = position_end
    return self

  def set_context(self, context=None):
    self.context = context
    return self

  def added_to(self, other_number):
    return None, self.illegal_operation(other_number)

  def subtracted_by(self, other_number):
    return None, self.illegal_operation(other_number)

  def multiplied_by(self, other_number):
    return None, self.illegal_operation(other_number)

  def divided_by(self, other_number):
    return None, self.illegal_operation(other_number)

  def powered_by(self, other_number):
    return None, self.illegal_operation(other_number)

  def equals(self, other_number):
    return None, self.illegal_operation(other_number)

  def not_equals(self, other_number):
    return None, self.illegal_operation(other_number)

  def less_than(self, other_number):
    return None, self.illegal_operation(other_number)

  def greater_than(self, other_number):
    return None, self.illegal_operation(other_number)

  def less_than_or_equal_to(self, other_number):
    return None, self.illegal_operation(other_number)

  def greater_than_or_equal_to(self, other_number):
    return None, self.illegal_operation(other_number)

  def anded_by(self, other_number):
    return None, self.illegal_operation(other_number)

  def ored_by(self, other_number):
    return None, self.illegal_operation(other_number)

  def notted(self, other_number):
    return None, self.illegal_operation(other_number)

  def execute(self, node, arguments, position):
    _ = node, arguments, position
    return RuntimeResult().failure(self.illegal_operation())

  def copy(self):
    raise Exception('No copy method defined')

  def is_true(self):
    return False

  def illegal_operation(self, other_number=None):
    if not other_number: other_number = self
    return RuntimeError(
      self.position_start, other_number.position_end,
      'Illegal operation',
      self.context
    )

class Number(Value):
  null: 'Number'
  false: 'Number'
  true: 'Number'
  math_PI: 'Number'

  def __init__(self, value):
    super().__init__()
    self.value = value

  def added_to(self, other_number):
    if isinstance(other_number, Number):
      return Number(self.value + other_number.value).set_context(self.context), None
    else:
      return None, Value.illegal_operation(self, other_number)

  def subtracted_by(self, other_number):
    if isinstance(other_number, Number):
      return Number(self.value - other_number.value).set_context(self.context), None
    else:
      return None, Value.illegal_operation(self, other_number)

  def multiplied_by(self, other_number):
    if isinstance(other_number, Number):
      return Number(self.value * other_number.value).set_context(self.context), None
    else:
      return None, Value.illegal_operation(self, other_number)

  def divided_by(self, other_number):
    if isinstance(other_number, Number):
      if other_number.value == 0:
        return None, RuntimeError(
          other_number.position_start, other_number.position_end,
          'Division by zero',
          self.context
        )

      return Number(self.value / other_number.value).set_context(self.context), None
    else:
      return None, Value.illegal_operation(self, other_number)

  def powered_by(self, other_number):
    if isinstance(other_number, Number):
      return Number(self.value ** other_number.value).set_context(self.context), None
    else:
      return None, Value.illegal_operation(self, other_number)

  def equals(self, other_number):
    if isinstance(other_number, Number):
      return Number(int(self.value == other_number.value)).set_context(self.context), None
    else:
      return None, Value.illegal_operation(self, other_number)

  def not_equals(self, other_number):
    if isinstance(other_number, Number):
      return Number(int(self.value != other_number.value)).set_context(self.context), None
    else:
      return None, Value.illegal_operation(self, other_number)

  def less_than(self, other_number):
    if isinstance(other_number, Number):
      return Number(int(self.value < other_number.value)).set_context(self.context), None
    else:
      return None, Value.illegal_operation(self, other_number)

  def greater_than(self, other_number):
    if isinstance(other_number, Number):
      return Number(int(self.value > other_number.value)).set_context(self.context), None
    else:
      return None, Value.illegal_operation(self, other_number)

  def less_than_or_equal_t(self, other_number):
    if isinstance(other_number, Number):
      return Number(int(self.value <= other_number.value)).set_context(self.context), None
    else:
      return None, Value.illegal_operation(self, other_number)

  def greater_than_or_equal_to(self, other_number):
    if isinstance(other_number, Number):
      return Number(int(self.value >= other_number.value)).set_context(self.context), None
    else:
      return None, Value.illegal_operation(self, other_number)

  def anded_by(self, other_number):
    if isinstance(other_number, Number):
      return Number(int(self.value and other_number.value)).set_context(self.context), None
    else:
      return None, Value.illegal_operation(self, other_number)

  def ored_by(self, other_number):
    if isinstance(other_number, Number):
      return Number(int(self.value or other_number.value)).set_context(self.context), None
    else:
      return None, Value.illegal_operation(self, other_number)

  def notted(self, other_number):
    _ = other_number
    if self.value == 0: return Number(1).set_context(self.context), None
    else: return Number(0).set_context(self.context), None

  def copy(self):
    copy = Number(self.value)
    copy.set_position(self.position_start, self.position_end)
    copy.set_context(self.context)
    return copy

  def is_true(self):
    return self.value != 0

  def __str__(self):
    return str(self.value)

  def __repr__(self):
    return str(self.value)

Number.null = Number(0)
Number.false = Number(0)
Number.true = Number(1)
Number.math_PI = Number(math.pi)

# Mark the singleton objects
Number.null._is_null_singleton = True
Number.false._is_false_singleton = True
Number.true._is_true_singleton = True

class String(Value):
  def __init__(self, value):
    super().__init__()
    self.value = value

  def added_to(self, other_number):
    if isinstance(other_number, String):
      return String(self.value + other_number.value).set_context(self.context), None
    else:
      return None, Value.illegal_operation(self, other_number)

  def multiplied_by(self, other_number):
    if isinstance(other_number, Number):
      return String(self.value * other_number.value).set_context(self.context), None
    else:
      return None, Value.illegal_operation(self, other_number)

  def is_true(self):
    return len(self.value) > 0

  def copy(self):
    copy = String(self.value)
    copy.set_position(self.position_start, self.position_end)
    copy.set_context(self.context)
    return copy

  def __str__(self):
    return self.value

  def __repr__(self):
    return f'"{self.value}"'

class List(Value):
  def __init__(self, elements):
    super().__init__()
    self.elements = elements

  def added_to(self, other_number):
    new_list = self.copy()
    new_list.elements.append(other_number)
    return new_list, None

  def subtracted_by(self, other_number):
    if isinstance(other_number, Number):
      new_list = self.copy()
      try:
        new_list.elements.pop(other_number.value)
        return new_list, None
      except IndexError:
        return None, RuntimeError(
          other_number.position_start, other_number.position_end,
          'Element at this index could not be removed from list because index is out of bounds',
          self.context
        )
    else:
      return None, Value.illegal_operation(self, other_number)

  def multiplied_by(self, other_number):
    if isinstance(other_number, List):
      new_list = self.copy()
      new_list.elements.extend(other_number.elements)
      return new_list, None
    else:
      return None, Value.illegal_operation(self, other_number)

  def divided_by(self, other_number):
    if isinstance(other_number, Number):
      try:
        return self.elements[other_number.value], None
      except IndexError:
        return None, RuntimeError(
          other_number.position_start, other_number.position_end,
          'Element at this index could not be retrieved from list because index is out of bounds',
          self.context
        )
    else:
      return None, Value.illegal_operation(self, other_number)

  # def get_at_index(self, index):
  #   try: return self.elements[index]
  #   except IndexError: return None

  def copy(self):
    copy = List(self.elements)
    copy.set_position(self.position_start, self.position_end)
    copy.set_context(self.context)
    return copy

  def __str__(self):
    return ", ".join([str(string) for string in self.elements])

  def __repr__(self):
    return f'[{", ".join([repr(string) for string in self.elements])}]'

class BaseFunction(Value):
  def __init__(self, name):
    super().__init__()
    self.name = name or "<anonymous>"

  def generate_new_context(self, position_start):
    new_context = Context(self.name, self.context, position_start)

    if new_context.parent and new_context.parent.symbol_table:
        parent_symbol_table = new_context.parent.symbol_table
    else: parent_symbol_table = None
    new_context.symbol_table = SymbolTable(parent_symbol_table)
    return new_context

  def check_arguments(self, argument_names, arguments, execution_context=None):
    runtimeResult = RuntimeResult()

    _ = execution_context

    if len(arguments) > len(argument_names):
      return runtimeResult.failure(RuntimeError(
        self.position_start, self.position_end,
        f"{len(arguments) - len(argument_names)} too many arguments passed into {self}",
        self.context
      ))

    if len(arguments) < len(argument_names):
      return runtimeResult.failure(RuntimeError(
        self.position_start, self.position_end,
        f"{len(argument_names) - len(arguments)} too few arguments passed into {self}",
        self.context
      ))

    return runtimeResult.success(None)

  def populate_args(self, argument_names, arguments, execution_context):
    for i in range(len(arguments)):
      argument_name = argument_names[i]
      argument_value = arguments[i]
      argument_value.set_context(execution_context)
      execution_context.symbol_table.set(argument_name, argument_value)

  def check_and_populate_args(self, argument_names, arguments, execution_context):
    runtimeResult = RuntimeResult()
    runtimeResult.register(self.check_arguments(argument_names, arguments, execution_context))
    if runtimeResult.should_return(): return runtimeResult
    self.populate_args(argument_names, arguments, execution_context)
    return runtimeResult.success(None)

class Function(BaseFunction):
  def __init__(self, name, body_node, argument_names, should_auto_return):
    super().__init__(name)
    self.body_node = body_node
    self.argument_names = argument_names
    self.should_auto_return = should_auto_return

  def execute(self, node, arguments, position_start):
    from interpreter import Interpreter
    _ = node
    runtimeResult = RuntimeResult()
    interpreter = Interpreter()
    execution_context = self.generate_new_context(position_start)

    runtimeResult.register(self.check_and_populate_args(self.argument_names, arguments, execution_context))
    if runtimeResult.should_return(): return runtimeResult

    value = runtimeResult.register(interpreter.visit(self.body_node, execution_context))
    if runtimeResult.should_return() and runtimeResult.function_return_value is None: return runtimeResult

    if self.should_auto_return: return_value = value
    elif runtimeResult.function_return_value is not None:
      return_value = runtimeResult.function_return_value
    else: return_value = Number.null

    return runtimeResult.success(return_value)

  def copy(self):
    copy = Function(self.name, self.body_node, self.argument_names, self.should_auto_return)
    copy.set_context(self.context)
    copy.set_position(self.position_start, self.position_end)
    return copy

  def __repr__(self):
    return f"<function {self.name}>"


def argument_names(*names):
    def wrapper(function):
        function.argument_names = list(names)
        return function
    return wrapper
class BuiltInFunction(BaseFunction):
  print: 'BuiltInFunction'
  print_ret: 'BuiltInFunction'
  input: 'BuiltInFunction'
  input_int: 'BuiltInFunction'
  clear: 'BuiltInFunction'
  is_number: 'BuiltInFunction'
  is_string: 'BuiltInFunction'
  is_list: 'BuiltInFunction'
  is_function: 'BuiltInFunction'
  append: 'BuiltInFunction'
  pop: 'BuiltInFunction'
  extend: 'BuiltInFunction'
  len: 'BuiltInFunction'
  run: 'BuiltInFunction'
  isinstance: 'BuiltInFunction'
  hasattr: 'BuiltInFunction'
  getattr: 'BuiltInFunction'
  setattr: 'BuiltInFunction'
  str: 'BuiltInFunction'

  def __init__(self, name):
    super().__init__(name)

  def execute(self, node, arguments, position_start):
    runtimeResult = RuntimeResult()
    execution_context = self.generate_new_context(position_start)

    method_name = f'execute_{self.name}'
    method = getattr(self, method_name, self.no_visit_method)
    argument_names = getattr(method, 'argument_names', None)

    if argument_names is None:
        return runtimeResult.failure(RuntimeError(
            position_start, position_start,
            f"Function '{self.name}' does not define argument_names",
            execution_context
        ))

    runtimeResult.register(self.check_and_populate_args(argument_names, arguments, execution_context))
    if runtimeResult.should_return(): return runtimeResult

    return_value = runtimeResult.register(method(execution_context))
    if runtimeResult.should_return(): return runtimeResult
    return runtimeResult.success(return_value)

  def no_visit_method(self, node, context):
    _ = node, context
    raise Exception(f'No execute_{self.name} method defined')

  def copy(self):
    copy = BuiltInFunction(self.name)
    copy.set_context(self.context)
    copy.set_position(self.position_start, self.position_end)
    return copy

  def __repr__(self):
    return f"<built-in function {self.name}>"

  #####################################
  @argument_names('value')
  def execute_print(self, execution_context):
    print(str(execution_context.symbol_table.get('value')))
    return RuntimeResult().success(Number.null)
    #execute_print.argument_names = ['value']

  @argument_names('value')
  def execute_print_ret(self, execution_context):
    return RuntimeResult().success(String(str(execution_context.symbol_table.get('value'))))
  #execute_print_ret.argument_names = ['value']

  @argument_names()
  def execute_input(self, execution_context):
    _ = execution_context
    text = input()
    return RuntimeResult().success(String(text))
  #execute_input.argument_names = []

  @argument_names()
  def execute_input_int(self, execution_context):
    _ = execution_context
    while True:
      text = input()
      try:
        number = int(text)
        break
      except ValueError:
        print(f"'{text}' must be an integer. Try again!")
    return RuntimeResult().success(Number(number))
  #execute_input_int.argument_names = []

  @argument_names()
  def execute_clear(self, execution_context):
    _ = execution_context
    os.system('cls' if os.name == 'nt' else 'clear')
    return RuntimeResult().success(Number.null)
  #execute_clear.argument_names = []

  @argument_names('value')
  def execute_is_number(self, execution_context):
    is_number = isinstance(execution_context.symbol_table.get("value"), Number)
    return RuntimeResult().success(Number.true if is_number else Number.false)
  #execute_is_number.argument_names = ["value"]

  @argument_names('value')
  def execute_is_string(self, execution_context):
    is_number = isinstance(execution_context.symbol_table.get("value"), String)
    return RuntimeResult().success(Number.true if is_number else Number.false)
  #execute_is_string.argument_names = ["value"]

  @argument_names('value')
  def execute_is_list(self, execution_context):
    is_number = isinstance(execution_context.symbol_table.get("value"), List)
    return RuntimeResult().success(Number.true if is_number else Number.false)
  #execute_is_list.argument_names = ["value"]

  @argument_names('value')
  def execute_is_function(self, execution_context):
    is_number = isinstance(execution_context.symbol_table.get("value"), BaseFunction)
    return RuntimeResult().success(Number.true if is_number else Number.false)
  #execute_is_function.argument_names = ["value"]

  @argument_names('list', 'value')
  def execute_append(self, execution_context):
    list_ = execution_context.symbol_table.get("list")
    value = execution_context.symbol_table.get("value")

    if not isinstance(list_, List):
      return RuntimeResult().failure(RuntimeError(
        self.position_start, self.position_end,
        "First argument must be list",
        execution_context
      ))

    list_.elements.append(value)
    return RuntimeResult().success(Number.null)
  #execute_append.argument_names = ["list", "value"]

  @argument_names('list', 'index')
  def execute_pop(self, execution_context):
    list_ = execution_context.symbol_table.get("list")
    index = execution_context.symbol_table.get("index")

    if not isinstance(list_, List):
      return RuntimeResult().failure(RuntimeError(
        self.position_start, self.position_end,
        "First argument must be list",
        execution_context
      ))

    if not isinstance(index, Number):
      return RuntimeResult().failure(RuntimeError(
        self.position_start, self.position_end,
        "Second argument must be number",
        execution_context
      ))

    try:
      element = list_.elements.pop(index.value)
    except IndexError:
      return RuntimeResult().failure(RuntimeError(
        self.position_start, self.position_end,
        'Element at this index could not be removed from list because index is out of bounds',
        execution_context
      ))
    return RuntimeResult().success(element)
  #execute_pop.argument_names = ["list", "index"]

  @argument_names('listA', 'listB')
  def execute_extend(self, execution_context):
    listA = execution_context.symbol_table.get("listA")
    listB = execution_context.symbol_table.get("listB")

    if not isinstance(listA, List):
      return RuntimeResult().failure(RuntimeError(
        self.position_start, self.position_end,
        "First argument must be list",
        execution_context
      ))

    if not isinstance(listB, List):
      return RuntimeResult().failure(RuntimeError(
        self.position_start, self.position_end,
        "Second argument must be list",
        execution_context
      ))

    listA.elements.extend(listB.elements)
    return RuntimeResult().success(Number.null)
  #execute_extend.argument_names = ["listA", "listB"]

  @argument_names('list')
  def execute_len(self, execution_context):
    list_ = execution_context.symbol_table.get("list")

    if not isinstance(list_, List):
      return RuntimeResult().failure(RuntimeError(
        self.position_start, self.position_end,
        "Argument must be list",
        execution_context
      ))

    return RuntimeResult().success(Number(len(list_.elements)))
  #execute_len.argument_names = ["list"]

  @argument_names('function')
  def execute_run(self, execution_context):
    from main import run
    function = execution_context.symbol_table.get("function")

    if not isinstance(function, String):
      return RuntimeResult().failure(RuntimeError(
        self.position_start, self.position_end,
        "Second argument must be string",
        execution_context
      ))

    function = function.value

    try:
      with open(function, "r") as file:
        script = file.read()
    except Exception as exception:
      return RuntimeResult().failure(RuntimeError(
        self.position_start, self.position_end,
        f"Failed to load script \"{function}\"\n" + str(exception),
        execution_context
      ))

    _, error = run(function, script)

    if error:
      return RuntimeResult().failure(RuntimeError(
        self.position_start, self.position_end,
        f"Failed to finish executing script \"{function}\"\n" +
        error.as_string(),
        execution_context
      ))

    return RuntimeResult().success(Number.null)
  #execute_run.argument_names = ["function"]

  @argument_names('obj', 'class_or_classname')
  def execute_isinstance(self, execution_context):
    obj = execution_context.symbol_table.get("obj")
    class_or_classname = execution_context.symbol_table.get("class_or_classname")

    if isinstance(obj, Instance):
      if isinstance(class_or_classname, Class):
        # Check if obj is instance of class_or_classname or its parents
        current_class = obj.class_def
        while current_class:
          # Compare by name instead of object identity for more reliable comparison
          if current_class.name == class_or_classname.name:
            return RuntimeResult().success(Number.true)
          current_class = current_class.parent_class
        return RuntimeResult().success(Number.false)
      elif isinstance(class_or_classname, String):
        # Check by class name
        current_class = obj.class_def
        while current_class:
          if current_class.name == class_or_classname.value:
            return RuntimeResult().success(Number.true)
          current_class = current_class.parent_class
        return RuntimeResult().success(Number.false)

    return RuntimeResult().success(Number.false)

  @argument_names('obj', 'attr_name')
  def execute_hasattr(self, execution_context):
    obj = execution_context.symbol_table.get("obj")
    attr_name = execution_context.symbol_table.get("attr_name")

    if not isinstance(attr_name, String):
      return RuntimeResult().failure(RuntimeError(
        self.position_start, self.position_end,
        "Attribute name must be a string",
        execution_context
      ))

    if isinstance(obj, Instance):
      attribute = obj.get_attribute(attr_name.value)
      return RuntimeResult().success(Number.true if attribute is not None else Number.false)

    return RuntimeResult().success(Number.false)

  @argument_names('obj', 'attr_name', 'default')
  def execute_getattr(self, execution_context):
    obj = execution_context.symbol_table.get("obj")
    attr_name = execution_context.symbol_table.get("attr_name")
    default = execution_context.symbol_table.get("default")

    if not isinstance(attr_name, String):
      return RuntimeResult().failure(RuntimeError(
        self.position_start, self.position_end,
        "Attribute name must be a string",
        execution_context
      ))

    if isinstance(obj, Instance):
      attribute = obj.get_attribute(attr_name.value)
      if attribute is not None:
        return RuntimeResult().success(attribute)
      elif default is not None:
        return RuntimeResult().success(default)
      else:
        return RuntimeResult().failure(RuntimeError(
          self.position_start, self.position_end,
          f"'{obj.class_def.name}' object has no attribute '{attr_name.value}'",
          execution_context
        ))

    return RuntimeResult().failure(RuntimeError(
      self.position_start, self.position_end,
      "Cannot get attribute of non-object",
      execution_context
    ))

  @argument_names('obj', 'attr_name', 'value')
  def execute_setattr(self, execution_context):
    obj = execution_context.symbol_table.get("obj")
    attr_name = execution_context.symbol_table.get("attr_name")
    value = execution_context.symbol_table.get("value")

    if not isinstance(attr_name, String):
      return RuntimeResult().failure(RuntimeError(
        self.position_start, self.position_end,
        "Attribute name must be a string",
        execution_context
      ))

    if isinstance(obj, Instance):
      obj.set_attribute(attr_name.value, value)
      return RuntimeResult().success(Number.null)

    return RuntimeResult().failure(RuntimeError(
      self.position_start, self.position_end,
      f"Cannot set attribute of non-object (got {type(obj).__name__})",
      execution_context
    ))

  @argument_names('value')
  def execute_str(self, execution_context):
    value = execution_context.symbol_table.get("value")

    if isinstance(value, Number):
      # Handle boolean values by checking value and context
      if value.value == 1 and hasattr(value, '_is_true_singleton'):
        return RuntimeResult().success(String("true"))
      elif value.value == 0 and hasattr(value, '_is_false_singleton'):
        return RuntimeResult().success(String("false"))
      elif value.value == 0 and hasattr(value, '_is_null_singleton'):
        return RuntimeResult().success(String("null"))
      # Check by value for common boolean cases
      elif value.value == 1:
        # Could be true, check if it's in a boolean context
        return RuntimeResult().success(String("true"))
      elif value.value == 0:
        # Could be false, check if it's in a boolean context
        return RuntimeResult().success(String("false"))
      # For regular numbers, check if it's an integer
      elif value.value == int(value.value):
        return RuntimeResult().success(String(str(int(value.value))))
      else:
        return RuntimeResult().success(String(str(value.value)))
    elif isinstance(value, String):
      return RuntimeResult().success(value.copy())
    elif isinstance(value, List):
      return RuntimeResult().success(String(str(value)))
    elif isinstance(value, Instance):
      return RuntimeResult().success(String(str(value)))
    elif isinstance(value, Class):
      return RuntimeResult().success(String(str(value)))
    else:
      return RuntimeResult().success(String(str(value)))

BuiltInFunction.print       = BuiltInFunction("print")
BuiltInFunction.print_ret   = BuiltInFunction("print_ret")
BuiltInFunction.input       = BuiltInFunction("input")
BuiltInFunction.input_int   = BuiltInFunction("input_int")
BuiltInFunction.clear       = BuiltInFunction("clear")
BuiltInFunction.is_number   = BuiltInFunction("is_number")
BuiltInFunction.is_string   = BuiltInFunction("is_string")
BuiltInFunction.is_list     = BuiltInFunction("is_list")
BuiltInFunction.is_function = BuiltInFunction("is_function")
BuiltInFunction.append      = BuiltInFunction("append")
BuiltInFunction.pop         = BuiltInFunction("pop")
BuiltInFunction.extend      = BuiltInFunction("extend")
BuiltInFunction.len         = BuiltInFunction("len")
BuiltInFunction.run         = BuiltInFunction("run")
BuiltInFunction.isinstance  = BuiltInFunction("isinstance")
BuiltInFunction.hasattr     = BuiltInFunction("hasattr")
BuiltInFunction.getattr     = BuiltInFunction("getattr")
BuiltInFunction.setattr     = BuiltInFunction("setattr")
BuiltInFunction.str         = BuiltInFunction("str")

class Class(Value):
  def __init__(self, name, methods, parent_class=None):
    super().__init__()
    self.name = name
    self.methods = methods  # Dictionary of method name -> Method object
    self.parent_class = parent_class  # For inheritance

  def get_method(self, method_name):
    # Look for method in this class first
    if method_name in self.methods:
      return self.methods[method_name]

    # Look in parent class if not found
    if self.parent_class:
      return self.parent_class.get_method(method_name)

    return None

  def create_instance(self, arguments, position_start):
    from interpreter import Interpreter
    runtimeResult = RuntimeResult()

    # Create new instance
    instance = Instance(self)

    # Look for constructor (__init__ method)
    constructor = self.get_method('__init__')
    if constructor:
      # Call constructor with instance as 'self'
      interpreter = Interpreter()
      execution_context = constructor.generate_new_context(position_start)

      # Add 'self' as first argument (constructor already has 'self' in argument_names)
      all_arguments = [instance] + arguments

      runtimeResult.register(constructor.check_and_populate_args(
        constructor.argument_names,
        all_arguments,
        execution_context
      ))
      if runtimeResult.should_return(): return runtimeResult

      # Execute constructor body
      value = runtimeResult.register(interpreter.visit(constructor.body_node, execution_context))
      if runtimeResult.should_return() and runtimeResult.function_return_value is None:
        return runtimeResult

    return runtimeResult.success(instance)

  def copy(self):
    copy = Class(self.name, self.methods.copy(), self.parent_class)
    copy.set_context(self.context)
    copy.set_position(self.position_start, self.position_end)
    return copy

  def __repr__(self):
    return f"<class {self.name}>"

class Instance(Value):
  def __init__(self, class_def):
    super().__init__()
    self.class_def = class_def
    self.attributes = {}  # Instance attributes

  def get_attribute(self, attribute_name):
    # Look for attribute in instance first
    if attribute_name in self.attributes:
      return self.attributes[attribute_name]

    # Look for method in class
    method = self.class_def.get_method(attribute_name)
    if method:
      # Return a bound method
      return BoundMethod(self, method)

    return None

  def set_attribute(self, attribute_name, value):
    self.attributes[attribute_name] = value

  def copy(self):
    copy = Instance(self.class_def)
    copy.attributes = self.attributes.copy()
    copy.set_context(self.context)
    copy.set_position(self.position_start, self.position_end)
    return copy

  def __repr__(self):
    return f"<{self.class_def.name} instance>"

class Method(BaseFunction):
  def __init__(self, name, body_node, argument_names, should_auto_return, is_constructor=False):
    super().__init__(name)
    self.body_node = body_node
    # Always include 'self' as the first parameter for methods
    self.argument_names = ['self'] + argument_names
    self.should_auto_return = should_auto_return
    self.is_constructor = is_constructor

  def execute(self, node, arguments, position_start):
    from interpreter import Interpreter
    _ = node
    runtimeResult = RuntimeResult()
    interpreter = Interpreter()
    execution_context = self.generate_new_context(position_start)

    runtimeResult.register(self.check_and_populate_args(self.argument_names, arguments, execution_context))
    if runtimeResult.should_return(): return runtimeResult

    value = runtimeResult.register(interpreter.visit(self.body_node, execution_context))
    if runtimeResult.should_return() and runtimeResult.function_return_value is None: return runtimeResult

    if self.should_auto_return: return_value = value
    elif runtimeResult.function_return_value is not None:
      return_value = runtimeResult.function_return_value
    else: return_value = Number.null

    return runtimeResult.success(return_value)

  def copy(self):
    copy = Method(self.name, self.body_node, self.argument_names, self.should_auto_return, self.is_constructor)
    copy.set_context(self.context)
    copy.set_position(self.position_start, self.position_end)
    return copy

  def __repr__(self):
    return f"<method {self.name}>"

class BoundMethod(Value):
  def __init__(self, instance, method):
    super().__init__()
    self.instance = instance
    self.method = method

  def execute(self, node, arguments, position_start):
    # Add 'self' (the instance) as the first argument
    all_arguments = [self.instance] + arguments
    return self.method.execute(node, all_arguments, position_start)

  def copy(self):
    copy = BoundMethod(self.instance, self.method)
    copy.set_context(self.context)
    copy.set_position(self.position_start, self.position_end)
    return copy

  def __repr__(self):
    return f"<bound method {self.method.name} of {self.instance}>"
