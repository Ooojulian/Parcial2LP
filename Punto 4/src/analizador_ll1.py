"""
LL(1) Recursive Descent para Expresiones Aritméticas
Top-down, predictive análisis sintáctico algorithm
Complejidad Temporal: O(n)
Space Complexity: O(n) call stack
"""

import time
from typing import List, Tuple

class LL1Analizador:
    """
    LL(1) Recursive Descent Analizador for calculator expressions
    
    Grammar (without left recursion):
        E    → T E'
        E'   → + T E' | - T E' | ε
        T    → F T'
        T'   → * F T' | / F T' | ε
        F    → ( E ) | num
    
    This grammar is:
    - Left-factored (no ambiguity)
    - No left recursion
    - LL(1)-parseable with 1-token preanalisis
    """
    
    def __init__(self):
        """Inicializar LL(1) analizador"""
        self.tokens = []
        self.pos = 0
    
    def tokenize(self, expr: str) -> List[str]:
        """Convert expression to tokens"""
        tokens = []
        i = 0
        while i < len(expr):
            if expr[i].isspace():
                i += 1
            elif expr[i].isdigit():
                j = i
                while j < len(expr) and expr[j].isdigit():
                    j += 1
                tokens.append(expr[i:j])
                i = j
            elif expr[i] in '+-*/()':
                tokens.append(expr[i])
                i += 1
            else:
                raise ValueError(f"Unknown character: {expr[i]}")
        return tokens
    
    def current_token(self) -> str:
        """Get current token without consuming"""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return '$'  # EOF marker
    
    def consume(self, expected: str = None) -> str:
        """Consume and return current token"""
        if self.pos >= len(self.tokens):
            raise SyntaxError(f"Unexpected EOF, expected {expected}")
        
        token = self.tokens[self.pos]
        if expected and token != expected:
            raise SyntaxError(f"Expected {expected}, got {token}")
        
        self.pos += 1
        return token
    
    def parse(self, expr: str) -> Tuple[bool, float]:
        """
        Parse expression using recursive descent LL(1)
        Returns (success, parse_time)
        """
        start_time = time.time()
        
        try:
            self.tokens = self.tokenize(expr)
            self.pos = 0
            
            if len(self.tokens) == 0:
                return False, time.time() - start_time
            
            self.E()
            
            # Check for EOF
            if self.current_token() != '$':
                return False, time.time() - start_time
            
            return True, time.time() - start_time
            
        except (SyntaxError, ValueError):
            return False, time.time() - start_time
    
    def E(self) -> float:
        """E → T E'"""
        val = self.T()
        return self.E_prime(val)

    def E_prime(self, izq: float) -> float:
        """E' → + T E' | - T E' | ε"""
        if self.current_token() == '+':
            self.consume('+')
            der = self.T()
            return self.E_prime(izq + der)
        elif self.current_token() == '-':
            self.consume('-')
            der = self.T()
            return self.E_prime(izq - der)
        return izq  # ε

    def T(self) -> float:
        """T → F T'"""
        val = self.F()
        return self.T_prime(val)

    def T_prime(self, izq: float) -> float:
        """T' → * F T' | / F T' | ε"""
        if self.current_token() == '*':
            self.consume('*')
            der = self.F()
            return self.T_prime(izq * der)
        elif self.current_token() == '/':
            self.consume('/')
            der = self.F()
            if der == 0:
                raise ZeroDivisionError("División por cero")
            return self.T_prime(izq / der)
        return izq  # ε

    def F(self) -> float:
        """F → ( E ) | num"""
        if self.current_token() == '(':
            self.consume('(')
            val = self.E()
            self.consume(')')
            return val
        else:
            tok = self.consume()
            return float(tok)
    
    def evaluar(self, expr: str) -> Tuple[bool, float, float]:
        """
        Evalúa la expresión y retorna el resultado numérico.
        Returns (success, resultado, tiempo)
        """
        start_time = time.time()
        try:
            self.tokens = self.tokenize(expr)
            self.pos = 0
            if len(self.tokens) == 0:
                return False, 0.0, time.time() - start_time
            resultado = self.E()
            if self.current_token() != '$':
                return False, 0.0, time.time() - start_time
            return True, resultado, time.time() - start_time
        except (SyntaxError, ValueError, ZeroDivisionError) as e:
            return False, 0.0, time.time() - start_time

    def parse_verbose(self, expr: str) -> dict:
        """Parse with detailed output"""
        try:
            self.tokens = self.tokenize(expr)
            self.pos = 0
            self.E()
            if self.current_token() != '$':
                return {'expr': expr, 'success': False, 'error': 'Extra tokens'}
            return {'expr': expr, 'success': True}
        except Exception as e:
            return {'expr': expr, 'success': False, 'error': str(e)}


if __name__ == '__main__':
    analizador = LL1Analizador()
    
    # Casos de prueba
    test_cases = [
        "2",
        "2 + 3",
        "2 + 3 * 4",
        "( 2 + 3 ) * 4",
        "10 - 5 / 2",
    ]
    
    print("=== LL(1) Analizador Test ===\n")
    for expr in test_cases:
        success, elapsed = analizador.parse(expr)
        status = "✓ ACCEPT" if success else "✗ REJECT"
        print(f"{status}: {expr:30} ({elapsed*1000:.4f}ms)")

