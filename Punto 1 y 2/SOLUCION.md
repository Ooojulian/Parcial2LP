# Punto 2 — Implementación de la Gramática en Bison

## Enunciado

> Implemente la gramática del punto 1 en BISON o ANTLR y realice pruebas sobre el lenguaje.

La gramática diseñada en el punto 1 se encuentra en [`Gramatica inicial.txt`](Gramatica%20inicial.txt).

---

## Implementación: Bison/Flex

Se utilizó **Bison** (parser LALR) + **Flex** (lexer) sobre C.

| Archivo | Rol |
|---------|-----|
| `src/bison/lexer.l` | Tokenizador: palabras clave, strings, números, booleanos, símbolos |
| `src/bison/parser.y` | Reglas gramaticales LALR(1) con acciones semánticas |
| `src/bison/main.c` | Entrada: lee archivo, invoca `yyparse()`, reporta resultado |

### Compilar

```bash
bison -d src/bison/parser.y      # genera parser.tab.c / parser.tab.h
flex src/bison/lexer.l           # genera lexer.yy.c
gcc parser.tab.c lexer.yy.c src/bison/main.c -o build/bison_parser
```

---

## Pruebas realizadas

Se ejecutaron 6 casos de prueba con el parser Bison. Todos pasaron exitosamente.

---

### Caso 1 — CREATE simple (`crear_valido.lang`)

**Entrada:**
```
INSERT INTO users {"name": "Alice", "age": 30, "active": true}
```

**Salida:**
```
=== Language Parser (Bison) ===
Parsing input...

        value: string
      field: "name"
        value: number
      field: "age"
        value: boolean
      field: "active"
  INSERT INTO 'users'
✓ CREATE statement

✓ Parse successful
```

---

### Caso 2 — READ con WHERE (`leer_valido.lang`)

**Entrada:**
```
FIND FROM users WHERE "status" = "active"
```

**Salida:**
```
=== Language Parser (Bison) ===
Parsing input...

      operator: =
        value: string
    condition: "status"
    with WHERE clause
  FIND FROM 'users'
✓ READ statement

✓ Parse successful
```

---

### Caso 3 — UPDATE con filtro (`actualizar_valido.lang`)

**Entrada:**
```
UPDATE users SET {"status": "inactive"} WHERE "id" = "123"
```

**Salida:**
```
=== Language Parser (Bison) ===
Parsing input...

        value: string
      field: "status"
      operator: =
        value: string
    condition: "id"
    with WHERE clause
  UPDATE 'users'
✓ UPDATE statement

✓ Parse successful
```

---

### Caso 4 — DELETE con filtro (`borrar_valido.lang`)

**Entrada:**
```
DELETE FROM users WHERE "age" < "18"
```

**Salida:**
```
=== Language Parser (Bison) ===
Parsing input...

      operator: <
        value: string
    condition: "age"
    with WHERE clause
  DELETE FROM 'users'
✓ DELETE statement

✓ Parse successful
```

---

### Caso 5 — Documento complejo + múltiples sentencias (`documento_complejo.lang`)

**Entrada:**
```
INSERT INTO users {
  "name": "Bob",
  "profile": {
    "email": "bob@example.com",
    "verified": true
  },
  "tags": ["admin", "developer"]
}
INSERT INTO products {"sku": "SKU-001", "price": 99.99}
UPDATE products SET {"stock": 50} WHERE "sku" = "SKU-001"
```

**Salida:**
```
=== Language Parser (Bison) ===
Parsing input...

        value: string
      field: "name"
        value: string
      field: "email"
        value: boolean
      field: "verified"
        value: document
      field: "profile"
        value: string
        value: string
        value: array
      field: "tags"
  INSERT INTO 'users'
✓ CREATE statement
        value: string
      field: "sku"
        value: number
      field: "price"
  INSERT INTO 'products'
✓ CREATE statement
        value: number
      field: "stock"
      operator: =
        value: string
    condition: "sku"
    with WHERE clause
  UPDATE 'products'
✓ UPDATE statement

✓ Parse successful
```

---

### Caso 6 — Arreglos anidados + doc complejo (`arreglos_anidados.lang`)

**Entrada:**
```
INSERT INTO matrix {"data": [1, 2, 3], "nested": {"values": [true, false, true]}}
FIND FROM matrix WHERE "count" > "5"
```

**Salida:**
```
=== Language Parser (Bison) ===
Parsing input...

        value: number
        value: number
        value: number
        value: array
      field: "data"
        value: boolean
        value: boolean
        value: boolean
        value: array
      field: "values"
        value: document
      field: "nested"
  INSERT INTO 'matrix'
✓ CREATE statement
      operator: >
        value: string
    condition: "count"
    with WHERE clause
  FIND FROM 'matrix'
✓ READ statement

✓ Parse successful
```

---

---

### Caso 7 — INSERT sin documento (`error_insert_sin_documento.lang`)

**Entrada:**
```
INSERT INTO usuarios
```

**Salida:**
```
ERROR: syntax error
✗ Parse failed
```

El parser rechaza la sentencia porque `CreateStmt` requiere obligatoriamente un `Doc` después del identificador de tabla.

---

### Caso 8 — FIND sin nombre de tabla (`error_find_sin_tabla.lang`)

**Entrada:**
```
FIND FROM WHERE "campo" = "valor"
```

**Salida:**
```
ERROR: syntax error
✗ Parse failed
```

`WHERE` es una palabra reservada, no un identificador válido para nombre de tabla. La regla `ReadStmt → FIND FROM id OptFilter` lo rechaza.

---

### Caso 9 — Documento con valor faltante (`error_documento_mal_formado.lang`)

**Entrada:**
```
INSERT INTO productos {"nombre": "silla", "precio":}
```

**Salida:**
```
ERROR: syntax error
✗ Parse failed
```

La regla `Pair → string ":" Value` exige un valor después de `:`. El `}` no es un `Value` válido.

---

## Resumen

### Casos válidos

| Caso | Operación | Resultado |
|------|-----------|-----------|
| `crear_valido.lang` | INSERT simple | ✓ PASS |
| `leer_valido.lang` | FIND con WHERE | ✓ PASS |
| `actualizar_valido.lang` | UPDATE con filtro | ✓ PASS |
| `borrar_valido.lang` | DELETE con filtro | ✓ PASS |
| `documento_complejo.lang` | Múltiples sentencias + anidamiento | ✓ PASS |
| `arreglos_anidados.lang` | Arreglos + doc anidado | ✓ PASS |

### Casos inválidos

| Caso | Error introducido | Resultado |
|------|-------------------|-----------|
| `error_insert_sin_documento.lang` | INSERT sin `{...}` | ✓ RECHAZADO |
| `error_find_sin_tabla.lang` | FIND sin nombre de tabla | ✓ RECHAZADO |
| `error_documento_mal_formado.lang` | Valor faltante en par | ✓ RECHAZADO |

**9/9 pruebas exitosas.** El parser acepta correctamente entradas válidas y rechaza entradas que violan la gramática definida en `Gramatica inicial.txt`.
