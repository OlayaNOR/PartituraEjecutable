# Producción 28 · `<letra>`

**Átomos** · Gramática BNF de TocaScript · Grupo 8

## La producción

Producción terminal: todas sus alternativas van entre comillas, no abre nada más.

```
28  <letra> ::= "a" | "b" | "c" | "..." | "z"
```

## Cómo se lee

Una de las 26 letras minúsculas del alfabeto inglés.

## Qué usa y quién la usa

| | |
|---|---|
| **Terminales que aparecen** (entre comillas) | `"a"` · `"b"` · `"c"` · `"..."` · `"z"` |
| **No terminales que aparecen** (se abren en otra producción) | ninguno — es una producción **terminal**: todas sus alternativas van entre comillas |
| **Producciones que usan `<letra>`** | `<identificador>` · `<texto>` |

## Ejemplo válido

```
q
```


## Ejemplo inválido

```
á
ñ
```

**Por qué no deriva:** Las letras con tilde y la eñe no están entre las alternativas, a propósito, para que el lexer no dependa de la codificación del archivo.

## Nota de diseño

Átomo: no se abre en nada más.

---
*Convención: `<x>` no terminal · `"x"` terminal · `'"'` la comilla doble como terminal · `{ }` cero o más · `[ ]` cero o uno · `|` alternativa · `<nl>` salto de línea*
