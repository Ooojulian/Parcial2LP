#!/usr/bin/env python3
"""
Punto 4 — Comparación CYK vs LL(1) para expresiones aritméticas
Corre ambos parsers sobre los mismos casos y compara tiempos.
"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))
from analizador_cyk import CYKAnalizador
from analizador_ll1 import LL1Analizador

class C:
    GREEN  = '\033[92m'
    FAIL   = '\033[91m'
    CYAN   = '\033[96m'
    YELLOW = '\033[93m'
    BOLD   = '\033[1m'
    END    = '\033[0m'

def cargar_casos(path="pruebas/casos.txt"):
    casos = []
    for line in Path(path).read_text().splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        partes = line.split('|')
        expr, desc, esperado = partes[0], partes[1], partes[2]
        casos.append((expr, desc, esperado == "PASS"))
    return casos

def main():
    cyk = CYKAnalizador()
    ll1 = LL1Analizador()
    casos = cargar_casos()

    validos   = [(e, d, esp) for e, d, esp in casos if esp]
    invalidos = [(e, d, esp) for e, d, esp in casos if not esp]

    print(f"\n{C.BOLD}=== PUNTO 4 — CYK vs LL(1) ==={C.END}\n")

    exitoso = 0
    total   = len(casos)

    # ── Casos válidos con resultado calculado ──
    print(f"{C.BOLD}Casos válidos (con resultado calculado por LL(1)):{C.END}\n")
    print(f"  {'Expresión':<35} {'Resultado':>10} {'LL(1)':>10} {'CYK':>10}  {'Ratio':>8}")
    print(f"  {'─'*35} {'─'*10} {'─'*10} {'─'*10}  {'─'*8}")

    for expr, desc, _ in validos:
        ok_ll, resultado, t_ll = ll1.evaluar(expr)
        ok_cy, t_cy            = cyk.parse(expr)
        ok = ok_ll and ok_cy
        if ok:
            exitoso += 1
        ratio  = f"{t_cy/t_ll:.1f}x" if t_ll > 0 else "—"
        estado = f"{C.GREEN}✓{C.END}" if ok else f"{C.FAIL}✗{C.END}"
        res_str = f"= {resultado:g}" if ok_ll else "ERROR"
        print(f"  {estado} {expr:<33} {C.CYAN}{res_str:>10}{C.END} {t_ll*1000:>8.4f}ms {t_cy*1000:>8.4f}ms  {C.CYAN}{ratio:>8}{C.END}")

    # ── Casos inválidos ──
    print(f"\n{C.BOLD}Casos inválidos (deben ser rechazados):{C.END}\n")
    for expr, desc, _ in invalidos:
        ok_ll, _ = ll1.parse(expr)
        ok_cy, _ = cyk.parse(expr)
        rechazado = (not ok_ll) and (not ok_cy)
        if rechazado:
            exitoso += 1
        estado = f"{C.GREEN}✓ RECHAZADO{C.END}" if rechazado else f"{C.FAIL}✗ ACEPTADO (error){C.END}"
        print(f"  {estado}  {expr}  ({desc})")

    # ── Rendimiento escalado ──
    print(f"\n{C.BOLD}Rendimiento con expresiones más largas:{C.END}\n")
    print(f"  {'Tokens':<10} {'LL(1)':>10} {'CYK':>10}  {'CYK/LL(1)':>10}")
    print(f"  {'─'*10} {'─'*10} {'─'*10}  {'─'*10}")

    base = "2 + 3"
    for n in [1, 3, 5, 7, 10]:
        expr = " + ".join(["( " + base + " )"] * n)
        _, t_ll = ll1.parse(expr)
        _, t_cy = cyk.parse(expr)
        tokens = len(expr.split())
        ratio = f"{t_cy/t_ll:.1f}x" if t_ll > 0 else "—"
        print(f"  {tokens:<10} {t_ll*1000:>8.4f}ms {t_cy*1000:>8.4f}ms  {C.CYAN}{ratio:>10}{C.END}")

    print(f"\n{C.BOLD}{'─'*50}")
    print(f"Resultado: {C.GREEN}{exitoso}/{total} exitosos{C.END}{C.BOLD}")
    print(f"{'─'*50}{C.END}\n")
    return 0 if exitoso == total else 1

if __name__ == "__main__":
    sys.exit(main())
