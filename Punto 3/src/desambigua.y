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

/* NO conflicts expected - grammar is unambiguous */

%%

prop    : prop_emparejada
        {
            INDENT(); printf("Reduce: prop → prop_emparejada\n");
        }
        | prop_no_emparejada
        {
            INDENT(); printf("Reduce: prop → prop_no_emparejada\n");
        }
        ;

prop_emparejada : IF EXPR THEN prop_emparejada ELSE prop_emparejada
        {
            INDENT(); printf("Reduce: prop_emparejada → if expr then prop_emparejada else prop_emparejada\n");
            printf("        (else MATCHED con if anterior)\n");
        }
        | STMT
        {
            INDENT(); printf("Reduce: prop_emparejada → instruccion\n");
        }
        ;

prop_no_emparejada : IF EXPR THEN prop
        {
            INDENT(); printf("Reduce: prop_no_emparejada → if expr then prop\n");
            printf("        (if WITHOUT emparejar)\n");
        }
        | IF EXPR THEN prop_emparejada ELSE prop_no_emparejada
        {
            INDENT(); printf("Reduce: prop_no_emparejada → if expr then prop_emparejada else prop_no_emparejada\n");
            printf("        (else matched, but overall unmatched)\n");
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
    printf("=== GRAMÁTICA DESAMBIGUADA (sin shift/reduce conflicts) ===\n\n");
    printf("Entrada esperada: i E t i E t s e s\n");
    printf("(if E then if E then stmt else stmt)\n\n");
    printf("Parseo (única derivación posible):\n");

    return yyparse();
}
