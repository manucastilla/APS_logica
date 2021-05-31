from rply import ParserGenerator
from ast import(Number, Sum, Sub, Print, Mul, Div, Rest,
                If, Or, And, Less, Greater, MinusEqual, PlusEqual, PlusOne,
                Block, Setter, Getter, Equal_Equal, UnOp, Identifier, While
                )


class Parser():
    def __init__(self):
        self.pg = ParserGenerator(
            # A list of all token names accepted by the parser.
            ['NUMBER', 'PRINT', 'OPEN_PAREN', 'CLOSE_PAREN',
             'SEMI_COLON', 'OPEN_BRACES', 'CLOSE_BRACES',
             'EQUAL', 'IDENTIFIER', 'LESS', 'GREATER',
             'SUM', 'SUB', 'NOT', 'MUL', 'DIV', 'EQUAL_EQUAL',
             'AND', 'OR', 'IF', 'ELSE', 'WHILE', 'TYPE', 'FUNCTION']

            # , 'COMMA'
            #  , , 'REST', 'SUB_EQUAL', 'PLUS_EQUAL',
            # 'PLUS_ONE'

            #  precedence=[
            #      ('left', [ 'SUM'])
            #  ]
        )

    def parse(self):
        #################### BLOCK ####################
        #                               p[0]       p[1]      p[2]
        @self.pg.production('start : def_function ')
        def begin(p):
            return p[0]

        @self.pg.production('def_function : FUNCTION IDENTIFIER OPEN_PAREN CLOSE_PAREN begin')
        # @self.pg.production('def_function : FUNCTION IDENTIFIER OPEN_PAREN params CLOSE_PAREN begin')
        def def_function(p):
            if len(p) == 5:
                # setter
                return p[4]
            else:
                return p[5]

        # @self.pg.production('params : IDENTIFIER')
        # @self.pg.production('params : IDENTIFIER COMMA params')
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
        @self.pg.production('command : if_cond')
        @self.pg.production('command : while_cond')
        @self.pg.production('command : definition SEMI_COLON')
        # @self.pg.production('command : while')
        def command(p):
            return p[0]

        #################### ASSIGNMENT and DEFINITION ####################
        @self.pg.production('assignment : IDENTIFIER EQUAL parseOREXPR')
        def assignment(p):
            return Setter(p[0].getstr(), p[2], None)

        @self.pg.production('definition : TYPE IDENTIFIER')
        def definition(p):
            return Setter(p[1].getstr(), None, p[0].getstr())
        #################### PRINT ####################

        @self.pg.production('println : PRINT OPEN_PAREN parseOREXPR CLOSE_PAREN SEMI_COLON')
        # @self.pg.production('println : PRINT OPEN_PAREN variable expression CLOSE_PAREN SEMI_COLON')
        def println(p):
            return Print(p[2])

        #################### WHILE AND FOR ####################
        #                                  p[0] p[1]        p[2]       p[3]         p[4]
        @self.pg.production('while_cond : WHILE OPEN_PAREN parseOREXPR CLOSE_PAREN begin')
        def while_cond(p):
            condition = p[2]
            todo = p[4]
            return While([condition, todo])

        #################### IF ####################
        #                             p[0] p[1]        p[2]       p[3]         p[4]       p[5]  p[6]
        @self.pg.production('if_cond : IF OPEN_PAREN parseOREXPR CLOSE_PAREN begin')
        @self.pg.production('if_cond : IF OPEN_PAREN parseOREXPR CLOSE_PAREN begin ELSE begin')
        def if_cond(p):
            # print(p[0].gettokentype())
            if p[0].gettokentype() == "IF":
                if len(p) == 5:
                    condition = p[2]
                    todo = p[4]
                    return If([condition, todo, None])
                else:
                    return If([p[2], p[4], p[6]])

        #################### parseOREXPR ####################

        @self.pg.production('parseOREXPR : parseANDEXPR')
        @self.pg.production('parseOREXPR : parseANDEXPR OR parseOREXPR')
        def parseOREXPR(p):
            if len(p) == 1:
                return p[0]
            else:
                right = p[2]
                left = p[0]
                operator = p[1]
                if operator.gettokentype() == 'OR':
                    return Or(left, right)

        #################### parseANDEXPR ####################
        @self.pg.production('parseANDEXPR : parseEQEXPR')
        @self.pg.production('parseANDEXPR : parseEQEXPR AND parseANDEXPR')
        def parseANDEXPR(p):
            if len(p) == 1:
                return p[0]
            else:
                right = p[2]
                left = p[0]
                operator = p[1]
                if operator.gettokentype() == 'AND':
                    return Equal_Equal(left, right)

        #################### parseEQEXPR ####################
        @self.pg.production('parseEQEXPR : parseRELEXPR')
        @self.pg.production('parseEQEXPR : parseRELEXPR EQUAL_EQUAL parseEQEXPR')
        def parseEQEXPR(p):
            if len(p) == 1:
                return p[0]
            else:
                right = p[2]
                left = p[0]
                operator = p[1]
                if operator.gettokentype() == 'EQUAL_EQUAL':
                    return Equal_Equal(left, right)

        #################### parseRELEXPR ####################
        @self.pg.production('parseRELEXPR : expression')
        @self.pg.production('parseRELEXPR : expression LESS parseRELEXPR')
        @self.pg.production('parseRELEXPR : expression GREATER parseRELEXPR')
        def parseRELEXPR(p):
            if len(p) == 1:
                return p[0]
            else:
                right = p[2]
                left = p[0]
                operator = p[1]
                if operator.gettokentype() == 'LESS':
                    return Less(left, right)
                elif operator.gettokentype() == 'GREATER':
                    return Greater(left, right)

        #################### EXPRESSION ####################
        @self.pg.production('expression : term')
        @self.pg.production('expression : term SUM expression')
        @self.pg.production('expression : term SUB expression')
        def expression(p):
            if len(p) == 1:
                return p[0]
            else:
                right = p[2]
                left = p[0]
                operator = p[1]
                if operator.gettokentype() == 'SUM':
                    return Sum(left, right)
                elif operator.gettokentype() == 'SUB':
                    return Sub(left, right)

        #################### TERM ####################
        @self.pg.production('term : factor')
        @self.pg.production('term : factor DIV term')
        @self.pg.production('term : factor MUL term')
        def term(p):
            if len(p) == 1:
                return p[0]
            else:
                right = p[2]
                left = p[0]
                operator = p[1]
                if operator.gettokentype() == 'DIV':
                    return Div(left, right)
                elif operator.gettokentype() == 'MUL':
                    return Mul(left, right)

        #################### FACTOR ####################
        @self.pg.production('factor : SUM factor')
        @self.pg.production('factor : SUB factor')
        @self.pg.production('factor : NOT factor')  # preciso fazer
        # @self.pg.production('factor : OPEN_PAREN parseOREXPR CLOSE_PAREN')
        @self.pg.production('factor : NUMBER')
        @self.pg.production('factor : IDENTIFIER')
        # fazer o readln
        def factor(p):
            # right = p[2]
            left = p[0]
            if left.gettokentype() == 'SUM':
                return UnOp("SUM", p[1])
            elif left.gettokentype() == 'SUB':
                return UnOp("SUB", p[1])
            elif left.gettokentype() == 'NOT':
                return UnOp("SUB", p[1])
            elif left.gettokentype() == "NUMBER":
                return Number(p[0].value)
            elif left.gettokentype() == "IDENTIFIER":
                return Getter(p[0].getstr())

        @self.pg.error
        def error_handle(token):
            raise ValueError(token)

    def get_parser(self):
        return self.pg.build()
