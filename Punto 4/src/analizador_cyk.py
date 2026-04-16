"""
CYK (Cocke-Younger-Kasami) para Expresiones Aritméticas
Complejidad Temporal: O(n³)
"""

import time
from typing import List, Tuple, Set, Dict
from collections import defaultdict

class CYKAnalizador:
    """
    Analizador CYK simplificado para expresiones aritméticas
    
    Terminales: digitos, +, -, *, /, (, )
    No terminales: E, T, F
    
    CFG simplificada (sin precedencia completa):
        E → T | E + T | E - T
        T → F | T * F | T / F
        F → num | ( E )
    """
    
    def __init__(self):
        """Inicializar analizador CYK con gramática"""
        # Variables
        self.variables = {'E', 'T', 'F', 'DIGIT', 'OP_ADD', 'OP_MUL', 'LPAREN', 'RPAREN'}
        
        # Reglas terminales: variable -> token
        self.terminal_rules = {
            'DIGIT':  ['NUM'],   # número (cualquier entero)
            'OP_ADD': ['+', '-'],
            'OP_MUL': ['*', '/'],
            'LPAREN': ['('],
            'RPAREN': [')'],
        }
        
        # Reglas no terminales en CNF: A → B C  o  A → B (regla de unidad)
        self.nonterminal_rules = {
            # F → num  |  ( E )
            'F': [
                ('DIGIT', None),         # F → DIGIT
                ('LPAREN', 'E_CLOSE'),   # F → ( E_CLOSE    donde E_CLOSE = E )
            ],
            # E_CLOSE → E )
            'E_CLOSE': [
                ('E', 'RPAREN'),
            ],
            # T → F  |  T * F  |  T / F
            'T': [
                ('F', None),             # T → F
                ('T', 'MUL_RIGHT'),      # T → T (MUL_RIGHT = * F)
            ],
            # MUL_RIGHT → OP_MUL F
            'MUL_RIGHT': [
                ('OP_MUL', 'F'),
            ],
            # E → T  |  E + T  |  E - T
            'E': [
                ('T', None),             # E → T
                ('E', 'ADD_RIGHT'),      # E → E (ADD_RIGHT = +/- T)
            ],
            # ADD_RIGHT → OP_ADD T
            'ADD_RIGHT': [
                ('OP_ADD', 'T'),
            ],
        }
        
        # Búsqueda inversa
        self.token_to_vars = defaultdict(set)
        for var, tokens in self.terminal_rules.items():
            for token in tokens:
                self.token_to_vars[token].add(var)
    
    def tokenize(self, expr: str) -> List[str]:
        """Tokenizar expresión — números multi-dígito como un solo token NUM"""
        tokens = []
        i = 0
        while i < len(expr):
            if expr[i].isspace():
                i += 1
            elif expr[i].isdigit():
                j = i
                while j < len(expr) and expr[j].isdigit():
                    j += 1
                tokens.append('NUM')   # número → token genérico NUM
                i = j
            elif expr[i] in '+-*/()':
                tokens.append(expr[i])
                i += 1
            else:
                raise ValueError(f"Carácter desconocido: {expr[i]}")
        return tokens
    
    def _propagar_unidades(self, cell: set):
        """Propaga reglas de unidad A → B en una celda hasta punto fijo."""
        changed = True
        while changed:
            changed = False
            for var, rules in self.nonterminal_rules.items():
                for (B, C) in rules:
                    if C is None and B in cell and var not in cell:
                        cell.add(var)
                        changed = True

    def parse(self, expr: str) -> Tuple[bool, float]:
        """Analizar usando algoritmo CYK — O(n³)"""
        start_time = time.time()
        try:
            tokens = self.tokenize(expr)
            n = len(tokens)
            if n == 0:
                return False, time.time() - start_time

            # chart[i][j] = variables que derivan tokens[i..j]
            chart = [[set() for _ in range(n)] for _ in range(n)]

            # Paso 1: diagonal — tokens individuales
            for i in range(n):
                tok = tokens[i]
                if tok in self.token_to_vars:
                    chart[i][i].update(self.token_to_vars[tok])
                self._propagar_unidades(chart[i][i])

            # Paso 2: substrings de longitud 2..n
            for length in range(2, n + 1):
                for i in range(n - length + 1):
                    j = i + length - 1
                    for k in range(i, j):
                        lv = chart[i][k]
                        rv = chart[k + 1][j]
                        for var, rules in self.nonterminal_rules.items():
                            for (B, C) in rules:
                                if C and B in lv and C in rv:
                                    chart[i][j].add(var)
                    self._propagar_unidades(chart[i][j])

            success = 'E' in chart[0][n - 1]
            return success, time.time() - start_time
        except Exception:
            return False, time.time() - start_time


if __name__ == '__main__':
    analizador = CYKAnalizador()
    
    test_cases = [
        "2",
        "2+3",
        "2+3*4",
        "(2+3)*4",
        "10-5/2",
    ]
    
    print("=== CYK Analizador Test ===\n")
    for expr in test_cases:
        success, elapsed = analizador.parse(expr)
        status = "✓ ACCEPT" if success else "✗ REJECT"
        print(f"{status}: {expr:30} ({elapsed*1000:.4f}ms)")

