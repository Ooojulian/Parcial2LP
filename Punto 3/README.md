# Punto 3 — Ambigüedad en Gramáticas IF-THEN-ELSE

## Enunciado

Se propone la gramática:

```
prop             → if expr then prop
                 | prop_emparejada

prop_emparejada  → if expr then prop_emparejada else prop
                 | otras
```

Demostrar que sigue siendo ambigua. Si lo es, desambiguarla.

## Resultado

| Gramática | Conflictos Bison | Ambigua |
|-----------|-----------------|---------|
| `ambigua.y` | 1 shift/reduce | Sí |
| `desambigua.y` | 0 | No |

## Estructura

```
Punto 3/
├── ambigua.y       # Gramática original con conflicto
├── desambigua.y    # Gramática desambiguada por estratificación
├── Makefile
├── README.md
├── CONCEPTOS.md
└── SOLUCION.md
```

## Compilar y probar

```bash
# Compilar ambas
make all

# Correr prueba principal
echo "i E t i E t s e s" | ./build/ambigua
echo "i E t i E t s e s" | ./build/desambigua

# Ver reporte de conflictos
make report
```

La entrada `i E t i E t s e s` representa: `if E then if E then stmt else stmt`
