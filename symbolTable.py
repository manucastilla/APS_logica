class SymbolTable:
    def __init__(self):
        self.a = {}

    def getter(self, value):
        return self.a[value]

    def setter(self, value, number):
        self.a[value] = number
