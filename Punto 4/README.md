# Punto 4 — CYK vs LL(1) para Calculadora

## Enunciado

> Implemente un parser usando el algoritmo CYK para realizar las operaciones de una calculadora. Realice pruebas sobre el rendimiento de este algoritmo comparándolo con un parser de tipo predictivo. Realice una comparación entre el rendimiento de los dos parsers.

## Resultado

| Parser | Complejidad | Ejemplo `2 + 3 * 4` |
|--------|------------|----------------------|
| CYK | O(n³) | ~0.07ms |
| LL(1) | O(n) | ~0.007ms |

A 59 tokens: LL(1) es **~690x más rápido**.

## Estructura

```
Punto 4/
├── src/
│   ├── analizador_cyk.py    # Parser CYK — O(n³)
│   └── analizador_ll1.py    # Parser LL(1) — O(n)
├── pruebas/
│   └── casos.txt            # Casos válidos e inválidos
├── main.py                  # Corre pruebas y comparación de rendimiento
├── README.md
├── CONCEPTOS.md
└── SOLUCION.md
```

## Ejecutar

```bash
# Sin dependencias externas
python3 main.py
```
