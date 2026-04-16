# Conceptos — Diseño de la Gramática

## ¿Por qué esta gramática?

BD no relacionales (MongoDB, CouchDB) operan sobre documentos JSON. La gramática modela exactamente eso: operaciones CRUD donde el "qué" es un documento y el "dónde" es un filtro simple.

## Clasificación

| Propiedad | Valor |
|-----------|-------|
| Tipo | Libre de contexto (CFG) |
| Ambigüedad | No ambigua |
| Conflictos | Ninguno (0 shift/reduce, 0 reduce/reduce) |
| Complejidad | O(n) |
| Compatible con | LALR(1) — Bison |

## Decisiones de diseño

**Sintaxis de operaciones:**
- `INSERT INTO` / `FIND FROM` / `UPDATE ... SET` / `DELETE FROM` — deliberadamente cercana a SQL para legibilidad, pero sin JOINs ni subconsultas (BD no relacional no los necesita).

**Documentos JSON:**
- `Doc → "{" Members "}"` permite anidamiento arbitrario y arreglos. Refleja el modelo de datos real de una BD documental.

**Filtro opcional (`OptFilter → ε`):**
- `FIND FROM tabla` sin WHERE es válido — retorna todos los documentos. Común en BD no relacionales.

**Condición simple (`Condition → string Operator Value`):**
- Un solo predicado por consulta. Suficiente para demostrar el lenguaje sin complejidad de AND/OR.

## Tokens del léxico

| Token | Patrón |
|-------|--------|
| Palabras clave | `INSERT`, `INTO`, `FIND`, `FROM`, `UPDATE`, `SET`, `DELETE`, `WHERE` |
| STRING | `"..."` o `'...'` |
| NUMBER | entero o flotante |
| BOOLEAN | `true` \| `false` |
| ID | `[a-zA-Z_][a-zA-Z0-9_]*` |
| Símbolos | `{ } [ ] : , = < >` |

## Parser: Bison/Flex

| Aspecto | Detalle |
|---------|---------|
| Estrategia | Bottom-up (LALR) |
| Lenguaje | C |
| Archivos | `lexer.l` (Flex) + `parser.y` (Bison) |
| Lookahead | 1 token |
| Generación | `bison -d parser.y` + `flex lexer.l` + `gcc` |
