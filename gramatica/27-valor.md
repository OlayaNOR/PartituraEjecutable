# Producción 27 · `<valor>`

**Nombres y valores** · Gramática BNF de TocaScript · Grupo 8

## La producción

La producción `<valor>` y, debajo, todas las que abre hasta llegar a los átomos —terminales entre comillas—. Todo en un mismo sitio, como en el tablero.

```
27  <valor> ::= <numero> | "true" | "false" | <texto>

28  <numero> ::= <digito> { <digito> } [ "." <digito> { <digito> } ]
32  <digito> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
29  <texto> ::= '"' { <letra> | <mayuscula> | <digito> | " " | "/" } '"'
30  <letra> ::= "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m"
              | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z"
31  <mayuscula> ::= "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M"
                  | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z"
```

## Cómo se lee

Un número, un booleano o un texto.

## Qué usa y quién la usa

| | |
|---|---|
| **Terminales que aparecen** (entre comillas) | `"true"` · `"false"` |
| **No terminales que aparecen** (se abren en otra producción) | `<numero>` · `<texto>` |
| **Producciones que usan `<valor>`** | `<ajuste>` · `<primario>` |

## Ejemplo válido y su derivación

Cada ejemplo, y debajo el árbol que la gramática construye para él: cada nodo es una producción (con su número) y las hojas son terminales entre comillas. Derivación producida por el parser (`verificar.py`) que implementa estas 33 producciones; en `<identificador>`, `<numero>`, `<texto>` y `<nota>` se muestran directamente las hojas — cada carácter viene de `<letra>`, `<mayuscula>` o `<digito>`.

```
140
```

```
<valor> (27)
  <numero> (28)  → "1" "4" "0"
```

```
0.85
```

```
<valor> (27)
  <numero> (28)  → "0" "." "8" "5"
```

```
true
```

```
<valor> (27)
  "true"
```

```
"ff"
```

```
<valor> (27)
  <texto> (29)  → '"' "f" "f" '"'
```

## Ejemplo inválido

```
verdadero
ff
```

**Por qué no deriva:** `verdadero` no es una alternativa. `ff` sin comillas no es un `<texto>`: sería un identificador.

## Nota de diseño

Los cuatro tipos de dato del lenguaje están en esta línea.

---
*Convención: `<x>` no terminal · `"x"` terminal · `'"'` la comilla doble como terminal · `{ }` cero o más · `[ ]` cero o uno · `|` alternativa · `<nl>` salto de línea*
