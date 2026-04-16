#!/usr/bin/env python3
"""
Punto 3 — Demostración de ambigüedad y desambiguación
Corre ambos parsers (ambigua y desambigua) sobre los mismos casos
y muestra los conflictos detectados por Bison.
"""
import subprocess
import sys
from pathlib import Path

class C:
    GREEN  = '\033[92m'
    FAIL   = '\033[91m'
    CYAN   = '\033[96m'
    YELLOW = '\033[93m'
    BOLD   = '\033[1m'
    END    = '\033[0m'

CASOS = [
    ("i E t i E t s e s", "if E then if E then S else S  ← caso principal"),
    ("i E t s",            "if E then S                   ← sin else"),
    ("i E t s e s",        "if E then S else S             ← completo"),
    ("i E t i E t i E t s e s", "triple anidado"),
]

def run(binary, entrada):
    try:
        r = subprocess.run([binary], input=entrada, capture_output=True, text=True, timeout=5)
        return r.returncode == 0, r.stdout, r.stderr
    except Exception as e:
        return False, "", str(e)

def conflictos(output_file):
    try:
        txt = Path(output_file).read_text()
        lineas = [l for l in txt.splitlines() if 'conflicto' in l.lower() or 'conflict' in l.lower()]
        return lineas[0] if lineas else "sin conflictos"
    except:
        return "archivo no encontrado"

def main():
    ambigua   = Path("build/ambigua")
    desambigua = Path("build/desambigua")

    if not ambigua.exists() or not desambigua.exists():
        print(f"{C.FAIL}✗ Binarios no encontrados. Ejecuta 'make' primero.{C.END}")
        return 1

    # Reporte de conflictos Bison
    print(f"\n{C.BOLD}=== REPORTE DE CONFLICTOS BISON ==={C.END}\n")
    print(f"  ambigua.y    → {C.YELLOW}{conflictos('build/ambigua.output')}{C.END}")
    print(f"  desambigua.y → {C.GREEN}{conflictos('build/desambigua.output')}{C.END}\n")

    # Pruebas comparativas
    print(f"{C.BOLD}=== PRUEBAS COMPARATIVAS ==={C.END}\n")
    exitoso = 0
    total   = len(CASOS)

    for entrada, desc in CASOS:
        ok_a, out_a, _ = run(str(ambigua),    entrada)
        ok_d, out_d, _ = run(str(desambigua), entrada)

        estado = f"{C.GREEN}✓{C.END}" if (ok_a and ok_d) else f"{C.FAIL}✗{C.END}"
        if ok_a and ok_d:
            exitoso += 1

        print(f"{estado} {C.BOLD}{desc}{C.END}")
        print(f"    Entrada : {C.CYAN}{entrada}{C.END}")

        # Muestra líneas relevantes del parser desambiguado
        lineas = [l.strip() for l in out_d.splitlines()
                  if any(x in l for x in ['Reduce:', 'MATCHED', 'WITHOUT'])]
        for l in lineas:
            print(f"    {C.CYAN}{l}{C.END}")
        print()

    print(f"{C.BOLD}{'─'*50}")
    print(f"Resultado: {C.GREEN}{exitoso}/{total} exitosos{C.END}{C.BOLD}")
    print(f"{'─'*50}{C.END}\n")
    return 0 if exitoso == total else 1

if __name__ == "__main__":
    sys.exit(main())
