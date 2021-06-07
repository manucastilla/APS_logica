from symbolTable import SymbolTable

st = SymbolTable()


class Number():
    def __init__(self, value):
        self.value = value

    def eval(self, st):
        return [int(self.value), "int"]


class BinaryOp():
    def __init__(self, left, right):
        self.left = left
        self.right = right


class Block():
    def __init__(self, children):
        self.children = children

    def eval(self, st):
        for node in self.children:
            if "return" in st.st_function:
                break
            node.eval(st)


class Setter(BinaryOp):
    def __init__(self, left, right, v_type):
        self.left = left
        self.right = right
        self.v_type = v_type

    def eval(self, st):

        if self.v_type in ["int", "bool"]:
            return st.setter(self.left, self.v_type)

        elif self.v_type == "vuelve":
            return st.set_return(self.left, self.right.eval(st))
        else:

            s = st.getter(self.left)
            if s[1] == "bool":
                return st.setter_valor(
                    self.left, int(bool(self.right.eval(st)[0]))
                )
            else:
                st.setter_valor(self.left, self.right.eval(st)[0])


class Getter(BinaryOp):
    def __init__(self, value):
        self.value = value

    def eval(self, st):
        # if self.v_type == "function":
        #     return st.getter_func(self.value)
        return st.getter(self.value)


class PlusOne(BinaryOp):
    def eval(self, st):
        return int(self.left.eval(st) + 1)


class PlusEqual(BinaryOp):
    def eval(self, st):
        c = self.left.eval(st)
        c += self.right.eval(st)
        return c


class MinusEqual(BinaryOp):
    def eval(self, st):
        c = self.left.eval(st)
        c -= self.right.eval(st)
        return c


class Greater(BinaryOp):
    def eval(self, st):
        return int(self.left.eval(st) < self.right.eval(st))


class Equal_Equal(BinaryOp):
    def eval(self, st):
        return int(self.left.eval(st) == self.right.eval(st))


class Less(BinaryOp):
    def eval(self, st):
        return int(self.left.eval(st) > self.right.eval(st))


class Or(BinaryOp):
    def eval(self, st):
        return int(self.left.eval(st) or self.right.eval(st))


class And(BinaryOp):
    def eval(self, st):
        return int(self.left.eval(st) and self.right.eval(st))


class Sum(BinaryOp):
    def eval(self, st):
        return self.left.eval(st) + self.right.eval(st)


class Sub(BinaryOp):
    def eval(self, st):
        return self.left.eval(st) - self.right.eval(st)


class Mul(BinaryOp):
    def eval(self, st):
        return int(self.left.eval(st) * self.right.eval(st))


class Div(BinaryOp):
    def eval(self, st):
        return int(self.left.eval(st) / self.right.eval(st))


class Rest(BinaryOp):
    def eval(self, st):
        return int(self.left.eval(st) % self.right.eval(st))


class UnOp(BinaryOp):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def eval(self, st):
        if self.value == "SUM":
            return self.children.eval(st)
        elif self.value == "SUB":
            return -self.children.eval(st)
        elif self.value == "NOT":
            return int(not self.children.eval(st))


class Identifier():
    def __init__(self, value):
        self.value = value

    def eval(self, st):
        return st.getter(self.value)

    # class For(BinaryOp, Number):
    #     def eval(self, st):
    #         i = self.value.eval(st)
    #         while i < self.left.eval(st):
    #             self.right.eval(st)
    #             i += 1


class If():
    def __init__(self, children):
        self.children = children

    def eval(self, st):
        if self.children[0].eval(st):
            self.children[1].eval(st)
        else:
            if self.children[2] != None:
                self.children[2].eval(st)


class While():
    def __init__(self, children):
        self.children = children

    def eval(self, st):
        while self.children[0].eval(st):
            self.children[1].eval(st)


class Print():
    def __init__(self, value):
        self.value = value

    def eval(self, st):
        print(self.value.eval(st)[0])


class FuncCall():
    def __init__(self, func_name, name_params):
        self.func_name = func_name
        self.name_params = name_params

    def eval(self, st):
        funcSt = SymbolTable()
        args = st.getter_func(self.func_name)

        # print(args[1])
        # print(self.name_params)

        if len(self.name_params) != 0:
            for i in range(len(args[1])):
                # print(self.name_params[i].eval(st))
                # print(args[1][i][0])
                a, b = self.name_params[i].eval(st)
                funcSt.setter(args[1][i][1], b)
                funcSt.setter_valor(args[1][i][1], a)

                if b == "string":
                    raise ValueError("Cannot operate string")

        args[2].eval(funcSt)

        if "vuelve" in funcSt.st_function:
            return_return = funcSt.getter_func("vuelve")
            if args[0].lower() == return_return[1]:
                del funcSt.st_function["vuelve"]
                return return_return
            else:
                raise ValueError


class FuncDec():
    def __init__(self, children, func_name, func_type):
        self.children = children
        self.func_name = func_name
        self.func_type = func_type

    def eval(self, st):
        return st.setter_func(
            self.func_name,
            self.func_type,
            self.children[0],
            self.children[1],
        )
