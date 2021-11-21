class DFA:
  def __init__(self):
    self.handlers = {}
    self.startState = None
    self.endStates = []
  
  def addState(self, name, handler, isEndState=False, isStartState=False):
    self.handlers[name] = handler
    if isEndState:
      self.endStates.append(name)
    if isStartState:
      self.startState = name
  
  def check(self, strings):
    handler = self.handlers[self.startState]
    while len(strings) > 0:
      (newState, strings) = handler(strings)
      if (newState == 'errorState'):
        break
      else:
        handler = self.handlers[newState]
    return (newState in self.endStates)

def start_transitions(strings):
  if (len(strings) > 1):
    char = strings[0]
    strings = strings[1:]
  else:
    char = strings[0]
    strings = ""
  # check
  if (char.isalpha() or char == '_'):
    newState = "finalState"
  else:
    newState = "errorState"
  return (newState, strings)

def final_transitions(strings):
  if (len(strings) > 1):
    char = strings[0]
    strings = strings[1:]
  else:
    char = strings[0]
    strings = ""
  # check
  if (char.isalpha() or char.isdigit() or char == '_'):
    newState = "finalState"
  else:
    newState = "errorState"
  return (newState, strings)

def error_transitions(strings):
  if (len(strings) > 1):
    strings = strings[1:]
  else:
    strings = ""
  newState = "errorState"
  return (newState, strings)  

def checkVar(variable):
  variableChecker = DFA()
  variableChecker.addState("start", start_transitions, isStartState=True)
  variableChecker.addState("finalState", final_transitions, isEndState=True)
  variableChecker.addState("errorState", error_transitions)
  return variableChecker.check(variable)