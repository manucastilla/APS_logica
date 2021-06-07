class SymbolTable:

    st_function = {}

    def __init__(self):
        self.a = {}

    def getter(self, value):
        return self.a[value]

    def setter_valor(self, value, number):
        self.a[value][0] = number

    def setter(self, value, v_type):
        if value in self.a:
            raise ValueError
        self.a[value] = [None, v_type]

    def setter_func(self, nome, func_name, func_type, params_name):
        if nome in self.st_function:
            raise ValueError("Already in the dictionary")

        self.st_function[nome] = [func_name, func_type, params_name]

    # pegar a função
    def getter_func(self, nome):

        return self.st_function[nome]

    def set_return(self, return_f, valor):
        self.st_function[return_f] = valor
