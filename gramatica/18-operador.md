# Producción 18 · `<operador>`

**La regla de interpretación** · Gramática BNF de TocaScript · Grupo 8

## La producción

Producción terminal: todas sus alternativas van entre comillas, no abre nada más.

```
18  <operador> ::= ">" | "<" | ">=" | "<=" | "=" | "<>"
```

## Cómo se lee

Los seis signos de comparación.

## Qué usa y quién la usa

| | |
|---|---|
| **Terminales que aparecen** (entre comillas) | `">"` · `"<"` · `">="` · `"<="` · `"="` · `"<>"` |
| **No terminales que aparecen** (se abren en otra producción) | ninguno — es una producción **terminal**: todas sus alternativas van entre comillas |
| **Producciones que usan `<operador>`** | `<condicion>` |

## Ejemplo válido

```
num_voces >= 4
tempo <> 120
```


## Ejemplo inválido

```
num_voces => 4
```

**Por qué no deriva:** `=>` no está entre las alternativas; el símbolo es `">="`.

## Nota de diseño

Producción terminal: ninguna alternativa se abre en nada más.

---
*Convención: `<x>` no terminal · `"x"` terminal · `'"'` la comilla doble como terminal · `{ }` cero o más · `[ ]` cero o uno · `|` alternativa · `<nl>` salto de línea*
