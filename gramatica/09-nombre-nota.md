# Producción 9 · `<nombre_nota>`

**La música** · Gramática BNF de TocaScript · Grupo 8

## La producción

Producción terminal: todas sus alternativas van entre comillas, no abre nada más.

```
 9  <nombre_nota> ::= "do" | "re" | "mi" | "fa" | "sol" | "la" | "si"
```

## Cómo se lee

Uno de los siete nombres de nota.

## Qué usa y quién la usa

| | |
|---|---|
| **Terminales que aparecen** (entre comillas) | `"do"` · `"re"` · `"mi"` · `"fa"` · `"sol"` · `"la"` · `"si"` |
| **No terminales que aparecen** (se abren en otra producción) | ninguno — es una producción **terminal**: todas sus alternativas van entre comillas |
| **Producciones que usan `<nombre_nota>`** | `<nota>` |

## Ejemplo válido

```
do
sol
```


## Ejemplo inválido

```
C
Do
```

**Por qué no deriva:** `C` es notación anglosajona, no del lenguaje. `Do` con mayúscula no es la alternativa `"do"`.

## Nota de diseño

Se usa el solfeo —do, re, mi— porque es la notación que un músico hispanohablante ya conoce.

---
*Convención: `<x>` no terminal · `"x"` terminal · `'"'` la comilla doble como terminal · `{ }` cero o más · `[ ]` cero o uno · `|` alternativa · `<nl>` salto de línea*
