# Producción 31 · `<mayuscula>`

**Átomos** · Gramática BNF de TocaScript · Grupo 8

## La producción

Producción terminal: todas sus alternativas van entre comillas, no abre nada más.

```
31  <mayuscula> ::= "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M"
                  | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z"
```

## Cómo se lee

Una de las 26 letras mayúsculas.

## Qué usa y quién la usa

| | |
|---|---|
| **Terminales que aparecen** (entre comillas) | `"A"` · `"B"` · `"C"` · `"D"` · `"E"` · `"F"` · `"G"` · `"H"` · `"I"` · `"J"` · `"K"` · `"L"` · `"M"` · `"N"` · `"O"` · `"P"` · `"Q"` · `"R"` · `"S"` · `"T"` · `"U"` · `"V"` · `"W"` · `"X"` · `"Y"` · `"Z"` |
| **No terminales que aparecen** (se abren en otra producción) | ninguno — producción terminal |
| **Producciones que usan `<mayuscula>`** | `<texto>` |

## Ejemplo válido y su derivación

Cada ejemplo, y debajo el árbol que la gramática construye para él: cada nodo es una producción (con su número) y las hojas son terminales entre comillas. Derivación producida por el parser (`verificar.py`) que implementa estas 33 producciones; en `<identificador>`, `<numero>`, `<texto>` y `<nota>` se muestran directamente las hojas — cada carácter viene de `<letra>`, `<mayuscula>` o `<digito>`.

```
D
```

```
<mayuscula> (31)
  "D"
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
