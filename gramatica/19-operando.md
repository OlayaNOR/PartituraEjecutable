# Producción 19 · `<operando>`

**La regla de interpretación** · Gramática BNF de TocaScript · Grupo 8

## La producción

La producción `<operando>` y, debajo, todas las que abre hasta llegar a los átomos —terminales entre comillas—. Todo en un mismo sitio, como en el tablero.

```
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
```

## Cómo se lee

Una variable, un valor fijo, o una cuenta entre dos operandos.

## Qué usa y quién la usa

| | |
|---|---|
| **Terminales que aparecen** (entre comillas) | — |
| **No terminales que aparecen** (se abren en otra producción) | `<variable>` · `<valor>` · `<op_aritmetico>` |
| **Producciones que usan `<operando>`** | `<condicion>` · `<accion>` |

## Ejemplo válido

```
tempo
10
duracion_total - 2
```


## Ejemplo inválido

```
tempo -
```

**Por qué no deriva:** Tras el operador aritmético falta el segundo `<operando>`.

## Nota de diseño

Recursiva: un operando puede contener operandos. La aritmética se lee de izquierda a derecha.

---
*Convención: `<x>` no terminal · `"x"` terminal · `'"'` la comilla doble como terminal · `{ }` cero o más · `[ ]` cero o uno · `|` alternativa · `<nl>` salto de línea*
