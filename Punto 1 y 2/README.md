# Puntos 1 y 2 — CRUD para BD No Relacional

Lenguaje de consultas con operaciones CRUD sobre documentos JSON. Implementado con Bison/Flex (C).

## Gramática

```
S → Stmt S | Stmt

Stmt → CreateStmt | ReadStmt | UpdateStmt | DeleteStmt

CreateStmt → "INSERT" "INTO" id Doc
ReadStmt   → "FIND"   "FROM" id OptFilter
UpdateStmt → "UPDATE" id "SET" Doc OptFilter
DeleteStmt → "DELETE" "FROM" id OptFilter

OptFilter  → "WHERE" Condition | ε
Condition  → string Operator Value
Operator   → "=" | "<" | ">"

Doc      → "{" Members "}" | "{" "}"
Members  → Pair "," Members | Pair
Pair     → string ":" Value
Value    → string | number | boolean | Doc | Array
Array    → "[" Elements "]" | "[" "]"
Elements → Value "," Elements | Value
```

## Ejemplos de uso

```
INSERT INTO usuarios {"nombre": "Ana", "edad": 25, "activo": true}

FIND FROM usuarios WHERE "nombre" = "Ana"

UPDATE usuarios SET {"edad": 26} WHERE "nombre" = "Ana"

DELETE FROM usuarios WHERE "activo" = false
```

## Estructura

```
Punto 1 y 2/
├── src/
│   └── bison/          # lexer.l, parser.y, main.c
├── pruebas/            # casos de prueba .lang
├── build/              # binarios compilados
├── Makefile
├── main.py
├── README.md
├── CONCEPTOS.md
└── SOLUCION.md
```

## Compilar y ejecutar

```bash
# Prerrequisitos
sudo apt-get install bison flex gcc

# Compilar
make

# Ejecutar parser
./build/bison_parser pruebas/casos/crear_valido.lang

# Correr todas las pruebas
python3 main.py
```
