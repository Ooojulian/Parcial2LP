# Solución — Implementación y Comparación

## Enunciado

> Implemente un parser usando el algoritmo CYK para realizar las operaciones de una calculadora. Realice pruebas sobre el rendimiento de este algoritmo comparándolo con un parser de tipo predictivo.

La gramática utilizada está en [`CONCEPTOS.md`](CONCEPTOS.md).

---

## Implementaciones

### Parser CYK (`src/analizador_cyk.py`)

Tabla dinámica n×n. Acepta si el símbolo inicial `E` aparece en `chart[0][n-1]`.

```python
parser = CYKAnalizador()
ok, tiempo = parser.parse("2 + 3 * 4")
```

### Parser LL(1) (`src/analizador_ll1.py`)

Descenso recursivo predictivo. Una función por no-terminal, 1 token de lookahead.

```python
parser = LL1Analizador()
ok, tiempo = parser.parse("2 + 3 * 4")
```

---

## Pruebas de corrección

### Casos válidos

El parser LL(1) **calcula el resultado** durante el análisis. CYK solo reconoce (acepta/rechaza).

| Expresión | Resultado | LL(1) | CYK | Ratio |
|-----------|-----------|-------|-----|-------|
| `2` | **= 2** | ✓ 0.0081ms | ✓ 0.0086ms | 1.1x |
| `2 + 3` | **= 5** | ✓ 0.0091ms | ✓ 0.0188ms | 2.1x |
| `2 + 3 * 4` | **= 14** | ✓ 0.0076ms | ✓ 0.1123ms | 14.7x |
| `( 2 + 3 ) * 4` | **= 20** | ✓ 0.0091ms | ✓ 0.0696ms | 7.7x |
| `10 - 5 / 2` | **= 7.5** | ✓ 0.0069ms | ✓ 0.0324ms | 4.7x |
| `( ( 2 + 3 ) * ( 4 - 1 ) ) / 3` | **= 5** | ✓ 0.0129ms | ✓ 0.5052ms | 39.2x |

La precedencia es correcta: `2 + 3 * 4 = 14` (no 20), `10 - 5 / 2 = 7.5` (no 2.5).

### Casos inválidos (ambos rechazan correctamente)

| Expresión | Motivo | Resultado |
|-----------|--------|-----------|
| `2 +` | Operando derecho faltante | ✓ RECHAZADO |
| `* 3` | Sin operando izquierdo | ✓ RECHAZADO |
| `( 2 + 3` | Paréntesis sin cerrar | ✓ RECHAZADO |

**9/9 pruebas exitosas.**

---

## Comparación de rendimiento

Misma expresión base escalada a distintas longitudes:

| Tokens | LL(1) | CYK | CYK/LL(1) |
|--------|-------|-----|-----------|
| 5 | 0.0048ms | 0.0315ms | 6.6x |
| 17 | 0.0114ms | 0.6678ms | 58.4x |
| 29 | 0.0191ms | 3.0825ms | 161.6x |
| 41 | 0.0424ms | 8.3902ms | 197.7x |
| 59 | 0.0634ms | 24.1160ms | 380.3x |

El ratio crece con n — confirmando la diferencia O(n) vs O(n³).

---

## Análisis de complejidad

### Comportamiento observado

```
n=5  → CYK/LL(1) ≈ 7x      (n² = 25)
n=17 → CYK/LL(1) ≈ 58x     (n² = 289)
n=59 → CYK/LL(1) ≈ 380x    (n² = 3481)
```

El ratio experimental crece aproximadamente como n², consistente con la teoría:

```
CYK/LL(1) = O(n³) / O(n) = O(n²)
```

### ¿Por qué LL(1) es más rápido?

- **LL(1):** cada token se procesa exactamente una vez — 1 pase lineal
- **CYK:** para cada par `(i,j)` evalúa todos los cortes `k` — tabla completa

Para n=59: LL(1) hace ~59 operaciones, CYK hace ~59³ ≈ 205.000.

---

## Conclusión

| Aspecto | CYK | LL(1) |
|---------|-----|-------|
| Complejidad | O(n³) | O(n) |
| Velocidad real (n=59) | 24ms | 0.06ms |
| Ratio | — | **380x más rápido** |
| Escalabilidad | No (crece cúbico) | Sí (lineal) |

**Los compiladores reales usan LL(1) o LR(1)** porque O(n³) es inaceptable: para 1.000 tokens, CYK necesitaría 10⁹ operaciones vs 1.000 de LL(1).

CYK tiene su lugar en gramáticas arbitrarias (PLN, bioinformática) donde la flexibilidad importa más que la velocidad.
