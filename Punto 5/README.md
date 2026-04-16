# Punto 5 — Analizador Descendente Recursivo

## Enunciado

> Diseñe e implemente un algoritmo de emparejamiento para el algoritmo descendente recursivo. Para probar, diseñe una gramática que pueda hacer operaciones de asignación y operaciones de condicionales.

## Resultado

Parser descendente recursivo con función `parea()` implementada. Soporta:

- Asignaciones: `x = 5 + 3`
- Condicionales: `if (a > b) then x = 10 else y = 20`
- Expresiones aritméticas con precedencia: `+`, `-`, `*`, `/`
- Operadores relacionales: `>`, `<`, `>=`, `<=`, `==`, `!=`

## Estructura

```
Punto 5/
├── src/
│   └── analizador_descendente.py   # Parser + función parea()
├── pruebas/
│   ├── validos.txt                 # Casos que deben aceptarse
│   └── invalidos.txt               # Casos que deben rechazarse
├── main.py                         # Corre todas las pruebas
├── README.md
├── CONCEPTOS.md
└── SOLUCION.md
```

## Ejecutar

```bash
python3 main.py
```
