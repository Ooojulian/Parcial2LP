# Conceptos — Ambigüedad y Desambiguación

## El problema: Dangling Else

La cadena `if E1 then if E2 then S1 else S2` tiene dos interpretaciones posibles:

**Interpretación A** — `else` con el segundo `if` (correcta):
```
if E1 then {
    if E2 then S1 else S2
}
```

**Interpretación B** — `else` con el primer `if` (ambigua):
```
if E1 then {
    if E2 then S1
} else S2
```

La gramática original permite ambas → es ambigua.

## ¿Qué es ambigüedad en una gramática?

Una gramática es **ambigua** si existe al menos una cadena que tiene dos o más árboles de derivación distintos. En Bison esto se manifiesta como un **conflicto shift/reduce**: el parser no sabe si desplazar el token `else` o reducir la producción actual.

## Por qué la gramática original es ambigua

```
prop → if expr then prop        ← "prop" puede ser otro if sin else
     | prop_emparejada
```

El problema: cuando el parser ve `if E2 then S1` seguido de `else`, no sabe si:
- **Reducir** `if E2 then S1` a `prop` (y emparejar `else` con `if E1`)
- **Desplazar** `else` (y emparejarlo con `if E2`)

Ambas acciones son válidas según las reglas → **conflicto shift/reduce**.

## Solución: Estratificación

Separar `prop` en dos niveles mutuamente excluyentes:

| No-terminal | Significado | Estructura |
|-------------|-------------|------------|
| `prop_emparejada` | Todo `if` tiene `else` | `if E then [emparejada] else [emparejada]` |
| `prop_no_emparejada` | Al menos un `if` sin `else` | `if E then [cualquier prop]` |

**Regla clave:** Después de `then` en un if-then-**else**, solo puede ir `prop_emparejada`. Esto impide que un `if` interno "robe" el `else` externo.

## Gramática desambiguada

```
prop → prop_emparejada
     | prop_no_emparejada

prop_emparejada → if expr then prop_emparejada else prop_emparejada
                | otras

prop_no_emparejada → if expr then prop
                   | if expr then prop_emparejada else prop_no_emparejada
```

Con esta estructura, para `if E1 then if E2 then S1 else S2`:
- `if E2 then S1` solo puede derivar a `prop_no_emparejada` (sin else)
- Pero después de `then` en `if E1 then _ else _` se requiere `prop_emparejada`
- → El `else` **forzosamente** pertenece a `if E2`. Derivación única.
