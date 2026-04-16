#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

class Colors:
    OKGREEN = '\033[92m'
    FAIL    = '\033[91m'
    CYAN    = '\033[96m'
    BOLD    = '\033[1m'
    ENDC    = '\033[0m'

def run_test(parser_path, test_file):
    try:
        result = subprocess.run(
            [parser_path, test_file],
            capture_output=True, text=True, timeout=5
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def main():
    parser  = Path("build/bison_parser")
    test_dir = Path("pruebas/casos")

    if not parser.exists():
        print(f"{Colors.FAIL}✗ Parser no encontrado. Ejecuta 'make' primero.{Colors.ENDC}")
        return 1

    tests = sorted(test_dir.glob("*.lang"))
    if not tests:
        print(f"{Colors.FAIL}✗ No se encontraron casos de prueba en {test_dir}{Colors.ENDC}")
        return 1

    validos  = [t for t in tests if not t.stem.startswith("error_")]
    invalidos = [t for t in tests if t.stem.startswith("error_")]

    exitoso = 0
    fallo   = 0

    print(f"\n{Colors.BOLD}=== CASOS VÁLIDOS ==={Colors.ENDC}\n")
    for test_file in validos:
        success, stdout, stderr = run_test(str(parser), str(test_file))
        # válido debe pasar (exit 0)
        ok = success
        estado = f"{Colors.OKGREEN}✓ PASS{Colors.ENDC}" if ok else f"{Colors.FAIL}✗ FAIL{Colors.ENDC}"
        print(f"{estado}  {Colors.BOLD}{test_file.stem}{Colors.ENDC}")
        if ok:
            exitoso += 1
            for line in stdout.split('\n'):
                if any(x in line for x in ['✓', 'INSERT', 'FIND', 'UPDATE', 'DELETE']):
                    print(f"       {Colors.CYAN}{line}{Colors.ENDC}")
        else:
            fallo += 1
            print(f"       {Colors.FAIL}{stderr[:200]}{Colors.ENDC}")
        print()

    print(f"\n{Colors.BOLD}=== CASOS INVÁLIDOS (deben ser rechazados) ==={Colors.ENDC}\n")
    for test_file in invalidos:
        success, stdout, stderr = run_test(str(parser), str(test_file))
        # inválido debe fallar (exit 1)
        ok = not success
        estado = f"{Colors.OKGREEN}✓ RECHAZADO{Colors.ENDC}" if ok else f"{Colors.FAIL}✗ ACEPTADO (error){Colors.ENDC}"
        print(f"{estado}  {Colors.BOLD}{test_file.stem}{Colors.ENDC}")
        if ok:
            exitoso += 1
            print(f"       {Colors.CYAN}{stderr.strip()}{Colors.ENDC}")
        else:
            fallo += 1
        print()

    total = exitoso + fallo
    print(f"{Colors.BOLD}{'─'*40}")
    print(f"Resultado: {Colors.OKGREEN}{exitoso} exitosos{Colors.ENDC}{Colors.BOLD}, {Colors.FAIL}{fallo} fallidos{Colors.ENDC}{Colors.BOLD}, {total} total")
    print(f"{'─'*40}{Colors.ENDC}\n")

    return 0 if fallo == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
