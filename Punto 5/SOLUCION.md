# Solución — Implementación del Analizador Descendente Recursivo

## Enunciado

> Diseñe e implemente un algoritmo de emparejamiento para el algoritmo descendente recursivo. Para probar, diseñe una gramática que pueda hacer operaciones de asignación y operaciones de condicionales.

La gramática diseñada está en [`CONCEPTOS.md`](CONCEPTOS.md).

---

## Función parea() — Algoritmo de emparejamiento

La función `parea()` es el núcleo del analizador. Se encuentra en `src/analizador_descendente.py`.

```python
def parea(self, esperado: str) -> Token:
    tok = self.preanalisis
    if tok.tipo == esperado or tok.valor == esperado:
        self.pos += 1
        self.preanalisis = self.tokens[self.pos]
        return tok
    else:
        raise SyntaxError(
            f"Error de emparejamiento en columna {tok.col}\n"
            f"  Esperado : '{esperado}'\n"
            f"  Obtenido : {tok.tipo}  →  '{tok.valor}'"
        )
```

**Cómo funciona paso a paso** para `x = 5 + 3`:

```
Llamada a InstrAsignacion():

  Paso 1: parea('ID')
          preanalisis = Token(ID, 'x', col=0)
          'x'.tipo == 'ID' → coincide
          Consume 'x', avanza → preanalisis = Token(ASIG, '=')

  Paso 2: parea('=')
          preanalisis = Token(ASIG, '=', col=2)
          '='.valor == '=' → coincide
          Consume '=', avanza → preanalisis = Token(NUMERO, '5')

  Paso 3: Expr()  → procesa '5 + 3'
          Factor():   parea('NUMERO') → consume '5'
          ExprPrima():  parea('+') → consume '+'
          Factor():   parea('NUMERO') → consume '3'

  Resultado: ACEPTADO
```

---

## Implementación

Una función por cada no-terminal. Cada función usa `parea()` para los terminales:

```python
def InstrAsignacion(self):
    """InstrAsignacion → id = Expr"""
    self.parea('ID')
    self.parea('=')
    self.Expr()

def InstrIf(self):
    """InstrIf → if ( Expr ) then Stmt IfRest"""
    self.parea('IF')
    self.parea('(')
    self.Expr()
    self.parea(')')
    self.parea('THEN')
    self.Stmt()
    self.IfRest()

def IfRest(self):
    """IfRest → else Stmt | ε"""
    if self.preanalisis.valor == 'else':
        self.parea('ELSE')
        self.Stmt()
    # else: ε
```

---

## Pruebas

### Casos válidos — operaciones de asignación

| Entrada | Resultado |
|---------|-----------|
| `x = 5` | ✓ ACEPTADO |
| `x = 5 + 3` | ✓ ACEPTADO |
| `x = ( 2 + 3 ) * 4` | ✓ ACEPTADO |
| `x = 5 ; y = 10` | ✓ ACEPTADO |

### Casos válidos — operaciones de condicionales

| Entrada | Resultado |
|---------|-----------|
| `if (a > b) then x = 10` | ✓ ACEPTADO |
| `if (a > b) then x = 10 else y = 20` | ✓ ACEPTADO |
| `if (x == 0) then y = 1 else y = x + 1` | ✓ ACEPTADO |
| `if (a >= b) then x = 1 else if (a < b) then x = 2 else x = 3` | ✓ ACEPTADO |

### Casos inválidos — parea() detecta el error exacto

| Entrada | Error detectado |
|---------|----------------|
| `x =` | `Se esperaba '(', identificador o número en columna 3, se encontró '$'` |
| `if a > b then x = 10` | `Esperado: '('  Obtenido: ID → 'a'` (falta paréntesis) |
| `if (a > b) x = 10` | parser no encuentra `then` |
| `= 5` | `Se esperaba una sentencia (id o if) en columna 0, pero se encontró '='` |
| `x = 5 y` | `Tokens inesperados al final en columna 6: 'y'` |

**13/13 pruebas exitosas.**

---

## Traza de derivación — caso del enunciado

**Entrada:** `if (a > b) then x = 10 else y = 20`

```
S
└── Stmt
    └── InstrIf
         ├── parea('IF')       → consume 'if'
         ├── parea('(')        → consume '('
         ├── Expr()
         │    ├── Termino → Factor → parea('ID')   → consume 'a'
         │    └── ExprPrima
         │         ├── parea('REL_OP')  → consume '>'
         │         └── Termino → Factor → parea('ID') → consume 'b'
         ├── parea(')')        → consume ')'
         ├── parea('THEN')     → consume 'then'
         ├── Stmt()
         │    └── InstrAsignacion
         │         ├── parea('ID')   → consume 'x'
         │         ├── parea('=')    → consume '='
         │         └── Expr → Termino → Factor → parea('NUMERO') → consume '10'
         └── IfRest()
              ├── parea('ELSE')     → consume 'else'
              └── Stmt()
                   └── InstrAsignacion
                        ├── parea('ID')   → consume 'y'
                        ├── parea('=')    → consume '='
                        └── Expr → Termino → Factor → parea('NUMERO') → consume '20'

RESULTADO: ✓ ACEPTADO
```
