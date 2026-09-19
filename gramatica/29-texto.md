# Producción 29 · `<texto>`

**Nombres y valores** · Gramática BNF de TocaScript · Grupo 8

## La producción

La producción `<texto>` y, debajo, todas las que abre hasta llegar a los átomos —terminales entre comillas—. Todo en un mismo sitio, como en el tablero.

```
29  <texto> ::= '"' { <letra> | <mayuscula> | <digito> | " " | "/" } '"'

30  <letra> ::= "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m"
              | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z"
31  <mayuscula> ::= "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M"
                  | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z"
32  <digito> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
```

## Cómo se lee

Una comilla doble, cero o más letras, mayúsculas, dígitos, espacios o barras, y otra comilla doble.

## Qué usa y quién la usa

| | |
|---|---|
| **Terminales que aparecen** (entre comillas) | `" "` · `"/"` · `'"'` |
| **No terminales que aparecen** (se abren en otra producción) | `<letra>` · `<mayuscula>` · `<digito>` |
| **Producciones que usan `<texto>`** | `<pieza>` · `<valor>` |

## Ejemplo válido y su derivación

Cada ejemplo, y debajo el árbol que la gramática construye para él: cada nodo es una producción (con su número) y las hojas son terminales entre comillas. Derivación producida por el parser (`verificar.py`) que implementa estas 33 producciones; en `<identificador>`, `<numero>`, `<texto>` y `<nota>` se muestran directamente las hojas — cada carácter viene de `<letra>`, `<mayuscula>` o `<digito>`.

```
"ff"
```

```
<texto> (29)
  '"'
  <letra> (30)
    "f"
  <letra> (30)
    "f"
  '"'
```

```
"4/4"
```

```
<texto> (29)
  '"'
  <digito> (32)
    "4"
  "/"
  <digito> (32)
    "4"
  '"'
```

```
"Do mayor"
```

```
<texto> (29)
  '"'
  <mayuscula> (31)
    "D"
  <letra> (30)
    "o"
  " "
  <letra> (30)
    "m"
  <letra> (30)
    "a"
  <letra> (30)
    "y"
  <letra> (30)
    "o"
  <letra> (30)
    "r"
  '"'
```

## Ejemplo inválido

```
'ff'
```

**Por qué no deriva:** Las comillas simples no delimitan texto en TocaScript.

## Nota de diseño

Aquí viven las comillas: la producción empieza y termina en `'"'`, así que todo texto las lleva a los dos lados. Las producciones que usan un texto —valor, pieza— no las repiten: dicen `<texto>` y al derivar aparecen. La comilla doble como terminal se escribe `'"'`, entre comillas simples, porque las dobles ya marcan los demás terminales y `"""` sería ilegible.

---
*Convención: `<x>` no terminal · `"x"` terminal · `'"'` la comilla doble como terminal · `{ }` cero o más · `[ ]` cero o uno · `|` alternativa · `<nl>` salto de línea*
