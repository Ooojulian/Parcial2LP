%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int yylex();
void yyerror(const char *s);

int depth = 0;

#define INDENT() for(int i=0; i<depth*2; i++) printf(" ");

%}

%union {
    char *str;
}

%token IF THEN ELSE
%token <str> EXPR STMT

%start prop

%expect 1          /* Expect 1 shift/reduce conflict (dangling else) */

%%

prop    : IF EXPR THEN prop
        {
            INDENT(); printf("Reduce: if-then-prop (sin else)\n");
        }
        | prop_emparejada
        {
            INDENT(); printf("Reduce: prop_emparejada\n");
        }
        ;

prop_emparejada : IF EXPR THEN prop_emparejada ELSE prop
        {
            INDENT(); printf("Reduce: if-then-emparejada-else-prop\n");
        }
        | STMT
        {
            INDENT(); printf("Reduce: instruccion\n");
        }
        ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "ERROR: %s\n", s);
}

int yylex() {
    int c = getchar();

    switch(c) {
        case 'i': return IF;
        case 't': return THEN;
        case 'e': return ELSE;
        case 's': return STMT;
        case 'E': yylval.str = "expr"; return EXPR;
        case '\n':
        case ' ':
        case '\t': return yylex();  /* Skip whitespace */
        case EOF: return 0;
        default: return c;
    }
}

int main() {
    printf("=== GRAMÁTICA AMBIGUA (con shift/reduce conflict) ===\n\n");
    printf("Entrada esperada: i E t i E t s e s\n");
    printf("(if E then if E then stmt else stmt)\n\n");
    printf("Parseo:\n");

    return yyparse();
}
