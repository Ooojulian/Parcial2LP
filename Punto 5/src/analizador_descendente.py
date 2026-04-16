"""
Analizador Descendente Recursivo (Recursive Descent Analizador)
Punto 5 — Parcial 2 LP

Función principal: parea(token_esperado)
  - Verifica que token actual == esperado
  - Si coincide: consume y avanza preanálisis
  - Si no coincide: lanza SyntaxError detallado

Gramática LL(1) sin recursión izquierda:
    S          → Stmt
    Stmt       → InstrAsignacion StmtPrime
               | InstrIf     StmtPrime
               | ε
    StmtPrime  → ; Stmt | ε
    InstrAsignacion → id = Expr
    InstrIf     → if ( Expr ) then Stmt IfRest
    IfRest     → else Stmt | ε
    Expr       → Termino ExprAdd ExprPrima
    ExprAdd    → AddOp Termino ExprAdd | ε
    ExprPrima  → RelOp Termino ExprAdd | ε
    Termino    → Factor TerminoPrima
    TerminoPrima → MulOp Factor TerminoPrima | ε
    Factor     → ( Expr ) | id | num
    RelOp      → > | < | >= | <= | == | !=
    MulOp      → * | /
    AddOp      → + | -
"""

import re
from dataclasses import dataclass
from typing import List

# ──────────────────────────────────────────────
# TOKENS
# ──────────────────────────────────────────────

@dataclass
class Token:
    tipo:  str
    valor: str
    col:   int

    def __repr__(self):
        return f"Token({self.tipo}, '{self.valor}', col={self.col})"


PALABRAS_CLAVE = {'if', 'then', 'else'}

PATRONES = [
    ('ESPACIO',   r'[ \t]+'),
    ('NUMERO',    r'\d+'),
    ('REL_OP',    r'>=|<=|==|!=|>|<'),
    ('MUL_OP',    r'[*/]'),
    ('ADD_OP',    r'[+\-]'),
    ('ASIG',      r'='),
    ('LPAREN',    r'\('),
    ('RPAREN',    r'\)'),
    ('SEMICOLON', r';'),
    ('ID',        r'[a-zA-Z_]\w*'),
]


def tokenizar(texto: str) -> List[Token]:
    """Convierte texto en lista de tokens"""
    tokens = []
    pos = 0
    while pos < len(texto):
        for tipo, patron in PATRONES:
            m = re.match(patron, texto[pos:])
            if m:
                val = m.group(0)
                if tipo != 'ESPACIO':
                    # Palabras clave → tipo propio
                    t = val.upper() if val in PALABRAS_CLAVE else tipo
                    tokens.append(Token(t, val, pos))
                pos += len(val)
                break
        else:
            raise SyntaxError(
                f"Carácter inválido '{texto[pos]}' en columna {pos}"
            )
    tokens.append(Token('$', '$', pos))
    return tokens


# ──────────────────────────────────────────────
# PARSER
# ──────────────────────────────────────────────

