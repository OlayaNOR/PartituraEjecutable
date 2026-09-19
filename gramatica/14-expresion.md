# Producción 14 · `<expresion>`

**La regla de interpretación** · Gramática BNF de TocaScript · Grupo 8

## La producción

La producción `<expresion>` y, debajo, todas las que abre hasta llegar a los átomos —terminales entre comillas—. Todo en un mismo sitio, como en el tablero.

```
14  <expresion> ::= <termino> { "O" <termino> }

15  <termino> ::= <factor> { "Y" <factor> }
16  <factor> ::= "NO" <factor> | "(" <expresion> ")" | <condicion> | <variable>
14  <expresion> ::= <termino> { "O" <termino> }
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

Un término, seguido opcionalmente de más términos unidos por `O`.

## Qué usa y quién la usa

| | |
|---|---|
| **Terminales que aparecen** (entre comillas) | `"O"` |
| **No terminales que aparecen** (se abren en otra producción) | `<termino>` |
| **Producciones que usan `<expresion>`** | `<regla>` · `<factor>` |

## Ejemplo válido

```
es_estrofa O hay_repeticion
```


## Ejemplo inválido

```
es_estrofa O
```

**Por qué no deriva:** Después de `"O"` tiene que venir otro `<termino>`.

## Nota de diseño

`O` vive en el nivel más alto de la condición: es el operador que menos fuerza tiene y se resuelve el último.

---
*Convención: `<x>` no terminal · `"x"` terminal · `'"'` la comilla doble como terminal · `{ }` cero o más · `[ ]` cero o uno · `|` alternativa · `<nl>` salto de línea*
