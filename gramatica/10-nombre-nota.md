# Producción 10 · `<nombre_nota>`

**La música** · Gramática BNF de TocaScript · Grupo 8

## La producción

Producción terminal: todas sus alternativas van entre comillas, no abre nada más.

```
10  <nombre_nota> ::= "do" | "re" | "mi" | "fa" | "sol" | "la" | "si"
```

## Cómo se lee

Uno de los siete nombres de nota.

## Qué usa y quién la usa

| | |
|---|---|
| **Terminales que aparecen** (entre comillas) | `"do"` · `"re"` · `"mi"` · `"fa"` · `"sol"` · `"la"` · `"si"` |
| **No terminales que aparecen** (se abren en otra producción) | ninguno — producción terminal |
| **Producciones que usan `<nombre_nota>`** | `<nota>` |

## Ejemplo válido y su derivación

Cada ejemplo, y debajo el árbol que la gramática construye para él: cada nodo es una producción (con su número) y las hojas son terminales entre comillas. Derivación producida por el parser (`verificar.py`) que implementa estas 33 producciones; en `<identificador>`, `<numero>`, `<texto>` y `<nota>` se muestran directamente las hojas — cada carácter viene de `<letra>`, `<mayuscula>` o `<digito>`.

```
do
```

```
<nombre_nota> (10)
  "do"
```

```
sol
```

```
<nombre_nota> (10)
  "sol"
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
