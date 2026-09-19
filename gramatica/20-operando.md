# Producción 20 · `<operando>`

**La regla de interpretación** · Gramática BNF de TocaScript · Grupo 8

## La producción

La producción `<operando>` y, debajo, todas las que abre hasta llegar a los átomos —terminales entre comillas—. Todo en un mismo sitio, como en el tablero.

```
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
20  <operando> ::= <sumando> { "+" <sumando> | "-" <sumando> }
```

## Cómo se lee

Uno o más sumandos unidos por `+` o `-`. Es el nivel más alto de la aritmética, como `<expresion>` lo es de la lógica: lo que se suma o resta se resuelve al final.

## Qué usa y quién la usa

| | |
|---|---|
| **Terminales que aparecen** (entre comillas) | `"+"` · `"-"` |
| **No terminales que aparecen** (se abren en otra producción) | `<sumando>` |
| **Producciones que usan `<operando>`** | `<condicion>` · `<primario>` · `<accion>` |

## Ejemplo válido y su derivación

Cada ejemplo, y debajo el árbol que la gramática construye para él: cada nodo es una producción (con su número) y las hojas son terminales entre comillas. Derivación producida por el parser (`verificar.py`) que implementa estas 33 producciones; en `<identificador>`, `<numero>`, `<texto>` y `<nota>` se muestran directamente las hojas — cada carácter viene de `<letra>`, `<mayuscula>` o `<digito>`.

```
tempo
```

```
<operando> (20)
  <sumando> (21)
    <primario> (22)
      <variable> (25)
        <identificador> (26)  → "t" "e" "m" "p" "o"
```

```
10
```

```
<operando> (20)
  <sumando> (21)
    <primario> (22)
      <valor> (27)
        <numero> (28)  → "1" "0"
```

```
duracion_total - 2
```

```
<operando> (20)
  <sumando> (21)
    <primario> (22)
      <variable> (25)
        <identificador> (26)  → "d" "u" "r" "a" "c" "i" "o" "n" "_" "t" "o" "t" "a" "l"
  "-"
  <sumando> (21)
    <primario> (22)
      <valor> (27)
        <numero> (28)  → "2"
```

```
tempo - 10 - 5
```

```
<operando> (20)
  <sumando> (21)
    <primario> (22)
      <variable> (25)
        <identificador> (26)  → "t" "e" "m" "p" "o"
  "-"
  <sumando> (21)
    <primario> (22)
      <valor> (27)
        <numero> (28)  → "1" "0"
  "-"
  <sumando> (21)
    <primario> (22)
      <valor> (27)
        <numero> (28)  → "5"
```

## Ejemplo inválido

```
tempo -
```

**Por qué no deriva:** Tras el `-` falta el segundo `<sumando>`.

## Nota de diseño

Escrito con la repetición `{ }` en lugar de `<operando> <op> <operando>`, el operando deja de ser ambiguo: `tempo - 10 - 5` tiene un solo árbol y se lee de izquierda a derecha. Y como `+` y `-` viven aquí, y `*` y `/` un nivel más abajo en `<sumando>`, la multiplicación va antes que la suma sin una regla aparte: es la misma técnica de los tres niveles `<expresion>` → `<termino>` → `<factor>`.

---
*Convención: `<x>` no terminal · `"x"` terminal · `'"'` la comilla doble como terminal · `{ }` cero o más · `[ ]` cero o uno · `|` alternativa · `<nl>` salto de línea*
