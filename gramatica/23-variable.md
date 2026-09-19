# Producción 23 · `<variable>`

**Nombres y valores** · Gramática BNF de TocaScript · Grupo 8

## La producción

La producción `<variable>` y, debajo, todas las que abre hasta llegar a los átomos —terminales entre comillas—. Todo en un mismo sitio, como en el tablero.

```
23  <variable> ::= <identificador>

24  <identificador> ::= <letra> { <letra> | <digito> | "_" }
28  <letra> ::= "a" | "b" | "c" | "..." | "z"
30  <digito> ::= "0" | "1" | "2" | "..." | "9"
```

## Cómo se lee

Una variable se escribe como un identificador.

## Qué usa y quién la usa

| | |
|---|---|
| **Terminales que aparecen** (entre comillas) | — |
| **No terminales que aparecen** (se abren en otra producción) | `<identificador>` |
| **Producciones que usan `<variable>`** | `<factor>` · `<operando>` · `<accion>` |

## Ejemplo válido

```
compas_actual
tiene_percusion
```


## Ejemplo inválido

```
Tempo
```

**Por qué no deriva:** Empieza en mayúscula, y `<identificador>` empieza por `<letra>`, que solo tiene minúsculas.

## Nota de diseño

El conjunto de variables es cerrado: son las 20 de la tabla. Sintácticamente cualquier identificador deriva; que exista lo comprueba el intérprete.

---
*Convención: `<x>` no terminal · `"x"` terminal · `'"'` la comilla doble como terminal · `{ }` cero o más · `[ ]` cero o uno · `|` alternativa · `<nl>` salto de línea*
