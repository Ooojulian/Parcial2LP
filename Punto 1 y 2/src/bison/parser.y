%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>

extern FILE* yyin;
int yylex();
void yyerror(const char *s);

typedef struct {
    char *type;
    char *value;
} ASTNode;

ASTNode* create_node(const char *type, const char *value);
void print_ast(ASTNode *node, int depth);

%}

%union {
    double num;
    char *str;
    int bval;
    void *node;
}

%token INSERT INTO FIND FROM UPDATE SET DELETE WHERE
%token LBRACE RBRACE LBRACKET RBRACKET
%token COLON COMMA
%token EQ LT GT
%token <str> STRING ID
%token <num> NUMBER
%token <bval> BOOLEAN

%type <node> S Stmt CreateStmt ReadStmt UpdateStmt DeleteStmt
%type <node> OptFilter Condition Operator Value Doc Members Pair
%type <node> Array Elements

%start S

%%

S   : Stmt S
    | Stmt
    ;

Stmt    : CreateStmt { printf("✓ CREATE instruccion\n"); }
        | ReadStmt   { printf("✓ READ instruccion\n"); }
        | UpdateStmt { printf("✓ UPDATE instruccion\n"); }
        | DeleteStmt { printf("✓ DELETE instruccion\n"); }
        ;

CreateStmt  : INSERT INTO ID Doc
            {
                printf("  INSERT INTO '%s'\n", $3);
            }
            ;

ReadStmt    : FIND FROM ID OptFilter
            {
                printf("  FIND FROM '%s'\n", $3);
            }
            ;

UpdateStmt  : UPDATE ID SET Doc OptFilter
            {
                printf("  UPDATE '%s'\n", $2);
            }
            ;

DeleteStmt  : DELETE FROM ID OptFilter
            {
                printf("  DELETE FROM '%s'\n", $3);
            }
            ;

OptFilter   : WHERE Condition
            {
                printf("    with WHERE clause\n");
            }
            | /* epsilon */
            ;

Condition   : STRING Operator Value
            {
                printf("    condition: %s\n", $1);
            }
            ;

Operator    : EQ { printf("      operator: =\n"); }
            | LT { printf("      operator: <\n"); }
            | GT { printf("      operator: >\n"); }
            ;

Doc : LBRACE Members RBRACE
    | LBRACE RBRACE
    {
        printf("    document: {}\n");
    }
    ;

Members : Pair COMMA Members
        | Pair
        ;

Pair    : STRING COLON Value
        {
            printf("      field: %s\n", $1);
        }
        ;

Value   : STRING
        {
            printf("        value: string\n");
        }
        | NUMBER
        {
            printf("        value: number\n");
        }
        | BOOLEAN
        {
            printf("        value: boolean\n");
        }
        | Doc
        {
            printf("        value: document\n");
        }
        | Array
        {
            printf("        value: array\n");
        }
        ;

Array   : LBRACKET Elements RBRACKET
        | LBRACKET RBRACKET
        {
            printf("        array: []\n");
        }
        ;

Elements    : Value COMMA Elements
            | Value
            ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "ERROR: %s\n", s);
}

int main(int argc, char **argv) {
    if (argc > 1) {
        yyin = fopen(argv[1], "r");
        if (!yyin) {
            perror("Cannot open file");
            return 1;
        }
    }

    printf("=== Language Analizador (Bison) ===\n");
    printf("Análisis sintáctico input...\n\n");

    int ret = yyparse();

    if (yyin && yyin != stdin) {
        fclose(yyin);
    }

    if (ret == 0) {
        printf("\n✓ Parse successful\n");
    } else {
        printf("\n✗ Parse fallo\n");
    }

    return ret;
}
