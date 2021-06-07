from parser_ import Parser
from lexical import Lexer
from symbolTable import SymbolTable
st = SymbolTable()

text_input = """
funcion int hola(){
    imprimir(6);
}
funcion int buenas(int x, int m){
    imprimir(m);
}
funcion int adios(){
    vuelve 6;
}
funcion int main()
{
    int x;
    x = 1;
    int a;
    a = 5;
    imprimir(x);
    imprimir(adios());
    hola();
    buenas(x, a);
    
}
"""


lexer = Lexer().get_lexer()
tokens = lexer.lex(text_input)

# for token in tokens:
#     print(token)

pg = Parser()
pg.parse()
parser = pg.get_parser()
parser.parse(tokens).eval(st)
