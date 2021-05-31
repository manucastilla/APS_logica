from parser_ import Parser
from lexical import Lexer


text_input = """
funcion main()
{
    // comentario //
    bool x;
    x = 1;
    imprimir(x);
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
