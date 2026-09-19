# Producción 30 · `<digito>`

**Átomos** · Gramática BNF de TocaScript · Grupo 8

## La producción

Producción terminal: todas sus alternativas van entre comillas, no abre nada más.

```
30  <digito> ::= "0" | "1" | "2" | "..." | "9"
```

## Cómo se lee

Uno de los diez dígitos.

## Qué usa y quién la usa

| | |
|---|---|
| **Terminales que aparecen** (entre comillas) | `"0"` · `"1"` · `"2"` · `"..."` · `"9"` |
| **No terminales que aparecen** (se abren en otra producción) | ninguno — es una producción **terminal**: todas sus alternativas van entre comillas |
| **Producciones que usan `<digito>`** | `<octava>` · `<identificador>` · `<numero>` · `<texto>` |

## Ejemplo válido

```
7
```


## Ejemplo inválido

```
x
```

**Por qué no deriva:** No es un dígito.

## Nota de diseño

Átomo: no se abre en nada más.

---
*Convención: `<x>` no terminal · `"x"` terminal · `'"'` la comilla doble como terminal · `{ }` cero o más · `[ ]` cero o uno · `|` alternativa · `<nl>` salto de línea*
