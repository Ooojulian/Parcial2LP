# Conceptos — Análisis Descendente Recursivo

## Función parea()

El corazón de un analizador descendente recursivo. Verifica que el token actual coincida con el esperado, lo consume y avanza el preanálisis.

```python
def parea(self, esperado: str) -> Token:
    tok = self.preanalisis
    if tok.tipo == esperado or tok.valor == esperado:
        self.pos += 1
        self.preanalisis = self.tokens[self.pos]
        return tok
    else:
        raise SyntaxError(f"Esperado {esperado}, obtuve {tok.tipo}")
```

Si coincide → consume y avanza. Si no → error con contexto exacto.

## Gramática diseñada

### Gramática original (con problemas)

```
Stmt → id = Expr
     | if ( Expr ) then Stmt else Stmt
     | Stmt ; Stmt          ← recursión izquierda

Expr → Expr + Termino       ← recursión izquierda
     | Termino
```

La recursión izquierda impide el análisis descendente — el parser entraría en bucle infinito.

### Gramática LL(1) final (sin recursión izquierda)

```
S                → Stmt
Stmt             → InstrAsignacion StmtPrime
                 | InstrIf StmtPrime
                 | ε
StmtPrime        → ; Stmt | ε

InstrAsignacion  → id = Expr
InstrIf          → if ( Expr ) then Stmt IfRest
IfRest           → else Stmt | ε

Expr             → Termino ExprAdd ExprPrima
ExprAdd          → AddOp Termino ExprAdd | ε
ExprPrima        → RelOp Termino ExprAdd | ε

Termino          → Factor TerminoPrima
TerminoPrima     → MulOp Factor TerminoPrima | ε

Factor           → ( Expr ) | id | num

RelOp            → > | < | >= | <= | == | !=
AddOp            → + | -
MulOp            → * | /
```

## Conjuntos FIRST y FOLLOW

Necesarios para que el parser sepa qué regla aplicar con 1 token de lookahead.

| No-terminal | FIRST | FOLLOW |
|-------------|-------|--------|
| Stmt | `{id, if, ε}` | `{;, else, $}` |
| InstrAsignacion | `{id}` | `{;, else, $}` |
| InstrIf | `{if}` | `{;, else, $}` |
| IfRest | `{else, ε}` | `{;, $}` |
| Expr | `{id, num, (}` | `{), then, else, ;, $}` |
| Termino | `{id, num, (}` | `{RelOp, +, -, ), then, else, ;, $}` |
| Factor | `{id, num, (}` | `{*, /, +, -, RelOp, ), then, else, ;, $}` |

## Estructura del analizador

Una función por cada no-terminal. Cada función llama a `parea()` para los terminales y a las otras funciones para los no-terminales.

```
Stmt()
 ├── InstrAsignacion()
 │    ├── parea('ID')
 │    ├── parea('=')
 │    └── Expr()
 │         ├── Termino()
 │         │    ├── Factor()   → parea('ID') | parea('NUMERO') | parea('(')...
 │         │    └── TerminoPrima()
 │         └── ExprPrima()
 └── InstrIf()
      ├── parea('IF')
      ├── parea('(')
      ├── Expr()
      ├── parea(')')
      ├── parea('THEN')
      ├── Stmt()
      └── IfRest()
           └── parea('ELSE') + Stmt()  |  ε
```
