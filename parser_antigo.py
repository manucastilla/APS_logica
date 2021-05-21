from rply import ParserGenerator
from ast import(Number, Sum, Sub, Print, Mul, Div, Rest,
                If, Or, And, Less, Greater, MinusEqual, PlusEqual, PlusOne,
                Block, Setter, Getter, Equal_Equal
                )


class Parser():
    def __init__(self):
        self.pg = ParserGenerator(
            # A list of all token names accepted by the parser.
            ['NUMBER', 'PRINT', 'OPEN_PAREN', 'CLOSE_PAREN',
             'SEMI_COLON', 'SUM', 'SUB', 'MUL', 'DIV', 'REST',
             'OPEN_BRACES', 'CLOSE_BRACES',
             'OR', 'LESS', 'GREATER', 'AND', 'MINUS_EQUAL', 'PLUS_EQUAL',
             'PLUS_ONE', 'EQUAL', 'IDENTIFIER', 'EQUAL_EQUAL']

            # 'IF', 'ELSE',

            #  precedence=[
            #      ('left', [ 'SUM'])
            #  ]
        )

    def parse(self):
        #################### BLOCK ####################
        #                               p[0]       p[1]      p[2]
        @self.pg.production('begin : OPEN_BRACES block CLOSE_BRACES ')
        def begin(p):
            return p[1]

        @self.pg.production('block : command')
        @self.pg.production('block : block command')
        # arrumar porque ta igual do ma
        def block(p):
            if len(p) == 1:
                return Block([p[0]])

            p[0].children += [p[1]]
            return p[0]

        #################### COMMAND ####################
        @self.pg.production('command : SEMI_COLON')
        @self.pg.production('command : assignment SEMI_COLON')
        @self.pg.production('command : println')
        def command(p):
            return p[0]

        #################### PRINT ####################

        @self.pg.production('println : PRINT OPEN_PAREN expression CLOSE_PAREN SEMI_COLON')
        @self.pg.production('println : PRINT OPEN_PAREN variable CLOSE_PAREN SEMI_COLON')
        # @self.pg.production('println : PRINT OPEN_PAREN variable expression CLOSE_PAREN SEMI_COLON')
        def println(p):
            return Print(p[2])

        #################### ASSIGNMENT ####################

        @self.pg.production('assignment : IDENTIFIER EQUAL expression')
        def assignment(p):
            return Setter(p[0].getstr(), p[2])

        @self.pg.production('variable : IDENTIFIER')
        def variable(p):
            return Getter(p[0].getstr())

        #################### IF/ELSE ####################
        @self.pg.production('if : IF OPEN_PAREN expression CLOSE_PAREN OPEN_BRACES expression CLOSE_BRACES')
        def if_func(p):
            left = p[0]
            right = p[0]
            return If(left, right)
        # @self.pg.production('''for : por OPEN_PAREN IDENTIFIER EQUAL NUMBER
        # SEMI_COLON IDENTIFIER LESS CLOSE_PAREN OPEN_BRACES
        # ''')

        #################### TERM / EXPRESSION ####################
        # variable and number
        @self.pg.production('expression : variable   SUB         expression')
        @self.pg.production('expression : variable   SUM         expression')
        @self.pg.production('expression : variable   MUL         expression')
        @self.pg.production('expression : variable   DIV         expression')
        @self.pg.production('expression : variable   REST        expression')
        @self.pg.production('expression : variable   OR          expression')
        @self.pg.production('expression : variable   AND         expression')
        @self.pg.production('expression : variable   GREATER     expression')
        @self.pg.production('expression : variable   LESS        expression')
        @self.pg.production('expression : variable   PLUS_EQUAL  expression')
        @self.pg.production('expression : variable   MINUS_EQUAL expression')
        @self.pg.production('expression : variable   EQUAL_EQUAL expression')
        # variable and variable
        @self.pg.production('expression : variable   SUM         variable')
        @self.pg.production('expression : variable   SUB         variable')
        @self.pg.production('expression : variable   MUL         variable')
        @self.pg.production('expression : variable   DIV         variable')
        @self.pg.production('expression : variable   REST        variable')
        @self.pg.production('expression : variable   OR          variable')
        @self.pg.production('expression : variable   AND         variable')
        @self.pg.production('expression : variable   GREATER     variable')
        @self.pg.production('expression : variable   LESS        variable')
        @self.pg.production('expression : variable   PLUS_EQUAL  variable')
        @self.pg.production('expression : variable   MINUS_EQUAL variable')
        @self.pg.production('expression : variable   EQUAL_EQUAL variable')
        # number and number
        @self.pg.production('expression : expression SUM  expression')
        @self.pg.production('expression : expression SUB  expression')
        @self.pg.production('expression : expression MUL  expression')
        @self.pg.production('expression : expression DIV  expression')
        @self.pg.production('expression : expression REST expression')
        # logOp
        @self.pg.production('expression : expression OR          expression')
        @self.pg.production('expression : expression AND         expression')
        @self.pg.production('expression : expression GREATER     expression')
        @self.pg.production('expression : expression LESS        expression')
        @self.pg.production('expression : expression PLUS_EQUAL  expression')
        @self.pg.production('expression : expression MINUS_EQUAL expression')
        @self.pg.production('expression : expression EQUAL_EQUAL expression')
        # @self.pg.production('expression : number PLUS_ONE')
        def expression(p):
            if len(p) > 2:
                right = p[2]

            left = p[0]
            operator = p[1]
            if operator.gettokentype() == 'SUM':
                return Sum(left, right)
            elif operator.gettokentype() == 'SUB':
                return Sub(left, right)
            elif operator.gettokentype() == 'MUL':
                return Mul(left, right)
            elif operator.gettokentype() == 'DIV':
                return Div(left, right)
            elif operator.gettokentype() == 'REST':
                return Rest(left, right)
            elif operator.gettokentype() == 'OR':
                return Or(left, right)
            elif operator.gettokentype() == 'AND':
                return And(left, right)
            elif operator.gettokentype() == 'LESS':
                return Less(left, right)
            elif operator.gettokentype() == 'GREATER':
                return Greater(left, right)
            # elif operator.gettokentype() == 'PLUS_ONE':
            #     return PlusOne(left, None)
            elif operator.gettokentype() == 'MINUS_EQUAL':
                return PlusEqual(left, right)
            elif operator.gettokentype() == 'MINUS_EQUAL':
                return MinusEqual(left, right)
            elif operator.gettokentype() == 'EQUAL_EQUAL':
                return Equal_Equal(left, right)

        @self.pg.production('expression : NUMBER')
        def number(p):
            return Number(p[0].value)

        @self.pg.error
        def error_handle(token):
            raise ValueError(token)

    def get_parser(self):
        return self.pg.build()
