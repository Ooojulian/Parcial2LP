# Parcial 2 — Lenguajes de Programación 2026

---

## Estructura

```
Parcial2LP/
├── Punto 1 y 2/   Gramática CRUD + parser Bison
├── Punto 3/       Ambigüedad if-then-else y desambiguación
├── Punto 4/       CYK vs LL(1) — comparación de rendimiento
└── Punto 5/       Algoritmo de emparejamiento parea() — descendente recursivo
```

---

## Punto 1 y 2 — Gramática CRUD (Bison)

Gramática para operaciones CRUD sobre una base de datos NO relacional con documentos JSON.

```bash
cd "Punto 1 y 2"
make all
python3 main.py
# 9/9 exitosos (6 válidos + 3 inválidos)
```

---

## Punto 3 — Ambigüedad if-then-else

Demuestra que la gramática propuesta en el parcial sigue siendo ambigua (conflicto shift/reduce),
y la resuelve mediante estratificación en gramática emparejada/no-emparejada.

```bash
cd "Punto 3"
make all
python3 main.py
# Ambigua: 1 conflicto shift/reduce
# Desambiguada: 0 conflictos
```

---

## Punto 4 — CYK vs LL(1)

Implementación de ambos parsers para expresiones aritméticas. Comparación experimental
de rendimiento que confirma O(n³) vs O(n).

```bash
cd "Punto 4"
python3 main.py
# Tabla de tiempos + ratio CYK/LL(1)
```

| Tokens | LL(1) | CYK | Ratio |
|--------|-------|-----|-------|
| 5 | ~0.005ms | ~0.03ms | 6x |
| 29 | ~0.02ms | ~3ms | 161x |
| 59 | ~0.06ms | ~24ms | 380x |

---

## Punto 5 — Algoritmo de emparejamiento (parea)

Implementación del algoritmo descendente recursivo con función `parea()`.
Gramática LL(1) para asignaciones y condicionales.

```bash
cd "Punto 5"
python3 main.py
# 13/13 exitosos (8 válidos + 5 inválidos)
```

Soporta:
- Asignaciones: `x = 5 + 3 * 2`
- Condicionales: `if (a > b) then x = 10 else y = 20`
- If-then-else anidado
- Expresiones con precedencia correcta (`*` antes que `+`)

---

## Resultados

| Punto | Resultado |
|-------|-----------|
| 1 y 2 | 9/9 pruebas — gramática CRUD Bison |
| 3 | Ambigüedad demostrada y resuelta |
| 4 | LL(1) hasta 380x más rápido que CYK |
| 5 | 13/13 pruebas — parea() implementado |
