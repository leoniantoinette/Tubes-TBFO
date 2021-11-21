import cyk
import lexer as lex
from dfa import checkVar
import sys

def compile(input_file):
  texts, variables = lex.lexer(input_file)
  if (texts != -1):
    # evaluate variables using DFA
    for var in variables:
      isValid = checkVar(var)
      if not(isValid):
        print("Syntax error!")
        break
    
    # evaluate syntax using CFG
    if isValid:
      parser = cyk.Parser("grammar.txt", texts)
      parser.__call__(texts)
      parser.print_tree()
    return

if __name__ == '__main__':
  filename = sys.argv[1]
  compile(filename)