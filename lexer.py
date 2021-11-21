import re

class Token(object):
    """ A simple Token structure.
        Contains the token type, value and position.
    """
    def __init__(self, type, val, pos):
        self.type = type
        self.val = val
        self.pos = pos

    def __str__(self):
        return '%s(%s) at %s' % (self.type, self.val, self.pos)


class LexerError(Exception):
    """ Lexer error exception.
        pos:
            Position in the input line where the error occurred.
    """
    def __init__(self, pos):
        self.pos = pos


class Lexer(object):
    """ A simple regex-based lexer/tokenizer.
        See below for an example of usage.
    """
    def __init__(self, rules, skip_whitespace=True):
        """ Create a lexer.
            rules:
                A list of rules. Each rule is a `regex, type`
                pair, where `regex` is the regular expression used
                to recognize the token and `type` is the type
                of the token to return when it's recognized.
            skip_whitespace:
                If True, whitespace (\s+) will be skipped and not
                reported by the lexer. Otherwise, you have to
                specify your rules for whitespace, or it will be
                flagged as an error.
        """
        # All the regexes are concatenated into a single one
        # with named groups. Since the group names must be valid
        # Python identifiers, but the token types used by the
        # user are arbitrary strings, we auto-generate the group
        # names and map them to token types.
        #
        idx = 1
        regex_parts = []
        self.group_type = {}

        for regex, type in rules:
            groupname = 'GROUP%s' % idx
            regex_parts.append('(?P<%s>%s)' % (groupname, regex))
            self.group_type[groupname] = type
            idx += 1

        self.regex = re.compile('|'.join(regex_parts))
        self.skip_whitespace = skip_whitespace
        self.re_ws_skip = re.compile('\S')

    def input(self, buf):
        """ Initialize the lexer with a buffer as input.
        """
        self.buf = buf
        self.pos = 0

    def token(self):
        """ Return the next token (a Token object) found in the
            input buffer. None is returned if the end of the
            buffer was reached.
            In case of a lexing error (the current chunk of the
            buffer matches no rule), a LexerError is raised with
            the position of the error.
        """
        if self.pos >= len(self.buf):
            return None
        else:
            if self.skip_whitespace:
                m = self.re_ws_skip.search(self.buf, self.pos)

                if m:
                    self.pos = m.start()
                else:
                    return None

            m = self.regex.match(self.buf, self.pos)
            if m:
                groupname = m.lastgroup
                tok_type = self.group_type[groupname]
                # tok = Token(tok_type, m.group(groupname), self.pos)
                # tok = tok_type
                self.pos = m.end()
                return tok_type

            # if we're here, no rule matched
            raise LexerError(self.pos)

    def tokens(self):
        """ Returns an iterator to the tokens found in the buffer.
        """
        while 1:
            tok = self.token()
            if tok is None: break
            yield tok

def lexer(inputfile):
    rules = [
        (r'\#.*', 'COMMENT'),
        (r'\"\"\"', 'COMMENT2'),
        (r'\'\'\'', 'COMMENT3'),
        (r'\n', 'NEWLINE'),
        (r'\s', 'WHITESPACE'),
        (r'from\s', 'FROM'),
        (r'import\s', 'IMPORT'),
        (r'as\s', 'AS'),
        (r'class\s', 'CLASS'),
        (r'def\s', 'DEF'),
        (r'return', 'RETURN'),
        (r'pass', 'PASS'),
        (r'raise\s', 'RAISE'),
        (r'continue\s', 'CONTINUE'),
        (r'break\s', 'BREAK'),
        (r'if\s', ' IF'),
        (r'if\(', ' IF_LPAR'),
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
        (r'or', 'OR'),
        (r'and', 'AND'),
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
        (r'\.', 'WITH_METHOD'),
        (r':', 'COLON'),
        (r';', 'SEMICOLON'),
        (r'\d+','INTEGER'),
        (r'\d+.+\d','DECIMAL'),
        # (r'[a-zA-Z_]+[\da-zA-Z_0-9]*','VAR'),
        (r'[\da-zA-Z_0-9]+','VAR'),
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
        (r'\sand\s', 'AND'),
        (r'\sor\s', 'OR'),
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

    lx = Lexer(rules, skip_whitespace=False)
    lx.input(contents)

    arr_res = []
    try:
        for tok in lx.tokens():
            if (tok != 'WHITESPACE' and tok != 'NEWLINE' and tok != 'COMMENT'):
                arr_res.append(tok)
        # print(arr_res)    # testing
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
            return ' '.join(arr_res)
        else:
            print("Syntax error!")
            return -1

    except LexerError as err:
        print('LexerError at position %s' % err.pos)
        return -1