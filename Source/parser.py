#######################################
# PARSER
#######################################

from parse_result import *
from tokens import *
from errors import *
from nodes import *
from utils import suggest_keyword

class Parser:
  def __init__(self, tokens):
    self.tokens = tokens
    self.token_index = -1
    self.advance()

  def advance(self):
    self.token_index += 1
    self.update_current_token()
    return self.current_token

  def reverse(self, amount=1):
    self.token_index -= amount
    self.update_current_token()
    return self.current_token

  def update_current_token(self):
    if self.token_index >= 0 and self.token_index < len(self.tokens):
      self.current_token = self.tokens[self.token_index]

  def peek_next_token(self):
    """Look ahead at the next token without advancing"""
    peek_index = self.token_index + 1
    if peek_index < len(self.tokens):
      return self.tokens[peek_index]
    return None

  def parse(self):
    parseResult = self.statements()
    if not parseResult.error and self.current_token.type != TT_END_OF_FILE:
      return parseResult.failure(InvalidSyntaxError(
        self.current_token.position_start, self.current_token.position_end,
        "Token cannot appear after previous tokens"
      ))
    return parseResult

  ###################################

  def statements(self):
    parseResult = ParseResult()
    statements = []
    position_start = self.current_token.position_start.copy()

    # Suggest keyword if identifier is close to a keyword
    if self.current_token.type == TT_IDENTIFIER:
        suggestion = suggest_keyword(self.current_token.value)
        if suggestion:
            return parseResult.failure(InvalidSyntaxError(
                self.current_token.position_start, self.current_token.position_end,
                f"Unexpected identifier '{self.current_token.value}'. Did you mean '{suggestion}'?"
            ))

    while self.current_token.type == TT_NEWLINE:
      parseResult.register_advancement()
      self.advance()

    statement = parseResult.register(self.statement())
    if parseResult.error: return parseResult
    statements.append(statement)

    more_statements = True

    while True:
      newline_count = 0
      while self.current_token.type == TT_NEWLINE:
        parseResult.register_advancement()
        self.advance()
        newline_count += 1
      if newline_count == 0:
        more_statements = False

      if not more_statements: break
      statement = parseResult.try_register(self.statement())
      if not statement:
        self.reverse(parseResult.to_reverse_count)
        more_statements = False
        continue
      statements.append(statement)

    return parseResult.success(ListNode(
      statements,
      position_start,
      self.current_token.position_end.copy()
    ))

  def statement(self):
    parseResult = ParseResult()
    position_start = self.current_token.position_start.copy()

    # Suggest keyword if identifier is close to a keyword at the start of a statement
    if self.current_token.type == TT_IDENTIFIER:
        suggestion = suggest_keyword(self.current_token.value)
        if suggestion:
            return parseResult.failure(InvalidSyntaxError(
                self.current_token.position_start, self.current_token.position_end,
                f"Unexpected identifier '{self.current_token.value}'. Did you mean '{suggestion}'?"
            ))

    if self.current_token.matches(TT_KEYWORD, 'return'):
      parseResult.register_advancement()
      self.advance()

      expression = parseResult.try_register(self.expression())
      if not expression: self.reverse(parseResult.to_reverse_count)
      return parseResult.success(ReturnNode(expression, position_start, self.current_token.position_start.copy()))

    if self.current_token.matches(TT_KEYWORD, 'continue'):
      parseResult.register_advancement()
      self.advance()
      return parseResult.success(ContinueNode(position_start, self.current_token.position_start.copy()))

    if self.current_token.matches(TT_KEYWORD, 'break'):
      parseResult.register_advancement()
      self.advance()
      return parseResult.success(BreakNode(position_start, self.current_token.position_start.copy()))

    expression = parseResult.register(self.expression())
    if parseResult.error:
      return parseResult.failure(InvalidSyntaxError(
        self.current_token.position_start, self.current_token.position_end,
        "Expected 'return', 'continue', 'break', 'var', 'if', 'for', 'while', 'func', int, float, identifier, '+', '-', '(', '[' or 'not'"
      ))
    return parseResult.success(expression)

  def expression(self):
    parseResult = ParseResult()
    parseResult.current_token = self.current_token

    # Suggest keyword if identifier is close to a keyword
    if self.current_token.type == TT_IDENTIFIER:
        suggestion = suggest_keyword(self.current_token.value)
        if suggestion:
            return parseResult.failure(InvalidSyntaxError(
                self.current_token.position_start, self.current_token.position_end,
                f"Unexpected identifier '{self.current_token.value}'. Did you mean '{suggestion}'?"
            ))

    # Check for type keywords used as variable declarations
    if self.current_token.type == TT_IDENTIFIER and self.current_token.value in ['int', 'float', 'string', 'list', 'function']:
      type_token = self.current_token
      parseResult.register_advancement()
      self.advance()

      if self.current_token.type != TT_IDENTIFIER:
        return parseResult.failure(InvalidSyntaxError(
          self.current_token.position_start, self.current_token.position_end,
          "Expected identifier"
        ))

      variable_name = self.current_token
      parseResult.register_advancement()
      self.advance()

      if self.current_token.type != TT_EQUAL and self.current_token.type != TT_COLON:
        return parseResult.failure(InvalidSyntaxError(
          self.current_token.position_start, self.current_token.position_end,
          "Expected '=' or ':'"
        ))

      is_colon = self.current_token.type == TT_COLON
      parseResult.register_advancement()
      self.advance()

      expression = parseResult.register(self.expression())
      if parseResult.error: return parseResult
      return parseResult.success(VarAssignNode(variable_name, expression, type_token))

    # Original var keyword handling
    elif self.current_token.matches(TT_KEYWORD, 'var'):
      parseResult.register_advancement()
      self.advance()

      if self.current_token.type != TT_IDENTIFIER:
        return parseResult.failure(InvalidSyntaxError(
          self.current_token.position_start, self.current_token.position_end,
          "Expected identifier"
        ))

      variable_name = self.current_token
      parseResult.register_advancement()
      self.advance()

      # Handle colon - could be type annotation or assignment
      if self.current_token.type == TT_COLON:
        parseResult.register_advancement()
        self.advance()

        expression = parseResult.register(self.expression())
        if parseResult.error: return parseResult
        return parseResult.success(VarAssignNode(variable_name, expression))

      # Regular equals assignment
      if self.current_token.type != TT_EQUAL:
        return parseResult.failure(InvalidSyntaxError(
          self.current_token.position_start, self.current_token.position_end,
          "Expected '=' or ':'"
        ))

      parseResult.register_advancement()
      self.advance()
      expression = parseResult.register(self.expression())
      if parseResult.error: return parseResult
      return parseResult.success(VarAssignNode(variable_name, expression))

    node = parseResult.register(self.binary_operation(self.comparison_expression, ((TT_KEYWORD, 'and'), (TT_KEYWORD, 'or'))))

    if parseResult.error:
      return parseResult.failure(InvalidSyntaxError(
        self.current_token.position_start, self.current_token.position_end,
        "Expected 'var', 'if', 'for', 'while', 'func', int, float, identifier, '+', '-', '(', '[' or 'not'"
      ))

    return parseResult.success(node)

  def comparison_expression(self):
    parseResult = ParseResult()

    if self.current_token.matches(TT_KEYWORD, 'not'):
      operation_token = self.current_token
      parseResult.register_advancement()
      self.advance()

      node = parseResult.register(self.comparison_expression())
      if parseResult.error: return parseResult
      return parseResult.success(UnaryOpNode(operation_token, node))

    node = parseResult.register(self.binary_operation(self.arithmatic_expression, (TT_EQUAL_EQUAL, TT_NOT_EQUAL, TT_LESS_THAN, TT_GREATER_THAN, TT_LESS_THAN_EQUAL, TT_GREATER_THAN_EQUAL)))

    if parseResult.error:
      return parseResult.failure(InvalidSyntaxError(
        self.current_token.position_start, self.current_token.position_end,
        "Expected int, float, identifier, '+', '-', '(', '[', 'if', 'for', 'while', 'func' or 'not'"
      ))

    return parseResult.success(node)

  def arithmatic_expression(self):
    return self.binary_operation(self.term, (TT_PLUS, TT_MINUS))

  def term(self):
    return self.binary_operation(self.factor, (TT_MULTIPLY, TT_DIVIDE))

  def factor(self):
    parseResult = ParseResult()
    token = self.current_token

    if token.type in (TT_PLUS, TT_MINUS):
      parseResult.register_advancement()
      self.advance()
      factor = parseResult.register(self.factor())
      if parseResult.error: return parseResult
      return parseResult.success(UnaryOpNode(token, factor))

    return self.power()

  def power(self):
    return self.binary_operation(self.call, (TT_POWER, ), self.factor)

  def call(self):
    parseResult = ParseResult()
    atomic = parseResult.register(self.atomic())
    if parseResult.error: return parseResult

    if self.current_token.type == TT_LEFT_PAREN:
      parseResult.register_advancement()
      self.advance()
      argument_nodes = []

      if self.current_token.type == TT_RIGHT_PAREN:
        parseResult.register_advancement()
        self.advance()
      else:
        argument_nodes.append(parseResult.register(self.expression()))
        if parseResult.error:
          return parseResult.failure(InvalidSyntaxError(
            self.current_token.position_start, self.current_token.position_end,
            "Expected ')', 'var', 'if', 'for', 'while', 'func', int, float, identifier, '+', '-', '(', '[' or 'not'"
          ))

        while self.current_token.type == TT_COMMA:
          parseResult.register_advancement()
          self.advance()

          argument_nodes.append(parseResult.register(self.expression()))
          if parseResult.error: return parseResult

        if self.current_token.type != TT_RIGHT_PAREN:
          return parseResult.failure(InvalidSyntaxError(
            self.current_token.position_start, self.current_token.position_end,
            f"Expected ',' or ')'"
          ))

        parseResult.register_advancement()
        self.advance()
      return parseResult.success(CallNode(atomic, argument_nodes))
    return parseResult.success(atomic)

  def atomic(self):
    parseResult = ParseResult()
    parseResult.current_token = self.current_token
    token= self.current_token

    if token.type in (TT_INT, TT_FLOAT):
        parseResult.register_advancement()
        self.advance()
        return parseResult.success(NumberNode(token))

    elif token.type == TT_STRING:
        parseResult.register_advancement()
        self.advance()
        return parseResult.success(StringNode(token))

    elif token.type == TT_IDENTIFIER:
        # parseResult.register_advancement()
        # self.advance()
        # return parseResult.success(VarAccessNode(token))
        suggestion = suggest_keyword(token.value)
        if suggestion:
            return parseResult.failure(InvalidSyntaxError(
                token.position_start, token.position_end,
                f"Unexpected identifier '{token.value}'. Did you mean '{suggestion}'?"
            ))
        parseResult.register_advancement()
        self.advance()
        return parseResult.success(VarAccessNode(token))

    elif token.type == TT_LEFT_PAREN:
        parseResult.register_advancement()
        self.advance()
        expression = parseResult.register(self.expression())
        if parseResult.error: return parseResult
        if self.current_token.type == TT_RPAREN:
            parseResult.register_advancement()
            self.advance()
            return parseResult.success(expression)
        else:
            return parseResult.failure(InvalidSyntaxError(
                self.current_token.position_start, self.current_token.position_end,
                "Expected ')'"
            ))

    elif token.type == TT_LEFT_SQUARE:
      list_expression = parseResult.register(self.list_expression())
      if parseResult.error: return parseResult
      return parseResult.success(list_expression)

    elif token.matches(TT_KEYWORD, 'if'):
      if_expression = parseResult.register(self.if_expression())
      if parseResult.error: return parseResult
      return parseResult.success(if_expression)

    elif token.matches(TT_KEYWORD, 'for'):
      for_expression = parseResult.register(self.for_expression())
      if parseResult.error: return parseResult
      return parseResult.success(for_expression)

    elif token.matches(TT_KEYWORD, 'while'):
      while_expression = parseResult.register(self.while_expression())
      if parseResult.error: return parseResult
      return parseResult.success(while_expression)

    elif token.matches(TT_KEYWORD, 'func'):
      function_definition = parseResult.register(self.function_definition())
      if parseResult.error: return parseResult
      return parseResult.success(function_definition)

    return parseResult.failure(InvalidSyntaxError(
        token.position_start, token.position_end,
        "Expected int, float, identifier, '+', '-', '(', '[', if', 'for', 'while', 'func'"
    ))

  def list_expression(self):
    parseResult = ParseResult()
    element_nodes = []
    position_start = self.current_token.position_start.copy()

    if self.current_token.type != TT_LEFT_SQUARE:
      return parseResult.failure(InvalidSyntaxError(
        self.current_token.position_start, self.current_token.position_end,
        f"Expected '['"
      ))

    parseResult.register_advancement()
    self.advance()

    if self.current_token.type == TT_RIGHT_SQUARE:
      parseResult.register_advancement()
      self.advance()
    else:
      element_nodes.append(parseResult.register(self.expression()))
      if parseResult.error:
        return parseResult.failure(InvalidSyntaxError(
          self.current_token.position_start, self.current_token.position_end,
          "Expected ']', 'var', 'if', 'for', 'while', 'func', int, float, identifier, '+', '-', '(', '[' or 'not'"
        ))

      while self.current_token.type == TT_COMMA:
        parseResult.register_advancement()
        self.advance()

        element_nodes.append(parseResult.register(self.expression()))
        if parseResult.error: return parseResult

      if self.current_token.type != TT_RIGHT_SQUARE:
        return parseResult.failure(InvalidSyntaxError(
          self.current_token.position_start, self.current_token.position_end,
          f"Expected ',' or ']'"
        ))

      parseResult.register_advancement()
      self.advance()

    return parseResult.success(ListNode(
      element_nodes,
      position_start,
      self.current_token.position_end.copy()
    ))

  def if_expression(self):
    parseResult = ParseResult()
    all_cases = parseResult.register(self.if_expr_cases('if'))
    if parseResult.error: return parseResult
    if all_cases is None:
        return parseResult.failure(InvalidSyntaxError(
            self.current_token.position_start, self.current_token.position_end,
            "Invalid 'elif' or 'else' block"
        ))
    cases, else_case = all_cases
    return parseResult.success(IfNode(cases, else_case))

  def if_expr_b(self):
    return self.if_expr_cases('elif')

  def if_expr_c(self):
    parseResult = ParseResult()
    else_case = None

    if self.current_token.matches(TT_KEYWORD, 'else'):
      parseResult.register_advancement()
      self.advance()

      if self.current_token.type == TT_COLON:
        parseResult.register_advancement()
        self.advance()

        if self.current_token.type == TT_NEWLINE:
          parseResult.register_advancement()
          self.advance()

          statements = parseResult.register(self.statements())
          if parseResult.error: return parseResult
          else_case = (statements, True)
        else:
          expression = parseResult.register(self.statement())
          if parseResult.error: return parseResult
          else_case = (expression, False)
      else:
        return parseResult.failure(InvalidSyntaxError(
          self.current_token.position_start, self.current_token.position_end,
          "Expected ':'"
        ))

    return parseResult.success(else_case)

  def if_expr_b_or_c(self):
    parseResult = ParseResult()
    cases, else_case = [], None

    if self.current_token.matches(TT_KEYWORD, 'elif'):
      all_cases = parseResult.register(self.if_expr_b())
      if parseResult.error: return parseResult
      if all_cases is None:
        return parseResult.failure(InvalidSyntaxError(
            self.current_token.position_start, self.current_token.position_end,
            "Invalid 'elif' or 'else' block"
        ))
      cases, else_case = all_cases
    else:
      else_case = parseResult.register(self.if_expr_c())
      if parseResult.error: return parseResult

    return parseResult.success((cases, else_case))

  def if_expr_cases(self, case_keyword):
    parseResult = ParseResult()
    cases = []
    else_case = None

    if not self.current_token.matches(TT_KEYWORD, case_keyword):
      return parseResult.failure(InvalidSyntaxError(
        self.current_token.position_start, self.current_token.position_end,
        f"Expected '{case_keyword}'"
      ))

    parseResult.register_advancement()
    self.advance()

    condition = parseResult.register(self.expression())
    if parseResult.error: return parseResult

    # Accept either colon or left brace
    if self.current_token.type != TT_COLON and self.current_token.type != TT_LEFT_BRACE:
      return parseResult.failure(InvalidSyntaxError(
        self.current_token.position_start, self.current_token.position_end,
        f"Expected ':' or '{{'"
      ))

    parseResult.register_advancement()
    self.advance()

    if self.current_token.type == TT_NEWLINE:
      parseResult.register_advancement()
      self.advance()

      statements = parseResult.register(self.statements())
      if parseResult.error: return parseResult
      cases.append((condition, statements, True))

      # No 'end' check here for if/elif/else
      all_cases = parseResult.register(self.if_expr_b_or_c())
      if parseResult.error: return parseResult
      if all_cases is None:
        return parseResult.failure(InvalidSyntaxError(
            self.current_token.position_start, self.current_token.position_end,
            "Invalid 'elif' or 'else' block"
        ))
      new_cases, else_case = all_cases
      cases.extend(new_cases)
    else:
      expression = parseResult.register(self.statement())
      if parseResult.error: return parseResult
      cases.append((condition, expression, False))

      all_cases = parseResult.register(self.if_expr_b_or_c())
      if parseResult.error: return parseResult
      new_cases, else_case = all_cases
      cases.extend(new_cases)

    return parseResult.success((cases, else_case))

  def for_expression(self):
    parseResult = ParseResult()

    if not self.current_token.matches(TT_KEYWORD, 'for'):
      return parseResult.failure(InvalidSyntaxError(
        self.current_token.position_start, self.current_token.position_end,
        f"Expected 'for'"
      ))

    parseResult.register_advancement()
    self.advance()

    if self.current_token.type != TT_IDENTIFIER:
      return parseResult.failure(InvalidSyntaxError(
        self.current_token.position_start, self.current_token.position_end,
        f"Expected identifier"
      ))

    variable_name = self.current_token
    parseResult.register_advancement()
    self.advance()

    if self.current_token.type != TT_EQUAL:
      return parseResult.failure(InvalidSyntaxError(
        self.current_token.position_start, self.current_token.position_end,
        f"Expected '='"
      ))

    parseResult.register_advancement()
    self.advance()

    start_value = parseResult.register(self.expression())
    if parseResult.error: return parseResult

    if not self.current_token.matches(TT_KEYWORD, 'to'):
      return parseResult.failure(InvalidSyntaxError(
        self.current_token.position_start, self.current_token.position_end,
        f"Expected 'to'"
      ))

    parseResult.register_advancement()
    self.advance()

    end_value = parseResult.register(self.expression())
    if parseResult.error: return parseResult

    step_value = None
    if self.current_token.matches(TT_KEYWORD, 'step'):
      parseResult.register_advancement()
      self.advance()

      step_value = parseResult.register(self.expression())
      if parseResult.error: return parseResult

    # Accept either colon, newline, or left brace
    if self.current_token.type == TT_COLON:
      parseResult.register_advancement()
      self.advance()

      if self.current_token.type == TT_NEWLINE:
        parseResult.register_advancement()
        self.advance()

        body = parseResult.register(self.statements())
        if parseResult.error: return parseResult

        if not self.current_token.matches(TT_KEYWORD, 'end'):
          return parseResult.failure(InvalidSyntaxError(
            self.current_token.position_start, self.current_token.position_end,
            f"Expected 'end'"
          ))

        parseResult.register_advancement()
        self.advance()

        return parseResult.success(ForNode(variable_name, start_value, end_value, step_value, body, True))

      body = parseResult.register(self.statement())
      if parseResult.error: return parseResult

      return parseResult.success(ForNode(variable_name, start_value, end_value, step_value, body, False))

    elif self.current_token.type == TT_LEFT_BRACE:
      parseResult.register_advancement()
      self.advance()

      body = parseResult.register(self.statements())
      if parseResult.error: return parseResult

      if self.current_token.type != TT_RIGHT_BRACE:
        return parseResult.failure(InvalidSyntaxError(
          self.current_token.position_start, self.current_token.position_end,
          f"Expected '}}'"
        ))

      parseResult.register_advancement()
      self.advance()

      return parseResult.success(ForNode(variable_name, start_value, end_value, step_value, body, True))

    else:
      return parseResult.failure(InvalidSyntaxError(
        self.current_token.position_start, self.current_token.position_end,
        f"Expected ':' or '{{'"
      ))

  def while_expression(self):
    res = ParseResult()

    if not self.current_token.matches(TT_KEYWORD, 'while'):
        return res.failure(InvalidSyntaxError(
            self.current_token.position_start, self.current_token.position_end,
            "Expected 'while'"
        ))

    res.register_advancement()
    self.advance()

    condition = res.register(self.expression())
    if res.error: return res

    if self.current_token.type == TT_LEFT_BRACE:
        res.register_advancement()
        self.advance()

        body = res.register(self.statements())
        if res.error: return res

        if self.current_token.type != TT_RIGHT_BRACE:
            return res.failure(InvalidSyntaxError(
                self.current_token.position_start, self.current_token.position_end,
                "Expected '}'"
            ))
        res.register_advancement()
        self.advance()

    elif self.current_token.type == TT_NEWLINE:
        res.register_advancement()
        self.advance()

        body = res.register(self.statements())
        if res.error: return res

        if not self.current_token.matches(TT_KEYWORD, 'end'):
            return res.failure(InvalidSyntaxError(
                self.current_token.position_start, self.current_token.position_end,
                "Expected 'end'"
            ))
        res.register_advancement()
        self.advance()
    else:
        return res.failure(InvalidSyntaxError(
            self.current_token.position_start, self.current_token.position_end,
            "Expected '{' or NEWLINE"
        ))

    return res.success(WhileNode(condition, body))

  def function_definition(self):
      parseResult = ParseResult()

      if not self.current_token.matches(TT_KEYWORD, 'func'):
          return parseResult.failure(InvalidSyntaxError(
              self.current_token.position_start, self.current_token.position_end,
              f"Expected 'func'"
          ))

      parseResult.register_advancement()
      self.advance()

      if self.current_token.type == TT_IDENTIFIER:
          variable_name_token = self.current_token
          parseResult.register_advancement()
          self.advance()
          if self.current_token.type != TT_LEFT_PAREN:
              return parseResult.failure(InvalidSyntaxError(
                  self.current_token.position_start, self.current_token.position_end,
                  f"Expected '('"
              ))
      else:
          variable_name_token = None
          if self.current_token.type != TT_LEFT_PAREN:
              return parseResult.failure(InvalidSyntaxError(
                  self.current_token.position_start, self.current_token.position_end,
                  f"Expected identifier or '('"
              ))

      parseResult.register_advancement()
      self.advance()
      argument_name_tokens = []
      argument_type_tokens = []

      # Check if we have parameters (non-empty parameter list)
      if self.current_token.type != TT_RIGHT_PAREN:
          # First parameter - check if it's a type
          current_token = self.current_token  # Store the current token

          # Check if this is a type identifier
          is_type = (current_token.type == TT_IDENTIFIER and
                     current_token.value in ['int', 'float', 'string', 'list', 'function'])

          if not is_type:
              # Create a direct error with the current token's position
              error = InvalidSyntaxError(
                  current_token.position_start, current_token.position_end,
                  f"Missing type for parameter '{current_token.value}'. Expected type identifier (int, float, string, list, function)"
              )
              # Return the error immediately
              return parseResult.failure(error)

          # This is a type identifier
          type_token = self.current_token
          parseResult.register_advancement()
          self.advance()

          if self.current_token.type != TT_IDENTIFIER:
              return parseResult.failure(InvalidSyntaxError(
                  self.current_token.position_start, self.current_token.position_end,
                  f"Expected parameter name"
              ))

          argument_name_token = self.current_token
          argument_type_tokens.append(type_token)
          argument_name_tokens.append(argument_name_token)
          parseResult.register_advancement()
          self.advance()

          # Additional parameters
          while self.current_token.type == TT_COMMA:
              parseResult.register_advancement()
              self.advance()

              # Store the current token position for potential error reporting
              param_pos_start = self.current_token.position_start
              param_pos_end = self.current_token.position_end
              param_value = self.current_token.value

              # Check if next token is a type
              is_type = (self.current_token.type == TT_IDENTIFIER and
                         self.current_token.value in ['int', 'float', 'string', 'list', 'function'])

              if not is_type:
                  # Error: Parameter must have a type - point to the parameter
                  return parseResult.failure(InvalidSyntaxError(
                      param_pos_start, param_pos_end,
                      f"Missing type for parameter '{param_value}'. Expected type identifier (int, float, string, list, function)"
                  ))

              # This is a type identifier
              type_token = self.current_token
              parseResult.register_advancement()
              self.advance()

              if self.current_token.type != TT_IDENTIFIER:
                  return parseResult.failure(InvalidSyntaxError(
                      self.current_token.position_start, self.current_token.position_end,
                      f"Expected parameter name"
                  ))

              argument_name_token = self.current_token
              argument_type_tokens.append(type_token)
              argument_name_tokens.append(argument_name_token)
              parseResult.register_advancement()
              self.advance()

      if self.current_token.type != TT_RIGHT_PAREN:
          return parseResult.failure(InvalidSyntaxError(
              self.current_token.position_start, self.current_token.position_end,
              f"Expected ',' or ')'"
          ))

      parseResult.register_advancement()
      self.advance()

      # Handle arrow-style single-expression function
      if self.current_token.type == TT_ARROW:
          parseResult.register_advancement()
          self.advance()

          body = parseResult.register(self.expression())
          if parseResult.error:
              return parseResult.failure(InvalidSyntaxError(
                  parseResult.error.position_start, parseResult.error.position_end, parseResult.error.details
              ))

          return parseResult.success(FuncDefNode(
              variable_name_token,
              argument_name_tokens,
              body,
              True,
              argument_type_tokens
          ))

      # MULTI-STATEMENT FUNCTION STARTS HERE
      # Accept either NEWLINE or LEFT_BRACE after parameter list
      if self.current_token.type == TT_NEWLINE:
          parseResult.register_advancement()
          self.advance()

          body = parseResult.register(self.statements())
          if parseResult.error:
              return parseResult.failure(InvalidSyntaxError(
                  parseResult.error.position_start, parseResult.error.position_end, parseResult.error.details
              ))

          if not self.current_token.matches(TT_KEYWORD, 'end'):
              return parseResult.failure(InvalidSyntaxError(
                  self.current_token.position_start, self.current_token.position_end,
                  f"Expected 'end'"
              ))

          parseResult.register_advancement()
          self.advance()

          return parseResult.success(FuncDefNode(
              variable_name_token,
              argument_name_tokens,
              body,
              False,
              argument_type_tokens
          ))

      elif self.current_token.type == TT_LEFT_BRACE:
          parseResult.register_advancement()
          self.advance()

          body = parseResult.register(self.statements())
          if parseResult.error:
              return parseResult.failure(InvalidSyntaxError(
                  parseResult.error.position_start, parseResult.error.position_end, parseResult.error.details
              ))

          if self.current_token.type != TT_RIGHT_BRACE:
              return parseResult.failure(InvalidSyntaxError(
                  self.current_token.position_start, self.current_token.position_end,
                  f"Expected '}}'"
              ))

          parseResult.register_advancement()
          self.advance()

          return parseResult.success(FuncDefNode(
              variable_name_token,
              argument_name_tokens,
              body,
              False,
              argument_type_tokens
          ))

      return parseResult.failure(InvalidSyntaxError(
          self.current_token.position_start, self.current_token.position_end,
          f"Expected '=>', '{{', or NEWLINE"
      ))

  ###################################

  def binary_operation(self, func_a, operations, func_b=None):
    if func_b == None:
      func_b = func_a

    parseResult = ParseResult()
    left = parseResult.register(func_a())
    if parseResult.error: return parseResult

    while self.current_token.type in operations or (self.current_token.type, self.current_token.value) in operations:
      operation_token = self.current_token
      parseResult.register_advancement()
      self.advance()
      right = parseResult.register(func_b())
      if parseResult.error: return parseResult
      left = BinaryOperationNode(left, operation_token, right)

    return parseResult.success(left)
