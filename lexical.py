from rply import LexerGenerator


class Lexer():
    def __init__(self):
        self.lexer = LexerGenerator()

# reserved = {
#     'if' : 'IF',
#     'then' : 'THEN',
#     'else' : 'ELSE',
#     'while' : 'WHILE',
#     ...
#  }

#  tokens = ['LPAREN','RPAREN',...,'ID'] + list(reserved.values())
    def _add_tokens(self):
        # comentarios
        self.lexer.ignore(r"//.*?//")
        # Print
        self.lexer.add('PRINT', r'imprimir')
        # Parenthesis and Braces
        self.lexer.add('OPEN_PAREN', r'\(')
        self.lexer.add('CLOSE_PAREN', r'\)')
        self.lexer.add('OPEN_BRACES', r'\{')
        self.lexer.add('CLOSE_BRACES', r'\}')
        # Semi Colon
        self.lexer.add('SEMI_COLON', r'\;')
        self.lexer.add('COMMA', r'\,')
        # function
        self.lexer.add('FUNCTION', r'funcion')
        # type
        self.lexer.add('TYPE', 'int')
        self.lexer.add('TYPE', 'bool')
       # Operators
        # self.lexer.add('PLUS_ONE', r'\++')`
        self.lexer.add('EQUAL_EQUAL', r'lo_mismo')
        self.lexer.add('PLUS_EQUAL', r'\+\=')
        self.lexer.add('MINUS_EQUAL', r'\-\=')
        # If-else
        self.lexer.add("ELSE", r'seno')
        self.lexer.add("IF", r'se')

        self.lexer.add('AND', r'y')
        self.lexer.add('OR', r'o')
        self.lexer.add('EQUAL', r'\=')
        self.lexer.add('SUM', r'\+')
        self.lexer.add('NOT', r'queno')
        self.lexer.add('SUB', r'\-')

        self.lexer.add('MUL', r'\*')
        self.lexer.add('DIV', r'/')
        self.lexer.add('REST', r'\%')
        # Logical Operators
        self.lexer.add("GREATER", r'mas_grande')
        self.lexer.add("LESS", r'menor')
        # Types
        self.lexer.add('INT', r'int')
        self.lexer.add('DOUBLE', r'doble')
        # Statement
        self.lexer.add("WHILE", r'todavia')
        self.lexer.add("FOR", r'por')

        # Identifier
        # IDENTIFIER = LETTER, { LETTER | DIGIT | "_" } ;
        self.lexer.add("IDENTIFIER", r'[a-zA-Z]*([a-zA-Z]|/d+|_)')
        # Number
        self.lexer.add('NUMBER', r'\d+')

        # Ignore spaces
        self.lexer.ignore('\s+')

    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()


# TYPE = {
#       char
#     | short
#     | int
#     | long
#     | float
#     | double
#     | signed
#     | unsigned
#     | STRUCT_OR_UNION_SPECIFIER
#     | ENUM-SPECIFIER
#     | TYPEDEF-NAME
# };


# LOGICAL =
#              *=
#             | /=
#             | %=
#             | <=
#             | >=
