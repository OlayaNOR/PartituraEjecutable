# Producción 17 · `<condicion>`

**La regla de interpretación** · Gramática BNF de TocaScript · Grupo 8

## La producción

La producción `<condicion>` y, debajo, todas las que abre hasta llegar a los átomos —terminales entre comillas—. Todo en un mismo sitio, como en el tablero.

```
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

Siempre tres cosas: un operando, un operador relacional y otro operando.

## Qué usa y quién la usa

| | |
|---|---|
| **Terminales que aparecen** (entre comillas) | — |
| **No terminales que aparecen** (se abren en otra producción) | `<operando>` · `<operador>` |
| **Producciones que usan `<condicion>`** | `<factor>` |

## Ejemplo válido

```
num_voces >= 4
compas = "3/4"
```

## Derivación del ejemplo hasta los átomos

Cada flecha aplica una producción; entre paréntesis, cuál. Al final solo quedan terminales entre comillas.

```
<condicion>
→ <operando> <operador> <operando>   (17)
→ <variable> ">=" <valor>   (19 operando ×2 · 18 operador)
→ <identificador> ">=" <numero>   (23 variable · 25 valor)
→ "n" "u" "m" "_" "v" "o" "c" "e" "s" ">=" "4"   (24, 28 · 26, 30)

Resultado:  num_voces >= 4
```

## Ejemplo inválido

```
num_voces >= 4 >= 6
```

**Por qué no deriva:** Una condición tiene exactamente un operador. Para encadenar hay que usar `"Y"`.

## Nota de diseño

Es la regla que obliga a que toda condición sea medible.

---
*Convención: `<x>` no terminal · `"x"` terminal · `'"'` la comilla doble como terminal · `{ }` cero o más · `[ ]` cero o uno · `|` alternativa · `<nl>` salto de línea*
