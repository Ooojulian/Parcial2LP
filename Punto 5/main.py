#!/usr/bin/env python3
"""
Punto 5 — Analizador descendente recursivo con función parea
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))
from analizador_descendente import analizar

class C:
    GREEN  = '\033[92m'
    FAIL   = '\033[91m'
    CYAN   = '\033[96m'
    BOLD   = '\033[1m'
    END    = '\033[0m'

def correr(expresiones, esperado_ok):
    exitoso = 0
    for expr in expresiones:
        expr = expr.strip()
        if not expr or expr.startswith('#'):
            continue
        try:
            ok = analizar(expr, verbose=False)
        except Exception:
            ok = False

        if esperado_ok:
            bien = ok
            estado = f"{C.GREEN}✓ ACEPTADO{C.END}" if bien else f"{C.FAIL}✗ RECHAZADO (error){C.END}"
        else:
            bien = not ok
            estado = f"{C.GREEN}✓ RECHAZADO{C.END}" if bien else f"{C.FAIL}✗ ACEPTADO (error){C.END}"

        if bien:
            exitoso += 1
        print(f"  {estado}  {C.CYAN}{expr}{C.END}")

    return exitoso

def main():
    validos   = Path("pruebas/validos.txt").read_text().splitlines()
    invalidos = Path("pruebas/invalidos.txt").read_text().splitlines()

    print(f"\n{C.BOLD}=== PUNTO 5 — ANALIZADOR DESCENDENTE RECURSIVO ==={C.END}\n")

    print(f"{C.BOLD}Casos válidos:{C.END}\n")
    ok_v = correr(validos, esperado_ok=True)
    total_v = len([l for l in validos if l.strip() and not l.startswith('#')])

    print(f"\n{C.BOLD}Casos inválidos (deben ser rechazados):{C.END}\n")
    ok_i = correr(invalidos, esperado_ok=False)
    total_i = len([l for l in invalidos if l.strip() and not l.startswith('#')])

    total   = total_v + total_i
    exitoso = ok_v + ok_i

    print(f"\n{C.BOLD}{'─'*50}")
    print(f"Resultado: {C.GREEN}{exitoso}/{total} exitosos{C.END}{C.BOLD}")
    print(f"{'─'*50}{C.END}\n")
    return 0 if exitoso == total else 1

if __name__ == "__main__":
    sys.exit(main())
