class SymbolTable:
    def __init__(self):
        self.a = {}

    def getter(self, value):
        return self.a[value]

    def setter_valor(self, value, number):
        self.a[value] = number

    def setter_func(self, name):
        self.a[name] = {}

    def setter(self, value, v_type):
        if value in self.a:
            raise ValueError
        self.a[value] = [None, v_type]
