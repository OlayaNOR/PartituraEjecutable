# Producción 17 · `<factor>`

**La regla de interpretación** · Gramática BNF de TocaScript · Grupo 8

## La producción

La producción `<factor>` y, debajo, todas las que abre hasta llegar a los átomos —terminales entre comillas—. Todo en un mismo sitio, como en el tablero.

```
17  <factor> ::= "NO" <factor>
               | "(" <expresion> ")"
               | <condicion>
               | <variable>

15  <expresion> ::= <termino> { "O" <termino> }
16  <termino> ::= <factor> { "Y" <factor> }
17  <factor> ::= "NO" <factor>
               | "(" <expresion> ")"
               | <condicion>
               | <variable>
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

Una de cuatro cosas: la negación de otro factor; una expresión entre paréntesis; una comparación; o una variable booleana sola.

## Qué usa y quién la usa

| | |
|---|---|
| **Terminales que aparecen** (entre comillas) | `"NO"` · `"("` · `")"` |
| **No terminales que aparecen** (se abren en otra producción) | `<expresion>` · `<condicion>` · `<variable>` |
| **Producciones que usan `<factor>`** | `<termino>` |

## Ejemplo válido y su derivación

Cada ejemplo, y debajo el árbol que la gramática construye para él: cada nodo es una producción (con su número) y las hojas son terminales entre comillas. Derivación producida por el parser (`verificar.py`) que implementa estas 33 producciones; en `<identificador>`, `<numero>`, `<texto>` y `<nota>` se muestran directamente las hojas — cada carácter viene de `<letra>`, `<mayuscula>` o `<digito>`.

```
NO tiene_percusion
```

```
<factor> (17)
  "NO"
  <factor> (17)
    <variable> (25)
      <identificador> (26)  → "t" "i" "e" "n" "e" "_" "p" "e" "r" "c" "u" "s" "i" "o" "n"
```

```
(es_coda O es_final)
```

```
<factor> (17)
  "("
  <expresion> (15)
    <termino> (16)
      <factor> (17)
        <variable> (25)
          <identificador> (26)  → "e" "s" "_" "c" "o" "d" "a"
    "O"
    <termino> (16)
      <factor> (17)
        <variable> (25)
          <identificador> (26)  → "e" "s" "_" "f" "i" "n" "a" "l"
  ")"
```

```
num_voces > 3
```

```
<factor> (17)
  <condicion> (18)
    <operando> (20)
      <sumando> (21)
        <primario> (22)
          <variable> (25)
            <identificador> (26)  → "n" "u" "m" "_" "v" "o" "c" "e" "s"
    <operador> (19)
      ">"
    <operando> (20)
      <sumando> (21)
        <primario> (22)
          <valor> (27)
            <numero> (28)  → "3"
```

```
es_coda
```

```
<factor> (17)
  <variable> (25)
    <identificador> (26)  → "e" "s" "_" "c" "o" "d" "a"
```

## Ejemplo inválido

```
NO (es_coda
```

**Por qué no deriva:** Se abrió el paréntesis y no se cerró.

## Nota de diseño

Es la producción recursiva de la condición: un factor puede contener una expresión entera, y esa expresión contiene factores. Eso permite anidar sin límite. `NO` vive aquí, en el nivel más bajo de los tres —expresión, término, factor—, por eso liga más fuerte que `Y` y que `O` sin una regla de precedencia aparte. Los paréntesis van entre comillas porque son símbolos del lenguaje, no notación.

---
*Convención: `<x>` no terminal · `"x"` terminal · `'"'` la comilla doble como terminal · `{ }` cero o más · `[ ]` cero o uno · `|` alternativa · `<nl>` salto de línea*
