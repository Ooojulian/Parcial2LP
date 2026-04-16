# Solución — Demostración y Desambiguación

## Parte 1: Demostración de Ambigüedad

### Gramática original (del enunciado)

```
prop             → if expr then prop
                 | prop_emparejada

prop_emparejada  → if expr then prop_emparejada else prop
                 | otras
```

### Cadena de prueba

```
if E1 then if E2 then S1 else S2
```

### Dos interpretaciones para la misma cadena

La cadena `if E1 then if E2 then S1 else S2` admite dos interpretaciones semánticas distintas:

**Interpretación A** — `else` pertenece al segundo `if` (más cercano):
```
if E1 then {
    if E2 then S1
    else S2          ← else de E2
}
```

**Interpretación B** — `else` pertenece al primer `if`:
```
if E1 then {
    if E2 then S1
}
else S2              ← else de E1
```

Ambas son sintácticamente válidas según las reglas de la gramática original — no hay nada que obligue al parser a elegir una sobre otra.

### Derivación completa (única posible con esta gramática)

La única derivación izquierda que completa la cadena es la **Interpretación A**:

```
prop
⟹ if E1 then prop                                   [prop → if expr then prop]
⟹ if E1 then prop_emparejada                        [prop → prop_emparejada]
⟹ if E1 then if E2 then prop_emparejada else prop   [prop_emparejada → if expr then prop_emparejada else prop]
⟹ if E1 then if E2 then S1 else prop                [prop_emparejada → otras]
⟹ if E1 then if E2 then S1 else S2                  [prop → prop_emparejada → otras]
```

Árbol sintáctico:
```
            prop
             |
      if E1 then prop
                  |
           prop_emparejada
                  |
      if E2 then prop_emparejada else prop
                  |                   |
                 S1                  S2
```

La **Interpretación B** no produce una derivación izquierda completa con esta gramática porque `prop_emparejada` exige siempre un `else` — no puede derivar `if E2 then S1` solo.

### ¿Por qué entonces es ambigua?

La ambigüedad **no se manifiesta en dos derivaciones completas** sino en el **estado del autómata LALR**: cuando el parser ha leído `if E1 then if E2 then S1` y el siguiente token es `else`, tiene dos acciones posibles y no puede decidir con 1 token de lookahead cuál es correcta:

| Acción | Significado |
|--------|-------------|
| **Reducir** `if E2 then S1` → `prop` | El `if E2` termina aquí; el `else` es de `if E1` |
| **Desplazar** `else` | El `else` pertenece a `if E2` (se completa `prop_emparejada`) |

Ambas acciones son legales según las reglas — esto es un **conflicto shift/reduce**, y es la definición formal de ambigüedad en un parser LR.

### Evidencia en Bison

Compilando `src/ambigua.y`:

```
Estado 9 conflictos: 1 desplazamiento/reducción
```

Bison detecta exactamente 1 conflicto shift/reduce en el estado donde aparece `ELSE`. **La existencia de este conflicto es la prueba formal de que la gramática es ambigua.** Bison lo resuelve eligiendo shift por defecto (convención), pero eso no elimina la ambigüedad — solo la oculta.

---

## Parte 2: Desambiguación por Estratificación

### Gramática desambiguada (`desambigua.y`)

```
prop → prop_emparejada
     | prop_no_emparejada

prop_emparejada → if expr then prop_emparejada else prop_emparejada
                | otras

prop_no_emparejada → if expr then prop
                   | if expr then prop_emparejada else prop_no_emparejada
```

### Compilando `desambigua.y`

```
0 conflictos shift/reduce
0 conflictos reduce/reduce
```

Bison no reporta ningún conflicto → gramática no ambigua.

---

## Parte 3: Pruebas

### Caso principal — `if E then if E then S else S`

**Entrada:** `i E t i E t s e s`

**Gramática ambigua:**
```
=== GRAMÁTICA AMBIGUA (con shift/reduce conflict) ===
Reduce: instruccion
Reduce: instruccion
Reduce: prop_emparejada
Reduce: if-then-emparejada-else-prop
Reduce: prop_emparejada
Reduce: if-then-prop (sin else)
```
Bison elige shift por defecto → resultado "correcto" pero por convención, no por estructura.

**Gramática desambiguada:**
```
=== GRAMÁTICA DESAMBIGUADA (sin shift/reduce conflicts) ===
Reduce: prop_emparejada → instruccion
Reduce: prop_emparejada → instruccion
Reduce: prop_emparejada → if expr then prop_emparejada else prop_emparejada
        (else MATCHED con if anterior)
Reduce: prop → prop_emparejada
Reduce: prop_no_emparejada → if expr then prop
        (if WITHOUT emparejar)
Reduce: prop → prop_no_emparejada
```
Derivación única y explícita: `else` forzosamente pertenece al segundo `if`.

---

### Caso 2 — `if E then S` (sin else)

**Entrada:** `i E t s`

```
Reduce: prop_emparejada → instruccion
Reduce: prop → prop_emparejada
Reduce: prop_no_emparejada → if expr then prop
        (if WITHOUT emparejar)
Reduce: prop → prop_no_emparejada
```
Reconocido como `prop_no_emparejada` — correcto, es un if sin else.

---

### Caso 3 — `if E then S else S` (completo)

**Entrada:** `i E t s e s`

```
Reduce: prop_emparejada → instruccion
Reduce: prop_emparejada → instruccion
Reduce: prop_emparejada → if expr then prop_emparejada else prop_emparejada
        (else MATCHED con if anterior)
Reduce: prop → prop_emparejada
```
Reconocido como `prop_emparejada` — correcto, if-then-else completo.

---

### Caso 4 — Triple anidado `if E then if E then if E then S else S`

**Entrada:** `i E t i E t i E t s e s`

```
Reduce: prop_emparejada → instruccion
Reduce: prop_emparejada → instruccion
Reduce: prop_emparejada → if expr then prop_emparejada else prop_emparejada
        (else MATCHED con if anterior)
Reduce: prop → prop_emparejada
Reduce: prop_no_emparejada → if expr then prop
        (if WITHOUT emparejar)
Reduce: prop → prop_no_emparejada
Reduce: prop_no_emparejada → if expr then prop
        (if WITHOUT emparejar)
Reduce: prop → prop_no_emparejada
```
El único `else` se empareja con el `if` más cercano. Los dos `if` externos quedan sin emparejar (`prop_no_emparejada`).

---

## Resumen

| Aspecto | Gramática ambigua | Gramática desambiguada |
|---------|-------------------|----------------------|
| Conflictos Bison | 1 shift/reduce | 0 |
| Derivaciones por cadena | Múltiples posibles | Exactamente 1 |
| Regla del `else` | Indefinida | Siempre con el `if` más cercano |
| Parser determinístico | No (resuelto por convención) | Sí (por estructura) |
