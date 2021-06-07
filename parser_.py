from symbolTable import SymbolTable
from rply import ParserGenerator
from ast import(Number, Sum, Sub, Print, Mul, Div, Rest,
                If, Or, And, Less, Greater, MinusEqual, PlusEqual, PlusOne,
                Block, Setter, Getter, Equal_Equal, UnOp, Identifier, While,
                FuncCall, FuncDec)


st = SymbolTable()


class Parser():
    params_name = []

    def __init__(self):
        self.pg = ParserGenerator(
            # A list of all token names accepted by the parser.
            ['NUMBER', 'PRINT', 'OPEN_PAREN', 'CLOSE_PAREN',
             'SEMI_COLON', 'OPEN_BRACES', 'CLOSE_BRACES',
             'EQUAL', 'IDENTIFIER', 'LESS', 'GREATER',
             'SUM', 'SUB', 'NOT', 'MUL', 'DIV', 'EQUAL_EQUAL',
             'AND', 'OR', 'IF', 'ELSE', 'WHILE', 'TYPE', 'FUNCTION', 'COMMA', 'RETURN']
        )

    def parse(self):
        #################### START ####################
        #                               p[0]       p[1]      p[2]
        @self.pg.production('start : def_function')
        @self.pg.production('start : def_function start')
        def begin(p):
            if len(p) == 1:
                return Block([p[0]])

            p[0].children += [p[1]]

            return p[0]

        #################### FUNCTION ####################
        #                                    p[0]    p[1]     p[2]      p[3]    p[4]         p[5]
        @self.pg.production('def_function : FUNCTION TYPE IDENTIFIER OPEN_PAREN CLOSE_PAREN begin')
        @self.pg.production('def_function : FUNCTION TYPE IDENTIFIER OPEN_PAREN params CLOSE_PAREN begin')
        @self.pg.production('def_function : def_function FUNCTION TYPE IDENTIFIER OPEN_PAREN params CLOSE_PAREN begin')
        @self.pg.production('def_function : def_function FUNCTION TYPE IDENTIFIER OPEN_PAREN  CLOSE_PAREN begin')
        def def_function(p):
            lista_func = []

            if len(p) == 6:
                if p[2].getstr() == 'main':
                    FuncDec([lista_func, p[5]], p[2].getstr(),
                            p[1].getstr()).eval(st)
                    return FuncCall(p[2].getstr(), [])
                else:
                    return FuncDec([lista_func, p[5]], p[2].getstr(), p[1].getstr()).eval(st)
            elif len(p) == 7:
                if p[3].getstr() == 'main':

                    FuncDec([lista_func, p[6]], p[3].getstr(),
                            p[2].getstr()).eval(st)
                    return FuncCall(p[3].getstr(), [])

                return FuncDec([p[4], p[6]], p[3].getstr(), p[2].getstr()).eval(st)
            else:

                return FuncDec(
                    [p[5], p[7]], p[3].getstr(), p[2].getstr()).eval(st)

        @ self.pg.production('params : TYPE IDENTIFIER')
        #                              p[0]    [1]    p[2]    p[3]
        @ self.pg.production('params : params COMMA TYPE IDENTIFIER')
        # fazer isso depois
        def params(p):
            if len(p) == 2:
                return [[p[0].getstr(), p[1].getstr()]]

            params_type = p[2]
            p_name = p[3]

            p[0].append([p[2].getstr(), p[3].getstr()])
            return p[0]

        #################### BLOCK ####################

        @ self.pg.production('begin : OPEN_BRACES block CLOSE_BRACES ')
        def begin(p):
            return p[1]

        @ self.pg.production('block : command')
        @ self.pg.production('block : block command')
        # arrumar porque ta igual do ma
        def block(p):
            if len(p) == 1:
                return Block([p[0]])

            p[0].children += [p[1]]
            return p[0]

        #################### COMMAND ####################
        @ self.pg.production('command : SEMI_COLON')
        @ self.pg.production('command : assignment SEMI_COLON')
        @ self.pg.production('command : println')
        @ self.pg.production('command : if_cond')
        @ self.pg.production('command : while_cond')
        @ self.pg.production('command : definition SEMI_COLON')
        @ self.pg.production('command : return_fun SEMI_COLON')
        # @self.pg.production('command : while')
        def command(p):
            return p[0]

        @self.pg.production('return_fun : RETURN parseOREXPR')
        def return_fun(p):
            return Setter("vuelve", p[1], "vuelve")

        #################### ASSIGNMENT and DEFINITION ####################
        @self.pg.production('assignment : IDENTIFIER OPEN_PAREN CLOSE_PAREN')
        @self.pg.production('assignment : IDENTIFIER OPEN_PAREN params_assignment CLOSE_PAREN')
        @self.pg.production('assignment : IDENTIFIER EQUAL parseOREXPR')
        def assignment(p):
            if len(p) == 3:
                if p[1].gettokentype() == "EQUAL":
                    return Setter(p[0].getstr(), p[2], None)
                else:
                    node = FuncCall(p[0].getstr(), [])
                    return node

            else:
                # args = []
                node = p[2]

                return FuncCall(p[0].getstr(), node)

        @ self.pg.production('params_assignment :  parseOREXPR')
        #                              p[0]    [1]    p[2]    p[3]
        @ self.pg.production('params_assignment :  params_assignment COMMA parseOREXPR')
        def params_assignment(p):
            if len(p) == 1:
                return [p[0]]
            else:
                p[0].append(p[2])
                return p[0]

        @ self.pg.production('definition : TYPE IDENTIFIER')
        def definition(p):
            return Setter(p[1].getstr(), None, p[0].getstr())
        #################### PRINT ####################

        @ self.pg.production('println : PRINT OPEN_PAREN parseOREXPR CLOSE_PAREN SEMI_COLON')
        # @self.pg.production('println : PRINT OPEN_PAREN variable expression CLOSE_PAREN SEMI_COLON')
        def println(p):
            return Print(p[2])

        #################### WHILE AND FOR ####################
        #                                  p[0] p[1]        p[2]       p[3]         p[4]
        @ self.pg.production('while_cond : WHILE OPEN_PAREN parseOREXPR CLOSE_PAREN begin')
        def while_cond(p):
            condition = p[2]
            todo = p[4]
            return While([condition, todo])

        #################### IF ####################
        #                             p[0] p[1]        p[2]       p[3]         p[4]       p[5]  p[6]
        @ self.pg.production('if_cond : IF OPEN_PAREN parseOREXPR CLOSE_PAREN begin')
        @ self.pg.production('if_cond : IF OPEN_PAREN parseOREXPR CLOSE_PAREN begin ELSE begin')
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

        @ self.pg.production('parseOREXPR : parseANDEXPR')
        @ self.pg.production('parseOREXPR : parseANDEXPR OR parseOREXPR')
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
        @ self.pg.production('parseANDEXPR : parseEQEXPR')
        @ self.pg.production('parseANDEXPR : parseEQEXPR AND parseANDEXPR')
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
        @ self.pg.production('parseEQEXPR : parseRELEXPR')
        @ self.pg.production('parseEQEXPR : parseRELEXPR EQUAL_EQUAL parseEQEXPR')
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
        @ self.pg.production('parseRELEXPR : expression')
        @ self.pg.production('parseRELEXPR : expression LESS parseRELEXPR')
        @ self.pg.production('parseRELEXPR : expression GREATER parseRELEXPR')
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
        @ self.pg.production('expression : term')
        @ self.pg.production('expression : term SUM expression')
        @ self.pg.production('expression : term SUB expression')
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
        @ self.pg.production('term : factor')
        @ self.pg.production('term : factor DIV term')
        @ self.pg.production('term : factor MUL term')
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
        @ self.pg.production('factor : SUM factor')
        @ self.pg.production('factor : SUB factor')
        @ self.pg.production('factor : NOT factor')  # preciso fazer
        # @self.pg.production('factor : OPEN_PAREN parseOREXPR CLOSE_PAREN')
        @ self.pg.production('factor : NUMBER')
        @ self.pg.production('factor : IDENTIFIER')
        @self.pg.production('factor : IDENTIFIER OPEN_PAREN CLOSE_PAREN')
        @self.pg.production('factor : IDENTIFIER OPEN_PAREN params_assignment CLOSE_PAREN')
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
                if len(p) == 1:
                    return Getter(p[0].getstr())
                elif len(p) == 3:
                    return FuncCall(p[0].getstr(), [])
                else:
                    return FuncCall(p[0].getstr(), p[2])

        @ self.pg.error
        def error_handle(token):
            raise ValueError(token)

    def get_parser(self):
        return self.pg.build()
