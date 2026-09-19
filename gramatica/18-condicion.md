# Producción 18 · `<condicion>`

**La regla de interpretación** · Gramática BNF de TocaScript · Grupo 8

## La producción

La producción `<condicion>` y, debajo, todas las que abre hasta llegar a los átomos —terminales entre comillas—. Todo en un mismo sitio, como en el tablero.

```
18  <condicion> ::= <operando> <operador> <operando>

20  <operando> ::= <sumando> { "+" <sumando> | "-" <sumando> }
21  <sumando> ::= <primario> { "*" <primario> | "/" <primario> }
22  <primario> ::= <variable> | <valor> | "(" <operando> ")"
25  <variable> ::= <identificador>
26  <identificador> ::= <letra> { <letra> | <digito> | "_" }
                        # y no puede coincidir con ninguna palabra reservada
30  <letra> ::= "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m"
              | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z"
32  <digito> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
27  <valor> ::= <numero> | "true" | "false" | <texto>
28  <numero> ::= <digito> { <digito> } [ "." <digito> { <digito> } ]
29  <texto> ::= '"' { <letra> | <mayuscula> | <digito> | " " | "/" } '"'
31  <mayuscula> ::= "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M"
                  | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z"
19  <operador> ::= ">" | "<" | ">=" | "<=" | "=" | "<>"
```

## Cómo se lee

Siempre tres cosas: un operando, un operador relacional y otro operando.

## Qué usa y quién la usa

| | |
|---|---|
| **Terminales que aparecen** (entre comillas) | — |
| **No terminales que aparecen** (se abren en otra producción) | `<operando>` · `<operador>` |
| **Producciones que usan `<condicion>`** | `<factor>` |

## Ejemplo válido y su derivación

Cada ejemplo, y debajo el árbol que la gramática construye para él: cada nodo es una producción (con su número) y las hojas son terminales entre comillas. Derivación producida por el parser (`verificar.py`) que implementa estas 33 producciones; en `<identificador>`, `<numero>`, `<texto>` y `<nota>` se muestran directamente las hojas — cada carácter viene de `<letra>`, `<mayuscula>` o `<digito>`.

```
num_voces >= 4
```

```
<condicion> (18)
  <operando> (20)
    <sumando> (21)
      <primario> (22)
        <variable> (25)
          <identificador> (26)  → "n" "u" "m" "_" "v" "o" "c" "e" "s"
  <operador> (19)
    ">="
  <operando> (20)
    <sumando> (21)
      <primario> (22)
        <valor> (27)
          <numero> (28)  → "4"
```

```
compas = "3/4"
```

```
<condicion> (18)
  <operando> (20)
    <sumando> (21)
      <primario> (22)
        <variable> (25)
          <identificador> (26)  → "c" "o" "m" "p" "a" "s"
  <operador> (19)
    "="
  <operando> (20)
    <sumando> (21)
      <primario> (22)
        <valor> (27)
          <texto> (29)  → '"' "3" "/" "4" '"'
```

## Ejemplo inválido

```
num_voces >= 4 >= 6
```

**Por qué no deriva:** Una condición tiene exactamente un operador. Para encadenar hay que usar `"Y"`.

## Nota de diseño

Es la regla que obliga a que toda condición sea medible: no se puede escribir «hace calor», hay que escribir `temperatura > 30`.

---
*Convención: `<x>` no terminal · `"x"` terminal · `'"'` la comilla doble como terminal · `{ }` cero o más · `[ ]` cero o uno · `|` alternativa · `<nl>` salto de línea*
