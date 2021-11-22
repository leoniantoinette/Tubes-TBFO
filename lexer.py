import re

class Token(object):
    def __init__(self, type, val, pos):
        self.type = type
        self.val = val
        self.pos = pos

class Lexer(object):
    def __init__(self, rules):
        idx = 1
        regex_parts = []
        self.group_type = {}

        for regex, type in rules:
            groupname = 'GROUP%s' % idx
            regex_parts.append('(?P<%s>%s)' % (groupname, regex))
            self.group_type[groupname] = type
            idx += 1

        self.regex = re.compile('|'.join(regex_parts))

    def input(self, buf):
        self.buf = buf
        self.pos = 0

    def token(self):
        if self.pos >= len(self.buf):
            return None
        else:
            try:
                m = self.regex.match(self.buf, self.pos)
                if m:
                    groupname = m.lastgroup
                    tok_type = self.group_type[groupname]
                    tok = Token(tok_type, m.group(groupname), self.pos)
                    self.pos = m.end()
                    return tok
            except:
                print("Syntax error!")

    def tokens(self):
        while 1:
            tok = self.token()
            if tok is None: 
                break
            yield tok

def lexer(inputfile):
    rules = [
        (r'\#.*', 'COMMENT'),
        (r'\"\"\"', 'COMMENT2'),
        (r'\'\'\'', 'COMMENT3'),
        # (r'\n', 'NEWLINE'),
        # (r'\s', 'WHITESPACE'),
        (r'from\s', 'FROM'),
        (r'import\s', 'IMPORT'),
        (r'as\s', 'AS'),
        (r'class\s', 'CLASS'),
        (r'def\s', 'DEF'),
        (r'return', 'RETURN'),
        (r'pass', 'PASS'),
        (r'raise\s', 'RAISE'),
        (r'continue', 'CONTINUE'),
        (r'break', 'BREAK'),
        (r'if\s', 'IF'),
        (r'if\(', 'IF_LPAR'),
        (r'elif\s', 'ELIF'),
        (r'elif\(', 'ELIF_LPAR'),
        (r'else', 'ELSE'),
        (r'for\s', 'FOR'),
        (r'in\s', 'IN'),
        (r'range\s', 'RANGE'),
        (r'range\(', 'RANGE_LPAR'),
        (r'while\s', 'WHILE'),
        (r'while\(', 'WHILE_LPAR'),
        (r'None', 'NONE'),
        (r'True', 'TRUE'),
        (r'False', 'FALSE'),
        (r'not', 'NOT'),
        (r'\sis\s', 'IS'),
        (r'with\s', 'WITH'),
        (r'print', 'PRINT'),
        (r'\sand\s', 'AND'),
        (r'\sor\s', 'OR'),
        (r'BaseException', 'BASEEXCPT'),
        (r'SystemExit', 'SYSEXIT'),
        (r'KeyboardInterrupt', 'KEYBINTER'),
        (r'GeneratorExit', 'GENEXIT'),
        (r'Exception', 'EXCPTERR'),
        (r'StopIteration', 'STOPITERATE'),
        (r'StopAsyncIteration', 'STOPASYNCITER'),
        (r'ArithmeticError', 'ARITHERR'),
        (r'FloatingPointError', 'FLOATPOINTERR'),
        (r'OverflowError', 'OVERFLOWERR'),
        (r'ZeroDivisionError', 'ZERODIVERR'),
        (r'AssertionError', 'ASSERTERR'),
        (r'AttributeError', 'ATTRERR'),
        (r'BufferError', 'BUFFERERR'),
        (r'EOFError', 'EOFERR'),
        (r'ImportError', 'IMPORTERR'),
        (r'ModuleNotFoundError', 'MODULEERR'),
        (r'LookupError', 'LOOKUPERR'),
        (r'IndexError', 'IDXERR'),
        (r'KeyError', 'KEYERR'),
        (r'MemoryError', 'MEMERR'),
        (r'NameError', 'NAMEERR'),
        (r'UnboundLocalError', 'UNBOUNDLCLERR'),
        (r'OSError', 'OSERR'),
        (r'BlockingIOError', 'BLOCKIOERR'),
        (r'ChildProcessError', 'CHILDERR'),
        (r'ConnectionError', 'CONNECTERR'),
        (r'BrokenPipeError', 'BROKENPIPEERR'),
        (r'ConnectionAbortedError', 'CONNECTABORTERR'),
        (r'ConnectionRefusedError', 'CONNECTREFERR'),
        (r'ConnectionResetError', 'CONNECTRSTERR'),
        (r'FileExistsError', 'FILEEXTERR'),
        (r'FileNotFoundError', 'FILENOTFOUNDERR'),
        (r'InterruptedError', 'INTERRUPTERR'),
        (r'IsADirectoryError', 'ISADIRERR'),
        (r'NotADirectiorError', 'NOTADIRERR'),
        (r'PermissionError', 'PERMISSIONERR'),
        (r'ProcessLookupError', 'PROCESSLOOKUPERR'),
        (r'TimeoutError', 'TIMEOUTERR'),
        (r'ReferenceError', 'REFERR'),
        (r'RuntimeError', 'RUNTIMEERR'),
        (r'NotImplementedError', 'NOTIMPLMTERR'),
        (r'RecursionError', 'RECURSIONERR'),
        (r'SyntaxError', 'SYNTAXERR'),
        (r'IndentationError', 'INDENTERR'),
        (r'TabError', 'TABERR'),
        (r'SystemError', 'SYSERR'),
        (r'TypeError', 'TYPEERR'),
        (r'ValueError', 'VALUEERR'),
        (r'UnicodeError', 'UNICODEERR'),
        (r'UnicodeDecodeError', 'UNICODEDCDERR'),
        (r'UnicodeTranslateError', 'UNICODETRANSERR'),
        (r'Warning', 'WARNING'),
        (r'DeprecationWarning', 'DEPRECATIONWARN'),
        (r'PendingDeprecationWarning', 'PENDDEPRECWARN'),
        (r'RuntimeWarning', 'RUNTIMEWARN'),
        (r'SyntaxWarning', 'SYNTAXWARN'),
        (r'UserWarning', 'USERWARN'),
        (r'FutureWarning', 'FUTUREWARN'),
        (r'ImportWarning', 'IMPORTWARN'),
        (r'UnicodeWarning', 'UNICODEWARN'),
        (r'BytesWarning', 'BYTESWARN'),
        (r'EncodingWarning', 'ENCODEWARN'),
        (r'ResourceWarning', 'RESOURCEWARN'),
        # (r'str', 'STR'),
        # (r'int', 'INT'),
        # (r'float', 'FLOAT'),
        # (r'double', 'DOUBLE'),
        # (r'bool', 'BOOL'),
        # (r'input', 'INPUT'),
        ('\".*\"', 'STRING'),
        ('\'.*\'', 'STRING'),
        (r'[\da-zA-Z_]*[a-zA-Z_]+[\da-zA-Z_]*','VAR'),
        (r'\.', 'WITH_METHOD'),
        (r'\n', 'NEWLINE'),
        (r'\s', 'WHITESPACE'),
        (r':', 'COLON'),
        (r';', 'SEMICOLON'),
        (r'\d+','INTEGER'),
        (r'\d+.+\d','DECIMAL'),
        (r'<<', 'LEFTSHIFT'),
        (r'>>', 'RIGHTSHIFT'),
        (r'//', 'DOUBLESLASH'),
        (r'\+=', 'PLUSEQUAL'),
        (r'-=', 'MINEQUAL'),
        (r'\*=', 'STAREQUAL'),
        (r'/=', 'SLASHEQUAL'),
        (r'%=', 'PERCENTEQUAL'),
        (r'//=', 'DSLASHEQUAL'),
        (r'\*\*=', 'POWEREQUAL'),
        (r'&=', 'ANDEQUAL'),
        (r'\|=', 'OREQUAL'),
        (r'^=', 'XOREQUAL'),
        (r'>>=', 'RSHIFTEQUAL'),
        (r'<<=', 'LSHIFTEQUAL'),
        (r'==','EQEQUAL'),
        (r'!=', 'NOTEQUAL'),
        (r'>', 'GREATER'),
        (r'<', 'LESS'),
        (r'>=', 'GREATEREQUAL'),
        (r'<=', 'LESSEQUAL'),
        (r'=','EQUAL'),
        (r'\+','PLUS'),
        (r'\-','MINUS'),
        (r'\*\*','POWER'),
        (r'\*','MULTIPLY'),
        (r'\/','SLASH'),
        (r'\%', 'PERCENT'),
        (r'&', 'BITAND'),
        (r'\|', 'BITOR'),
        (r'~', 'BITNOT'),
        (r'^', 'BITXOR'),
        (r'\[', 'LSQB'),
        (r'\]', 'RSQB'),
        (r'\(','LPAR'),
        (r'\)','RPAR'),
        (r',', 'COMMA'),
    ]

    file = open(inputfile)
    contents = file.read()
    file.close()

    lx = Lexer(rules)
    lx.input(contents)

    arr_res = []
    arr_var = []
    for tok in lx.tokens():
        if (tok.type != 'WHITESPACE' and tok.type != 'NEWLINE' and tok.type != 'COMMENT'):
            arr_res.append(tok.type)
            if (tok.type == 'VAR'):
                arr_var.append(tok.val)

    # testing
    # print(arr_res)
    # print(arr_var)

    # delete comment
    i = 0
    check = True
    while (i < len(arr_res) and check):
        if (arr_res[i] == 'COMMENT2'):
            j = i + 1
            while (arr_res[j] != 'COMMENT2' and j < len(arr_res)-1):
                del arr_res[j]
            # arr_res[j] == 'COMMENT2' atau j == len(arr_res)-1
            if (arr_res[j] == 'COMMENT2'):
                del arr_res[j]
                del arr_res[i]
            else:
                check = False
        elif (arr_res[i] == 'COMMENT3'):
            j = i + 1
            while (arr_res[j] != 'COMMENT3' and j < len(arr_res)-1):
                del arr_res[j]
            # arr_res[j] == 'COMMENT3' atau j == len(arr_res)-1
            if (arr_res[j] == 'COMMENT3'):
                del arr_res[j]
                del arr_res[i]
            else:
                check = False
        else:
            i += 1

    if check:
        return (' '.join(arr_res)), arr_var
    else:
        print("Syntax error!")
        return -1, -1