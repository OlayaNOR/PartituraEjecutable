# Producción 21 · `<acciones>`

**La regla de interpretación** · Gramática BNF de TocaScript · Grupo 8

## La producción

La producción `<acciones>` y, debajo, todas las que abre hasta llegar a los átomos —terminales entre comillas—. Todo en un mismo sitio, como en el tablero.

```
21  <acciones> ::= <accion> { "Y" <accion> }

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

Una acción, o varias unidas por `Y`.

## Qué usa y quién la usa

| | |
|---|---|
| **Terminales que aparecen** (entre comillas) | `"Y"` |
| **No terminales que aparecen** (se abren en otra producción) | `<accion>` |
| **Producciones que usan `<acciones>`** | `<regla>` |

## Ejemplo válido

```
dinamica = "fff" Y duplicar_octava
```


## Ejemplo inválido

```
dinamica = "fff", duplicar_octava
```

**Por qué no deriva:** Las acciones se unen con `"Y"`, no con coma.

## Nota de diseño

Aquí `Y` no compara: significa «y además». Lo distingue estar después de `TOCAR`.

---
*Convención: `<x>` no terminal · `"x"` terminal · `'"'` la comilla doble como terminal · `{ }` cero o más · `[ ]` cero o uno · `|` alternativa · `<nl>` salto de línea*
