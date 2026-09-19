# Producción 16 · `<termino>`

**La regla de interpretación** · Gramática BNF de TocaScript · Grupo 8

## La producción

La producción `<termino>` y, debajo, todas las que abre hasta llegar a los átomos —terminales entre comillas—. Todo en un mismo sitio, como en el tablero.

```
16  <termino> ::= <factor> { "Y" <factor> }

17  <factor> ::= "NO" <factor>
               | "(" <expresion> ")"
               | <condicion>
               | <variable>
15  <expresion> ::= <termino> { "O" <termino> }
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

Un factor, seguido opcionalmente de más factores unidos por `Y`.

## Qué usa y quién la usa

| | |
|---|---|
| **Terminales que aparecen** (entre comillas) | `"Y"` |
| **No terminales que aparecen** (se abren en otra producción) | `<factor>` |
| **Producciones que usan `<termino>`** | `<expresion>` |

## Ejemplo válido y su derivación

Cada ejemplo, y debajo el árbol que la gramática construye para él: cada nodo es una producción (con su número) y las hojas son terminales entre comillas. Derivación producida por el parser (`verificar.py`) que implementa estas 33 producciones; en `<identificador>`, `<numero>`, `<texto>` y `<nota>` se muestran directamente las hojas — cada carácter viene de `<letra>`, `<mayuscula>` o `<digito>`.

```
es_estribillo Y intensidad > 0.7
```

```
<termino> (16)
  <factor> (17)
    <variable> (25)
      <identificador> (26)  → "e" "s" "_" "e" "s" "t" "r" "i" "b" "i" "l" "l" "o"
  "Y"
  <factor> (17)
    <condicion> (18)
      <operando> (20)
        <sumando> (21)
          <primario> (22)
            <variable> (25)
              <identificador> (26)  → "i" "n" "t" "e" "n" "s" "i" "d" "a" "d"
      <operador> (19)
        ">"
      <operando> (20)
        <sumando> (21)
          <primario> (22)
            <valor> (27)
              <numero> (28)  → "0" "." "7"
```

## Ejemplo inválido

```
es_estribillo Y Y intensidad > 0.7
```

**Por qué no deriva:** Entre los dos `"Y"` falta un `<factor>`.

## Nota de diseño

Un nivel por debajo de la expresión: por eso `Y` liga más fuerte que `O` sin necesidad de paréntesis.

---
*Convención: `<x>` no terminal · `"x"` terminal · `'"'` la comilla doble como terminal · `{ }` cero o más · `[ ]` cero o uno · `|` alternativa · `<nl>` salto de línea*
