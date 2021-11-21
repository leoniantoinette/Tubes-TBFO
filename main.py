import cyk_parser as cyk
import lexer as lex
import sys

def compile(input_file):
  texts = lex.lexer(input_file)
  if (texts != -1):
    print(texts)
    parser = cyk.Parser("grammar.txt", texts)
    parser.__call__(texts, parse=True)
    parser.parse()
    parser.print_tree()
    return

if __name__ == '__main__':
  filename = sys.argv[1]
  compile(filename)