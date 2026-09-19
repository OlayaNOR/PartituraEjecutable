# Producción 15 · `<termino>`

**La regla de interpretación** · Gramática BNF de TocaScript · Grupo 8

## La producción

La producción `<termino>` y, debajo, todas las que abre hasta llegar a los átomos —terminales entre comillas—. Todo en un mismo sitio, como en el tablero.

```
15  <termino> ::= <factor> { "Y" <factor> }

16  <factor> ::= "NO" <factor> | "(" <expresion> ")" | <condicion> | <variable>
14  <expresion> ::= <termino> { "O" <termino> }
15  <termino> ::= <factor> { "Y" <factor> }
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

Un factor, seguido opcionalmente de más factores unidos por `Y`.

## Qué usa y quién la usa

| | |
|---|---|
| **Terminales que aparecen** (entre comillas) | `"Y"` |
| **No terminales que aparecen** (se abren en otra producción) | `<factor>` |
| **Producciones que usan `<termino>`** | `<expresion>` |

## Ejemplo válido

```
es_estribillo Y intensidad > 0.7
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
