%{
#include <stdio.h>
#include <string.h>
#include "parser.tab.h"

int line_num = 1;
%}

%option nounput
%option noinput

%%

"INSERT"        { return INSERT; }
"INTO"          { return INTO; }
"FIND"          { return FIND; }
"FROM"          { return FROM; }
"UPDATE"        { return UPDATE; }
"SET"           { return SET; }
"DELETE"        { return DELETE; }
"WHERE"         { return WHERE; }

"true"          { yylval.bval = 1; return BOOLEAN; }
"false"         { yylval.bval = 0; return BOOLEAN; }

"{"             { return LBRACE; }
"}"             { return RBRACE; }
"["             { return LBRACKET; }
"]"             { return RBRACKET; }
":"             { return COLON; }
","             { return COMMA; }
"="             { return EQ; }
"<"             { return LT; }
">"             { return GT; }

\"[^\"]*\"      { yylval.str = strdup(yytext); return STRING; }

[0-9]+\.[0-9]+  { yylval.num = atof(yytext); return NUMBER; }
[0-9]+          { yylval.num = atoi(yytext); return NUMBER; }

[a-zA-Z_][a-zA-Z0-9_]*  { yylval.str = strdup(yytext); return ID; }

[ \t]+          { /* Skip whitespace */ }
\n              { line_num++; }

#.*             { /* Skip comments */ }

.               { fprintf(stderr, "Unexpected character '%c' at line %d\n", yytext[0], line_num); }

%%

int yywrap() {
    return 1;
}
