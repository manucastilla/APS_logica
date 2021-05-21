from parser_ import Parser
from lexical import Lexer


text_input = """{
    x = 1;
    todavia(x mas_grande 5){
        x = x + 1;
        imprimir(x);
    }
    se (x lo_mismo 5){
        imprimir(10);
    }
}
"""


lexer = Lexer().get_lexer()
tokens = lexer.lex(text_input)

# for token in tokens:
#     print(token)

pg = Parser()
pg.parse()
parser = pg.get_parser()
parser.parse(tokens).eval()
