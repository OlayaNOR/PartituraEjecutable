# Producción 29 · `<mayuscula>`

**Átomos** · Gramática BNF de TocaScript · Grupo 8

## La producción

Producción terminal: todas sus alternativas van entre comillas, no abre nada más.

```
29  <mayuscula> ::= "A" | "B" | "C" | "..." | "Z"
```

## Cómo se lee

Una de las 26 letras mayúsculas.

## Qué usa y quién la usa

| | |
|---|---|
| **Terminales que aparecen** (entre comillas) | `"A"` · `"B"` · `"C"` · `"..."` · `"Z"` |
| **No terminales que aparecen** (se abren en otra producción) | ninguno — es una producción **terminal**: todas sus alternativas van entre comillas |
| **Producciones que usan `<mayuscula>`** | `<texto>` |

## Ejemplo válido

```
D
```


## Ejemplo inválido

```
É
```

**Por qué no deriva:** Sin tildes, por la misma razón que `<letra>`.

## Nota de diseño

Solo se usa dentro de `<texto>`, para títulos y tonalidades como `"Do mayor"`.

---
*Convención: `<x>` no terminal · `"x"` terminal · `'"'` la comilla doble como terminal · `{ }` cero o más · `[ ]` cero o uno · `|` alternativa · `<nl>` salto de línea*
