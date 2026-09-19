# Producción 30 · `<letra>`

**Átomos** · Gramática BNF de TocaScript · Grupo 8

## La producción

Producción terminal: todas sus alternativas van entre comillas, no abre nada más.

```
30  <letra> ::= "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m"
              | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z"
```

## Cómo se lee

Una de las 26 letras minúsculas del alfabeto inglés, enumeradas una a una: en BNF no existe la notación de rango, y unos puntos suspensivos entre comillas serían un terminal más.

## Qué usa y quién la usa

| | |
|---|---|
| **Terminales que aparecen** (entre comillas) | `"a"` · `"b"` · `"c"` · `"d"` · `"e"` · `"f"` · `"g"` · `"h"` · `"i"` · `"j"` · `"k"` · `"l"` · `"m"` · `"n"` · `"o"` · `"p"` · `"q"` · `"r"` · `"s"` · `"t"` · `"u"` · `"v"` · `"w"` · `"x"` · `"y"` · `"z"` |
| **No terminales que aparecen** (se abren en otra producción) | ninguno — producción terminal |
| **Producciones que usan `<letra>`** | `<identificador>` · `<texto>` |

## Ejemplo válido y su derivación

Cada ejemplo, y debajo el árbol que la gramática construye para él: cada nodo es una producción (con su número) y las hojas son terminales entre comillas. Derivación producida por el parser (`verificar.py`) que implementa estas 33 producciones; en `<identificador>`, `<numero>`, `<texto>` y `<nota>` se muestran directamente las hojas — cada carácter viene de `<letra>`, `<mayuscula>` o `<digito>`.

```
q
```

```
<letra> (30)
  "q"
```

## Ejemplo inválido

```
ñ
```

**Por qué no deriva:** Las letras con tilde y la eñe no están entre las alternativas, a propósito, para que el lexer no dependa de la codificación del archivo.

## Nota de diseño

Átomo: no se abre en nada más.

---
*Convención: `<x>` no terminal · `"x"` terminal · `'"'` la comilla doble como terminal · `{ }` cero o más · `[ ]` cero o uno · `|` alternativa · `<nl>` salto de línea*
