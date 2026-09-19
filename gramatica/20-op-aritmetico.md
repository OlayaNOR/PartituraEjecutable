# Producción 20 · `<op_aritmetico>`

**La regla de interpretación** · Gramática BNF de TocaScript · Grupo 8

## La producción

Producción terminal: todas sus alternativas van entre comillas, no abre nada más.

```
20  <op_aritmetico> ::= "+" | "-" | "*" | "/"
```

## Cómo se lee

Las cuatro operaciones.

## Qué usa y quién la usa

| | |
|---|---|
| **Terminales que aparecen** (entre comillas) | `"+"` · `"-"` · `"*"` · `"/"` |
| **No terminales que aparecen** (se abren en otra producción) | ninguno — es una producción **terminal**: todas sus alternativas van entre comillas |
| **Producciones que usan `<op_aritmetico>`** | `<operando>` |

## Ejemplo válido

```
tempo - 10
tempo * 0.85
```


## Ejemplo inválido

```
tempo ^ 2
```

**Por qué no deriva:** `^` no está entre las alternativas.

## Nota de diseño

El `"/"` también aparece dentro de `"4/4"`, pero ahí está entre comillas y es parte de un `<texto>`, no un operador.

---
*Convención: `<x>` no terminal · `"x"` terminal · `'"'` la comilla doble como terminal · `{ }` cero o más · `[ ]` cero o uno · `|` alternativa · `<nl>` salto de línea*
