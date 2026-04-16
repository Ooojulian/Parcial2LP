# Conceptos — CYK y LL(1)

## Gramática de la calculadora

### Original (con recursión izquierda)

```
E  → E + T | E - T | T
T  → T * F | T / F | F
F  → ( E ) | num
```

Resuelve precedencia (`*` antes que `+`) y asociatividad izquierda. No es LL(1) por la recursión izquierda.

### Transformada para LL(1) (sin recursión izquierda)

```
E   → T E'
E'  → + T E' | - T E' | ε

T   → F T'
T'  → * F T' | / F T' | ε

F   → ( E ) | num
```

### Transformada para CYK (Forma Normal de Chomsky)

CYK requiere reglas de la forma `A → B C` o `A → a`. Se agregan no-terminales auxiliares:

```
E         → T E' | T              (unidad)
E'        → ADD_RIGHT T           ADD_RIGHT → + | -
T         → F T' | F              (unidad)
T'        → MUL_RIGHT F           MUL_RIGHT → * | /
F         → num | ( E_CLOSE       E_CLOSE → E )
```

## Algoritmo CYK

Tabla dinámica n×n. `chart[i][j]` = conjunto de no-terminales que derivan `tokens[i..j]`.

```
1. Diagonal: llenar chart[i][i] con los terminales individuales
2. Por longitud creciente (2 a n):
     Para cada substring [i,j]:
       Para cada punto de corte k en [i, j-1]:
         Si A → B C y B ∈ chart[i][k] y C ∈ chart[k+1][j]:
           añadir A a chart[i][j]
3. Aceptar si E ∈ chart[0][n-1]
```

**Complejidad:** O(n²) celdas × O(n) cortes × O(|G|) reglas = **O(n³)**

## Algoritmo LL(1)

Descenso recursivo — una función por cada no-terminal. Avanza con 1 token de lookahead.

```python
def E():
    T()
    E_prima()

def E_prima():
    if lookahead in {'+', '-'}:
        consumir()
        T()
        E_prima()
    # else: ε (no hacer nada)
```

**Complejidad:** cada token se procesa exactamente una vez = **O(n)**

## Comparación

| Aspecto | CYK | LL(1) |
|---------|-----|-------|
| Complejidad | O(n³) | O(n) |
| Memoria | O(n²) | O(n) |
| Estrategia | Bottom-up, tabla | Top-down, recursión |
| Gramáticas válidas | Cualquier CFG | Solo LL(1) |
| Uso real | PLN, bioinformática | Compiladores |

Para n = 50 tokens: CYK realiza ~125.000 operaciones, LL(1) realiza ~50.
