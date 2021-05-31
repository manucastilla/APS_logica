from symbolTable import SymbolTable

st = SymbolTable()


class Number():
    def __init__(self, value):
        self.value = value

    def eval(self):
        return int(self.value)


class BinaryOp():
    def __init__(self, left, right):
        self.left = left
        self.right = right


class Block():
    def __init__(self, children):
        self.children = children

    def eval(self):
        for node in self.children:
            node.eval()


class Setter(BinaryOp):
    def __init__(self, left, right, v_type):
        self.left = left
        self.right = right
        self.v_type = v_type

    def eval(self):
        if self.v_type in ["int", "bool"]:
            return st.setter(self.left, self.v_type)
        else:
            s = st.getter(self.left)
            if s[1] == "bool":
                return st.setter_valor(
                    self.left, int(bool(self.right.eval()))
                )


class Getter(BinaryOp):
    def __init__(self, value):
        self.value = value

    def eval(self):
        return st.getter(self.value)


class PlusOne(BinaryOp):
    def eval(self):
        return int(self.left.eval() + 1)


class PlusEqual(BinaryOp):
    def eval(self):
        c = self.left.eval()
        c += self.right.eval()
        return c


class MinusEqual(BinaryOp):
    def eval(self):
        c = self.left.eval()
        c -= self.right.eval()
        return c


class Greater(BinaryOp):
    def eval(self):
        return int(self.left.eval() < self.right.eval())


class Equal_Equal(BinaryOp):
    def eval(self):
        return int(self.left.eval() == self.right.eval())


class Less(BinaryOp):
    def eval(self):
        return int(self.left.eval() > self.right.eval())


class Or(BinaryOp):
    def eval(self):
        return int(self.left.eval() or self.right.eval())


class And(BinaryOp):
    def eval(self):
        return int(self.left.eval() and self.right.eval())


class Sum(BinaryOp):
    def eval(self):
        return self.left.eval() + self.right.eval()


class Sub(BinaryOp):
    def eval(self):
        return self.left.eval() - self.right.eval()


class Mul(BinaryOp):
    def eval(self):
        return int(self.left.eval() * self.right.eval())


class Div(BinaryOp):
    def eval(self):
        return int(self.left.eval() / self.right.eval())


class Rest(BinaryOp):
    def eval(self):
        return int(self.left.eval() % self.right.eval())


class UnOp(BinaryOp):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def eval(self):
        if self.value == "SUM":
            return self.children.eval()
        elif self.value == "SUB":
            return -self.children.eval()
        elif self.value == "NOT":
            return int(not self.children.eval())


class Identifier():
    def __init__(self, value):
        self.value = value

    def eval(self):
        return st.getter(self.value)

    # class For(BinaryOp, Number):
    #     def eval(self):
    #         i = self.value.eval()
    #         while i < self.left.eval():
    #             self.right.eval()
    #             i += 1


class If():
    def __init__(self, children):
        self.children = children

    def eval(self):
        if self.children[0].eval():
            self.children[1].eval()
        else:
            if self.children[2] != None:
                self.children[2].eval()


class While():
    def __init__(self, children):
        self.children = children

    def eval(self):
        while self.children[0].eval():
            self.children[1].eval()


class Print():
    def __init__(self, value):
        self.value = value

    def eval(self):
        print(self.value.eval())
