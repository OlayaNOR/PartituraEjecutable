# Producción 10 · `<octava>`

**La música** · Gramática BNF de TocaScript · Grupo 8

## La producción

La producción `<octava>` y, debajo, todas las que abre hasta llegar a los átomos —terminales entre comillas—. Todo en un mismo sitio, como en el tablero.

```
10  <octava> ::= <digito>

30  <digito> ::= "0" | "1" | "2" | "..." | "9"
```

## Cómo se lee

Un solo dígito.

## Qué usa y quién la usa

| | |
|---|---|
| **Terminales que aparecen** (entre comillas) | — |
| **No terminales que aparecen** (se abren en otra producción) | `<digito>` |
| **Producciones que usan `<octava>`** | `<nota>` |

## Ejemplo válido

```
do4
sol3
```


## Ejemplo inválido

```
do10
```

**Por qué no deriva:** Dos dígitos no derivan: `<octava>` es un `<digito>`, no una repetición.

## Nota de diseño

`do4` es el do central, 60 en MIDI.

---
*Convención: `<x>` no terminal · `"x"` terminal · `'"'` la comilla doble como terminal · `{ }` cero o más · `[ ]` cero o uno · `|` alternativa · `<nl>` salto de línea*