class Analizador:
    """
    Analizador Sintáctico Descendente Recursivo LL(1)

    Atributo principal:
        preanálisis (preanalisis): token actual que se está analizando
    """

    def __init__(self, tokens: List[Token]):
        self.tokens   = tokens
        self.pos      = 0
        # preanálisis apunta al primer token
        self.preanalisis = self.tokens[0]

    # ──────────────────────────────────────────
    # FUNCIÓN PAREA (matching / emparejamiento)
    # ──────────────────────────────────────────

    def parea(self, esperado: str) -> Token:
        """
        Empareja el token actual con el esperado.

        Si el tipo o valor del preanálisis == esperado:
            ✓ consume el token y avanza el preanálisis
        Si no coincide:
            ✗ lanza SyntaxError con mensaje preciso

        Args:
            esperado: tipo ('ID', 'NUMERO', 'REL_OP') o
                      valor literal ('=', '(', 'if', ';')

        Returns:
            El token que fue consumido.
        """
        tok = self.preanalisis
        if tok.tipo == esperado or tok.valor == esperado:
            # ── Avanzar preanálisis ──
            self.pos += 1
            self.preanalisis = (
                self.tokens[self.pos]
                if self.pos < len(self.tokens)
                else Token('$', '$', -1)
            )
            return tok
        else:
            raise SyntaxError(
                f"\n  ✗ Error de emparejamiento en columna {tok.col}\n"
                f"    Esperado : '{esperado}'\n"
                f"    Obtenido : {tok.tipo}  →  '{tok.valor}'\n"
            )

    # ──────────────────────────────────────────
    # REGLAS GRAMATICALES (una función por NT)
    # ──────────────────────────────────────────

    def S(self):
        """S → Stmt"""
        self.Stmt()

    def Stmt(self):
        """
        Stmt → InstrAsignacion StmtPrime
              | InstrIf     StmtPrime
              | ε
        """
        if self.preanalisis.tipo == 'ID':
            self.InstrAsignacion()
            self.StmtPrime()
        elif self.preanalisis.tipo == 'IF':
            self.InstrIf()
            self.StmtPrime()
        elif self.preanalisis.tipo in ('$', 'ELSE', 'RPAREN', 'SEMICOLON'):
            pass  # ε
        else:
            raise SyntaxError(
                f"\n  ✗ Se esperaba una sentencia (id o if) en columna "
                f"{self.preanalisis.col}, pero se encontró '{self.preanalisis.valor}'\n"
            )

    def StmtPrime(self):
        """StmtPrime → ; Stmt | ε"""
        if self.preanalisis.valor == ';':
            self.parea(';')
            self.Stmt()
        # else ε

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
        if self.preanalisis.tipo == 'ELSE':
            self.parea('ELSE')
            self.Stmt()
        # else ε

    def Expr(self):
        """Expr → Termino ExprAdd ExprPrima

        Precedencia: * / antes que + - antes que relacionales
        """
        self.Termino()
        self.ExprAdd()
        self.ExprPrima()

    def ExprAdd(self):
        """ExprAdd → AddOp Termino ExprAdd | ε"""
        if self.preanalisis.tipo == 'ADD_OP':
            self.parea('ADD_OP')
            self.Termino()
            self.ExprAdd()
        # else ε

    def ExprPrima(self):
        """ExprPrima → RelOp Termino ExprAdd | ε"""
        if self.preanalisis.tipo == 'REL_OP':
            self.parea('REL_OP')
            self.Termino()
            self.ExprAdd()
        # else ε

    def Termino(self):
        """Termino → Factor TerminoPrima"""
        self.Factor()
        self.TerminoPrima()

    def TerminoPrima(self):
        """TerminoPrima → MulOp Factor TerminoPrima | ε"""
        if self.preanalisis.tipo == 'MUL_OP':
            self.parea('MUL_OP')
            self.Factor()
            self.TerminoPrima()
        # else ε

    def Factor(self):
        """Factor → ( Expr ) | id | num"""
        if self.preanalisis.valor == '(':
            self.parea('(')
            self.Expr()
            self.parea(')')
        elif self.preanalisis.tipo == 'ID':
            self.parea('ID')
        elif self.preanalisis.tipo == 'NUMERO':
            self.parea('NUMERO')
        else:
            raise SyntaxError(
                f"\n  ✗ Se esperaba '(', identificador o número en columna "
                f"{self.preanalisis.col}, se encontró '{self.preanalisis.valor}'\n"
            )

    # ──────────────────────────────────────────
    # PUNTO DE ENTRADA
    # ──────────────────────────────────────────

    def parse(self) -> bool:
        """Inicia el análisis sintáctico descendente"""
        self.S()
        if self.preanalisis.tipo != '$':
            raise SyntaxError(
                f"\n  ✗ Tokens inesperados al final en columna "
                f"{self.preanalisis.col}: '{self.preanalisis.valor}'\n"
            )
        return True


def analizar(codigo: str, verbose: bool = True) -> bool:
    """
    Analiza una cadena usando el analizador descendente recursivo.

    Returns:
        True si es sintácticamente correcto, False si no.
    """
    try:
        tokens = tokenizar(codigo)
        p = Analizador(tokens)
        p.parse()
        if verbose:
            print(f"  ✓ ACEPTADO")
        return True
    except SyntaxError as e:
        if verbose:
            print(f"  ✗ RECHAZADO: {e}")
        return False


# ──────────────────────────────────────────────
# PRUEBAS
# ──────────────────────────────────────────────

if __name__ == '__main__':
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║   Analizador Descendente Recursivo — Función parea (matching)    ║")
    print("╚══════════════════════════════════════════════════════════════╝\n")

    VALIDOS = [
        "x = 5",
        "x = 5 + 3",
        "x = a + b * 2",
        "x = (a + b) * c",
        "if (a > b) then x = 10",
        "if (a > b) then x = 10 else y = 20",
        "if (x >= 5) then y = x * 2 else y = 0",
        "a = 1; b = 2; c = 3",
        "if (a == b) then x = 1 else if (a != b) then x = 2 else x = 3",
    ]

    INVALIDOS = [
        "x =",
        "= 5",
        "if (a > b) then",
        "if a > b then x = 10",
        "x = 5 +",
        "x = 5 + * 3",
    ]

    print("── Casos VÁLIDOS ─────────────────────────────────────────────")
    all_ok = True
    for c in VALIDOS:
        print(f"\n  '{c}'")
        ok = analizar(c)
        if not ok:
            all_ok = False

    print("\n── Casos INVÁLIDOS ───────────────────────────────────────────")
    for c in INVALIDOS:
        print(f"\n  '{c}'")
        analizar(c)

    print("\n── PRUEBA DEL PARCIAL ────────────────────────────────────────")
    cadena_parcial = "if (a > b) then x = 10 else y = 20"
    print(f"\n  Analizando: '{cadena_parcial}'")
    analizar(cadena_parcial)

    print("\n── RESUMEN ───────────────────────────────────────────────────")
    print(f"  Analizador descendente recursivo: {'OK' if all_ok else 'con errores'}")
    print("  Función parea implementada con manejo de errores detallado.")
