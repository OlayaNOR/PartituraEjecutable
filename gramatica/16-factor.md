# Producción 16 · `<factor>`

**La regla de interpretación** · Gramática BNF de TocaScript · Grupo 8

## La producción

La producción `<factor>` y, debajo, todas las que abre hasta llegar a los átomos —terminales entre comillas—. Todo en un mismo sitio, como en el tablero.

```
16  <factor> ::= "NO" <factor> | "(" <expresion> ")" | <condicion> | <variable>

14  <expresion> ::= <termino> { "O" <termino> }
15  <termino> ::= <factor> { "Y" <factor> }
16  <factor> ::= "NO" <factor> | "(" <expresion> ")" | <condicion> | <variable>
17  <condicion> ::= <operando> <operador> <operando>
19  <operando> ::= <variable> | <valor> | <operando> <op_aritmetico> <operando>
23  <variable> ::= <identificador>
24  <identificador> ::= <letra> { <letra> | <digito> | "_" }
28  <letra> ::= "a" | "b" | "c" | "..." | "z"
30  <digito> ::= "0" | "1" | "2" | "..." | "9"
25  <valor> ::= <numero> | "true" | "false" | <texto>
26  <numero> ::= <digito> { <digito> } [ "." <digito> { <digito> } ]
27  <texto> ::= '"' { <letra> | <mayuscula> | <digito> | " " | "/" } '"'
29  <mayuscula> ::= "A" | "B" | "C" | "..." | "Z"
20  <op_aritmetico> ::= "+" | "-" | "*" | "/"
18  <operador> ::= ">" | "<" | ">=" | "<=" | "=" | "<>"
```

## Cómo se lee

Una de cuatro cosas: la negación de otro factor; una expresión entre paréntesis; una comparación; o una variable booleana sola.

## Qué usa y quién la usa

| | |
|---|---|
| **Terminales que aparecen** (entre comillas) | `"NO"` · `"("` · `")"` |
| **No terminales que aparecen** (se abren en otra producción) | `<expresion>` · `<condicion>` · `<variable>` |
| **Producciones que usan `<factor>`** | `<termino>` |

## Ejemplo válido

```
NO tiene_percusion
(es_coda O es_final)
num_voces > 3
es_coda
```

## Derivación del ejemplo hasta los átomos

Cada flecha aplica una producción; entre paréntesis, cuál. Al final solo quedan terminales entre comillas.

```
<factor>
→ "(" <expresion> ")"   (16, 2.ª alternativa)
→ "(" <termino> "O" <termino> ")"   (14 expresion)
→ "(" <factor> "O" <factor> ")"   (15 termino ×2)
→ "(" <variable> "O" <variable> ")"   (16, 4.ª alternativa ×2)
→ "(" "e" "s" "_" "c" "o" "d" "a" "O" "e" "s" "_" "f" "i" "n" "a" "l" ")"   (23, 24, 28)

Resultado:  (es_coda O es_final)
```

## Ejemplo inválido

```
NO (es_coda
```

**Por qué no deriva:** Se abrió el paréntesis y no se cerró.

## Nota de diseño

Es la producción recursiva de la condición: un factor puede contener una expresión entera entre paréntesis, y esa expresión contiene factores. Eso permite anidar sin límite. `NO` vive aquí, en el nivel más bajo de los tres —expresión, término, factor—, por eso liga más fuerte que `Y` y que `O` sin necesidad de una regla de precedencia aparte. Los paréntesis `"("` `")"` van entre comillas porque son símbolos del lenguaje, no notación.

---
*Convención: `<x>` no terminal · `"x"` terminal · `'"'` la comilla doble como terminal · `{ }` cero o más · `[ ]` cero o uno · `|` alternativa · `<nl>` salto de línea*
