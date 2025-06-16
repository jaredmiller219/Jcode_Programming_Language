#######################################
# RUNTIME RESULT
#######################################

class RuntimeResult:
  def __init__(self):
    self.reset()

  def reset(self):
    self.value = None
    self.error = None
    self.function_return_value = None
    self.loop_should_continue = False
    self.loop_should_break = False

  def register(self, result):
    self.error = result.error
    self.function_return_value = result.function_return_value
    self.loop_should_continue = result.loop_should_continue
    self.loop_should_break = result.loop_should_break
    return result.value

  def success(self, value):
    self.reset()
    self.value = value
    return self

  def success_return(self, value):
    self.reset()
    self.function_return_value = value
    return self

  def success_continue(self):
    self.reset()
    self.loop_should_continue = True
    return self

  def success_break(self):
    self.reset()
    self.loop_should_break = True
    return self

  def failure(self, error):
    self.reset()
    self.error = error
    return self

  def should_return(self):
    # Note: this will allow you to continue and break outside the current function
    return (
      self.error or
      self.function_return_value or
      self.loop_should_continue or
      self.loop_should_break
    )
