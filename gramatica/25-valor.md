# Producción 25 · `<valor>`

**Nombres y valores** · Gramática BNF de TocaScript · Grupo 8

## La producción

La producción `<valor>` y, debajo, todas las que abre hasta llegar a los átomos —terminales entre comillas—. Todo en un mismo sitio, como en el tablero.

```
25  <valor> ::= <numero> | "true" | "false" | <texto>

26  <numero> ::= <digito> { <digito> } [ "." <digito> { <digito> } ]
30  <digito> ::= "0" | "1" | "2" | "..." | "9"
27  <texto> ::= '"' { <letra> | <mayuscula> | <digito> | " " | "/" } '"'
28  <letra> ::= "a" | "b" | "c" | "..." | "z"
29  <mayuscula> ::= "A" | "B" | "C" | "..." | "Z"
```

## Cómo se lee

Un número, un booleano o un texto.

## Qué usa y quién la usa

| | |
|---|---|
| **Terminales que aparecen** (entre comillas) | `"true"` · `"false"` |
| **No terminales que aparecen** (se abren en otra producción) | `<numero>` · `<texto>` |
| **Producciones que usan `<valor>`** | `<operando>` |

## Ejemplo válido

```
140
0.85
true
"ff"
```


## Ejemplo inválido

```
verdadero
ff
```

**Por qué no deriva:** `verdadero` no es una alternativa. `ff` sin comillas no es un `<texto>`: sería un identificador.

## Nota de diseño

Los cuatro tipos de dato del lenguaje están en esta línea.

---
*Convención: `<x>` no terminal · `"x"` terminal · `'"'` la comilla doble como terminal · `{ }` cero o más · `[ ]` cero o uno · `|` alternativa · `<nl>` salto de línea*
