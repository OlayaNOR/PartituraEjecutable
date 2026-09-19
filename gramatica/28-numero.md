# Producción 28 · `<numero>`

**Nombres y valores** · Gramática BNF de TocaScript · Grupo 8

## La producción

La producción `<numero>` y, debajo, todas las que abre hasta llegar a los átomos —terminales entre comillas—. Todo en un mismo sitio, como en el tablero.

```
28  <numero> ::= <digito> { <digito> } [ "." <digito> { <digito> } ]

32  <digito> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
```

## Cómo se lee

Uno o más dígitos, y opcionalmente un punto seguido de uno o más dígitos.

## Qué usa y quién la usa

| | |
|---|---|
| **Terminales que aparecen** (entre comillas) | `"."` |
| **No terminales que aparecen** (se abren en otra producción) | `<digito>` |
| **Producciones que usan `<numero>`** | `<valor>` |

## Ejemplo válido y su derivación

Cada ejemplo, y debajo el árbol que la gramática construye para él: cada nodo es una producción (con su número) y las hojas son terminales entre comillas. Derivación producida por el parser (`verificar.py`) que implementa estas 33 producciones; en `<identificador>`, `<numero>`, `<texto>` y `<nota>` se muestran directamente las hojas — cada carácter viene de `<letra>`, `<mayuscula>` o `<digito>`.

```
96
```

```
<numero> (28)
  <digito> (32)
    "9"
  <digito> (32)
    "6"
```

```
0.85
```

```
<numero> (28)
  <digito> (32)
    "0"
  "."
  <digito> (32)
    "8"
  <digito> (32)
    "5"
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
