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
      except:
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
      except:
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


def argnames(*names):
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
  @argnames('value')
  def execute_print(self, execution_context):
    print(str(execution_context.symbol_table.get('value')))
    return RuntimeResult().success(Number.null)
    #execute_print.argument_names = ['value']

  @argnames('value')
  def execute_print_ret(self, execution_context):
    return RuntimeResult().success(String(str(execution_context.symbol_table.get('value'))))
  #execute_print_ret.argument_names = ['value']

  @argnames()
  def execute_input(self, execution_context):
    _ = execution_context
    text = input()
    return RuntimeResult().success(String(text))
  #execute_input.argument_names = []

  @argnames()
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

  @argnames()
  def execute_clear(self, execution_context):
    _ = execution_context
    os.system('cls' if os.name == 'nt' else 'clear')
    return RuntimeResult().success(Number.null)
  #execute_clear.argument_names = []

  @argnames('value')
  def execute_is_number(self, execution_context):
    is_number = isinstance(execution_context.symbol_table.get("value"), Number)
    return RuntimeResult().success(Number.true if is_number else Number.false)
  #execute_is_number.argument_names = ["value"]

  @argnames('value')
  def execute_is_string(self, execution_context):
    is_number = isinstance(execution_context.symbol_table.get("value"), String)
    return RuntimeResult().success(Number.true if is_number else Number.false)
  #execute_is_string.argument_names = ["value"]

  @argnames('value')
  def execute_is_list(self, execution_context):
    is_number = isinstance(execution_context.symbol_table.get("value"), List)
    return RuntimeResult().success(Number.true if is_number else Number.false)
  #execute_is_list.argument_names = ["value"]

  @argnames('value')
  def execute_is_function(self, execution_context):
    is_number = isinstance(execution_context.symbol_table.get("value"), BaseFunction)
    return RuntimeResult().success(Number.true if is_number else Number.false)
  #execute_is_function.argument_names = ["value"]

  @argnames('list', 'value')
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

  @argnames('list', 'index')
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
    except:
      return RuntimeResult().failure(RuntimeError(
        self.position_start, self.position_end,
        'Element at this index could not be removed from list because index is out of bounds',
        execution_context
      ))
    return RuntimeResult().success(element)
  #execute_pop.argument_names = ["list", "index"]

  @argnames('listA', 'listB')
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

  @argnames('list')
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

  @argnames('function')
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
