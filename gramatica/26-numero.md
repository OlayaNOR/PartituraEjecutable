# Producción 26 · `<numero>`

**Nombres y valores** · Gramática BNF de TocaScript · Grupo 8

## La producción

La producción `<numero>` y, debajo, todas las que abre hasta llegar a los átomos —terminales entre comillas—. Todo en un mismo sitio, como en el tablero.

```
26  <numero> ::= <digito> { <digito> } [ "." <digito> { <digito> } ]

30  <digito> ::= "0" | "1" | "2" | "..." | "9"
```

## Cómo se lee

Uno o más dígitos, y opcionalmente un punto seguido de uno o más dígitos.

## Qué usa y quién la usa

| | |
|---|---|
| **Terminales que aparecen** (entre comillas) | `"."` |
| **No terminales que aparecen** (se abren en otra producción) | `<digito>` |
| **Producciones que usan `<numero>`** | `<cabecera>` · `<valor>` |

## Ejemplo válido

```
96
0.85
```

## Derivación del ejemplo hasta los átomos

Cada flecha aplica una producción; entre paréntesis, cuál. Al final solo quedan terminales entre comillas.

```
<numero>
→ <digito> <digito> <digito>   (26: primer dígito + dos de la repetición; sin parte decimal)
→ "1" "0" "0"   (30 digito)

Resultado:  100

Con decimales:
<numero>
→ <digito> "." <digito> <digito>   (26: la parte opcional [ "." … ] presente)
→ "0" "." "8" "5"   (30)

Resultado:  0.85
```

## Ejemplo inválido

```
1.
.5
0,85
```

**Por qué no deriva:** El punto necesita dígitos a ambos lados. La coma no es separador decimal.

## Nota de diseño

No hay signo: los negativos se obtienen restando, `tempo - 10`.

---
*Convención: `<x>` no terminal · `"x"` terminal · `'"'` la comilla doble como terminal · `{ }` cero o más · `[ ]` cero o uno · `|` alternativa · `<nl>` salto de línea*
