# APS_logica

```
EBNF DE C EM PERUANO

BLOCK = { COMMAND };
COMMAND = ( λ | ASSIGNMENT | PRINT |  LOOP-STATEMENT | IF-STATEMENT | JUMP-STATEMENT). ";" ;
JUMP-STATEMENT = { "seva", IDENTIFIER | "enfrente" | "rompe" | "retorna", EXPRESSION
};
ASSIGNMENT = IDENTIFIER, "=", EXPRESSION ;
LOOP-STATEMENT = ( WHILE-STATEMENT | FOR-STATEMENT) ; 
TYPE = {
      char
    | short
    | int
    | long
    | float
    | double
    | signed
    | unsigned
    | STRUCT_OR_UNION_SPECIFIER
    | ENUM-SPECIFIER
    | TYPEDEF-NAME
};
WHILE-STATEMENT =  "todavia", "(", CONDITION_MORE, ")", "{", BLOCK ,"}" ;
FOR-STATEMENT = "por", "(" TYPE, ASSIGNMENT, ";", IDENTIFIER, "<", "IDENTIFIER, ";", IDENTIFIER, "++" ")", "{", BLOCK ,"}" ;
PRINT = "println", "(", EXPRESSION, ")" ;
EXPRESSION = TERM, { ("+" | "-"), TERM } ;
CONDITION_MORE = (CONDITION | CONDITION_MORE);
CONDITION = (EXPRESSION, LOGICAL, EXPRESSION);
LOGICAL = 
             *=
            | /=
            | %=
            | +=
            | -=
            | <<=
            | >>=
            | &=
            | ^=
            | |=;
IF-STATEMENT = "se", "(", CONDITION_MORE, ")", "{", BLOCK, "}" {ELSE-STATEMENT}| ELSE-IF-STATEMENT;
ELSE-IF-STATEMENT = "seno","se", "(", CONDITION_MORE, ")", "{", BLOCK, "}" {ELSE-STATEMENT}| ELSE-IF-STATEMENT;
ELSE-STATEMENT = "seno", "{", (BLOCK| IF-STATEMENT), "}"
TERM = FACTOR, { ("*" | "/"), FACTOR };
FACTOR = ("+" | "-"), FACTOR | "(", EXPRESSION, ")" | NUMBER;
IDENTIFIER = LETTER, { LETTER | DIGIT | "_" } ;
NUMBER = DIGIT, { DIGIT } ;
LETTER = ( a | ... | z | A | ... | Z ) ;
DIGIT = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 ) ;
```