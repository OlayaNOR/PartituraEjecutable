# Producción 11 · `<figura>`

**La música** · Gramática BNF de TocaScript · Grupo 8

## La producción

La producción `<figura>` y, debajo, todas las que abre hasta llegar a los átomos —terminales entre comillas—. Todo en un mismo sitio, como en el tablero.

```
11  <figura> ::= <nombre_figura> [ "." ]

12  <nombre_figura> ::= "redonda" | "blanca" | "negra" | "corchea" | "semicorchea" | "fusa"
```

## Cómo se lee

Un nombre de figura con un puntillo opcional.

## Qué usa y quién la usa

| | |
|---|---|
| **Terminales que aparecen** (entre comillas) | `"."` |
| **No terminales que aparecen** (se abren en otra producción) | `<nombre_figura>` |
| **Producciones que usan `<figura>`** | `<evento>` |

## Ejemplo válido

```
:negra
:negra.
```


## Ejemplo inválido

```
:negra..
```

**Por qué no deriva:** El puntillo es opcional pero uno solo: `[ "." ]` es cero o una vez.

## Nota de diseño

El puntillo alarga la figura la mitad de su valor, como en la partitura.

---
*Convención: `<x>` no terminal · `"x"` terminal · `'"'` la comilla doble como terminal · `{ }` cero o más · `[ ]` cero o uno · `|` alternativa · `<nl>` salto de línea*
