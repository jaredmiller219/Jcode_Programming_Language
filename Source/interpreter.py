#######################################
# INTERPRETER
#######################################

from runtime_result import RuntimeResult
from values import *
from errors import *
from tokens import *
from nodes import *

class Interpreter:
  def visit(self, node, context):
    method_name = f'visit_{type(node).__name__}'
    method = getattr(self, method_name, self.no_visit_method)
    return method(node, context)

  def no_visit_method(self, node, context):
    _ = context
    raise Exception(f'No visit_{type(node).__name__} method defined')

  ###################################

  def visit_NumberNode(self, node, context):
    return RuntimeResult().success(
      Number(node.token.value).set_context(context).set_position(node.position_start, node.position_end)
    )

  def visit_StringNode(self, node, context):
    return RuntimeResult().success(
      String(node.token.value).set_context(context).set_position(node.position_start, node.position_end)
    )

  def visit_ListNode(self, node, context):
    runtimeResult = RuntimeResult()
    elements = []

    for element_node in node.element_nodes:
      elements.append(runtimeResult.register(self.visit(element_node, context)))
      if runtimeResult.should_return(): return runtimeResult

    return runtimeResult.success(
      List(elements).set_context(context).set_position(node.position_start, node.position_end)
    )

  def visit_VarAccessNode(self, node, context):
    runtimeResult = RuntimeResult()
    variable_name = node.variable_name_token.value
    value = context.symbol_table.get(variable_name)

    if value is None:
      return runtimeResult.failure(RuntimeError(
        node.position_start, node.position_end,
        f"'{variable_name}' is not defined",
        context
      ))

    value = value.copy().set_position(node.position_start, node.position_end).set_context(context)
    return runtimeResult.success(value)

  def visit_VarAssignNode(self, node, context):
    runtimeResult = RuntimeResult()
    variable_name = node.variable_name_token.value
    variable_value = runtimeResult.register(self.visit(node.value_node, context))
    if runtimeResult.should_return(): return runtimeResult

    # Type checking if a type was specified
    if node.type_token:
      type_name = node.type_token.value

      # Check if the value matches the declared type
      if type_name == 'int' and not isinstance(variable_value, Number) or (isinstance(variable_value, Number) and not isinstance(variable_value.value, int)):
        return runtimeResult.failure(RuntimeError(
          node.position_start, node.position_end,
          f"Type mismatch: Expected 'int', got '{type(variable_value).__name__}'",
          context
        ))
      elif type_name == 'float' and not isinstance(variable_value, Number):
        return runtimeResult.failure(RuntimeError(
          node.position_start, node.position_end,
          f"Type mismatch: Expected 'float', got '{type(variable_value).__name__}'",
          context
        ))
      elif type_name == 'string' and not isinstance(variable_value, String):
        return runtimeResult.failure(RuntimeError(
          node.position_start, node.position_end,
          f"Type mismatch: Expected 'string', got '{type(variable_value).__name__}'",
          context
        ))
      elif type_name == 'list' and not isinstance(variable_value, List):
        return runtimeResult.failure(RuntimeError(
          node.position_start, node.position_end,
          f"Type mismatch: Expected 'list', got '{type(variable_value).__name__}'",
          context
        ))
      elif type_name == 'function' and not isinstance(variable_value, BaseFunction):
        return runtimeResult.failure(RuntimeError(
          node.position_start, node.position_end,
          f"Type mismatch: Expected 'function', got '{type(variable_value).__name__}'",
          context
        ))

    context.symbol_table.set(variable_name, variable_value)
    return runtimeResult.success(variable_value)

  def visit_BinaryOperationNode(self, node, context):
    runtimeResult = RuntimeResult()

    error = None
    runtimeResult = RuntimeResult()

    left = runtimeResult.register(self.visit(node.left_node, context))
    if runtimeResult.should_return(): return runtimeResult
    right = runtimeResult.register(self.visit(node.right_node, context))
    if runtimeResult.should_return(): return runtimeResult

    if node.operation_token.type == TT_PLUS:
      runtimeResultult, error = left.added_to(right)
    elif node.operation_token.type == TT_MINUS:
      runtimeResultult, error = left.subtracted_by(right)
    elif node.operation_token.type == TT_MULTIPLY:
      runtimeResultult, error = left.multiplied_by(right)
    elif node.operation_token.type == TT_DIVIDE:
      runtimeResultult, error = left.divided_by(right)
    elif node.operation_token.type == TT_POWER:
      runtimeResultult, error = left.powered_by(right)
    elif node.operation_token.type == TT_EQUAL_EQUAL:
      runtimeResultult, error = left.equals(right)
    elif node.operation_token.type == TT_NOT_EQUAL:
      runtimeResultult, error = left.not_equals(right)
    elif node.operation_token.type == TT_LESS_THAN:
      runtimeResultult, error = left.less_than(right)
    elif node.operation_token.type == TT_GREATER_THAN:
      runtimeResultult, error = left.greater_than(right)
    elif node.operation_token.type == TT_LESS_THAN_EQUAL:
      runtimeResultult, error = left.less_than_or_equal_to(right)
    elif node.operation_token.type == TT_GREATER_THAN_EQUAL:
      runtimeResultult, error = left.greater_than_or_equal_to(right)
    elif node.operation_token.matches(TT_KEYWORD, 'and'):
      runtimeResultult, error = left.anded_by(right)
    elif node.operation_token.matches(TT_KEYWORD, 'or'):
      runtimeResultult, error = left.ored_by(right)

    if error:
      return runtimeResult.failure(error)
    else:
      return runtimeResult.success(runtimeResultult.set_position(node.position_start, node.position_end))

  def visit_UnaryOpNode(self, node, context):
    runtimeResult = RuntimeResult()
    number = runtimeResult.register(self.visit(node.node, context))
    if runtimeResult.should_return(): return runtimeResult

    error = None

    if node.operation_token.type == TT_MINUS:
      number, error = number.multiplied_by(Number(-1))
    elif node.operation_token.matches(TT_KEYWORD, 'not'):
      number, error = number.notted()

    if error:
      return runtimeResult.failure(error)
    else:
      return runtimeResult.success(number.set_position(node.position_start, node.position_end))

  def visit_IfNode(self, node, context):
    runtimeResult = RuntimeResult()

    for condition, expression, should_return_null in node.cases:
      condition_value = runtimeResult.register(self.visit(condition, context))
      if runtimeResult.should_return(): return runtimeResult

      if condition_value.is_true():
        expression_value = runtimeResult.register(self.visit(expression, context))
        if runtimeResult.should_return(): return runtimeResult
        return runtimeResult.success(Number.null if should_return_null else expression_value)

    if node.else_case:
      expression, should_return_null = node.else_case
      expression_value = runtimeResult.register(self.visit(expression, context))
      if runtimeResult.should_return(): return runtimeResult
      return runtimeResult.success(Number.null if should_return_null else expression_value)

    return runtimeResult.success(Number.null)

  def visit_ForNode(self, node, context):
    runtimeResult = RuntimeResult()
    elements = []

    start_value = runtimeResult.register(self.visit(node.start_value_node, context))
    if runtimeResult.should_return(): return runtimeResult

    end_value = runtimeResult.register(self.visit(node.end_value_node, context))
    if runtimeResult.should_return(): return runtimeResult

    if node.step_value_node:
      step_value = runtimeResult.register(self.visit(node.step_value_node, context))
      if runtimeResult.should_return(): return runtimeResult
    else:
      step_value = Number(1)

    index = start_value.value

    if step_value.value >= 0:
      condition = lambda: index < end_value.value
    else:
      condition = lambda: index > end_value.value

    while condition():
      context.symbol_table.set(node.variable_name_token.value, Number(index))
      index += step_value.value

      value = runtimeResult.register(self.visit(node.body_node, context))
      if runtimeResult.should_return() and runtimeResult.loop_should_continue == False and runtimeResult.loop_should_break == False: return runtimeResult
      if runtimeResult.loop_should_continue:continue
      if runtimeResult.loop_should_break: break

      elements.append(value)

    return runtimeResult.success(
      Number.null if node.should_return_null else
      List(elements).set_context(context).set_position(node.position_start, node.position_end)
    )

  def visit_WhileNode(self, node, context):
    runtimeResult = RuntimeResult()
    elements = []

    while True:
      condition = runtimeResult.register(self.visit(node.condition_node, context))
      if runtimeResult.should_return(): return runtimeResult
      if not condition.is_true():break
      value = runtimeResult.register(self.visit(node.body_node, context))
      if runtimeResult.should_return() and runtimeResult.loop_should_continue == False and runtimeResult.loop_should_break == False: return runtimeResult

      if runtimeResult.loop_should_continue:continue
      if runtimeResult.loop_should_break: break
      elements.append(value)

    return runtimeResult.success(
      Number.null if node.should_return_null else
      List(elements).set_context(context).set_position(node.position_start, node.position_end)
    )

  def visit_FuncDefNode(self, node, context):
    runtimeResult = RuntimeResult()

    function_name = node.variable_name_token.value if node.variable_name_token else None
    body_node = node.body_node
    argument_names = [argument_name.value for argument_name in node.argument_name_tokens]
    function_value = Function(function_name, body_node, argument_names, node.should_auto_return).set_context(context).set_position(node.position_start, node.position_end)

    if node.variable_name_token:
      context.symbol_table.set(function_name, function_value)

    return runtimeResult.success(function_value)

  def visit_CallNode(self, node, context):
    runtimeResult = RuntimeResult()
    arguments = []

    value_to_call = runtimeResult.register(self.visit(node.node_to_call, context))
    if runtimeResult.should_return(): return runtimeResult
    value_to_call = value_to_call.copy().set_position(node.position_start, node.position_end)

    for argument_node in node.argument_nodes:
      arguments.append(runtimeResult.register(self.visit(argument_node, context)))
      if runtimeResult.should_return(): return runtimeResult

    # Distinguish between user-defined and built-in functions
    if isinstance(value_to_call, BuiltInFunction):
        return_value = runtimeResult.register(value_to_call.execute(node, arguments, node.position_start))
    else:
        return_value = runtimeResult.register(value_to_call.execute(arguments, node.position_start))

    # return_value = runtimeResult.register(value_to_call.execute(node, arguments, node.position_start))
    if runtimeResult.should_return(): return runtimeResult
    return_value = return_value.copy().set_position(node.position_start, node.position_end).set_context(context)
    return runtimeResult.success(return_value)

  def visit_ReturnNode(self, node, context):
    runtimeResult = RuntimeResult()

    if node.node_to_return:
      value = runtimeResult.register(self.visit(node.node_to_return, context))
      if runtimeResult.should_return(): return runtimeResult
    else:
      value = Number.null

    return runtimeResult.success_return(value)

  def visit_ContinueNode(self, node, context):
    _ = node, context
    return RuntimeResult().success_continue()

  def visit_BreakNode(self, node, context):
    _ = node, context
    return RuntimeResult().success_break()
