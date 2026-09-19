# Producción 22 · `<accion>`

**La regla de interpretación** · Gramática BNF de TocaScript · Grupo 8

## La producción

La producción `<accion>` y, debajo, todas las que abre hasta llegar a los átomos —terminales entre comillas—. Todo en un mismo sitio, como en el tablero.

```
22  <accion> ::= <variable> "=" <operando> | <identificador>

23  <variable> ::= <identificador>
24  <identificador> ::= <letra> { <letra> | <digito> | "_" }
28  <letra> ::= "a" | "b" | "c" | "..." | "z"
30  <digito> ::= "0" | "1" | "2" | "..." | "9"
19  <operando> ::= <variable> | <valor> | <operando> <op_aritmetico> <operando>
25  <valor> ::= <numero> | "true" | "false" | <texto>
26  <numero> ::= <digito> { <digito> } [ "." <digito> { <digito> } ]
27  <texto> ::= '"' { <letra> | <mayuscula> | <digito> | " " | "/" } '"'
29  <mayuscula> ::= "A" | "B" | "C" | "..." | "Z"
20  <op_aritmetico> ::= "+" | "-" | "*" | "/"
```

## Cómo se lee

Una asignación —variable, igual, operando— o el nombre de una acción predefinida.

## Qué usa y quién la usa

| | |
|---|---|
| **Terminales que aparecen** (entre comillas) | `"="` |
| **No terminales que aparecen** (se abren en otra producción) | `<variable>` · `<operando>` · `<identificador>` |
| **Producciones que usan `<accion>`** | `<acciones>` |

## Ejemplo válido

```
tempo = tempo - 10
activar_percusion
```


## Ejemplo inválido

```
"pp" = dinamica
```

**Por qué no deriva:** A la izquierda del `"="` tiene que ir una `<variable>`.

## Nota de diseño

El `=` aquí es asignación; en `<condicion>` es comparación. Se distinguen por estar antes o después de `TOCAR`.

---
*Convención: `<x>` no terminal · `"x"` terminal · `'"'` la comilla doble como terminal · `{ }` cero o más · `[ ]` cero o uno · `|` alternativa · `<nl>` salto de línea*
