# Producción 32 · `<digito>`

**Átomos** · Gramática BNF de TocaScript · Grupo 8

## La producción

Producción terminal: todas sus alternativas van entre comillas, no abre nada más.

```
32  <digito> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
```

## Cómo se lee

Uno de los diez dígitos.

## Qué usa y quién la usa

| | |
|---|---|
| **Terminales que aparecen** (entre comillas) | `"0"` · `"1"` · `"2"` · `"3"` · `"4"` · `"5"` · `"6"` · `"7"` · `"8"` · `"9"` |
| **No terminales que aparecen** (se abren en otra producción) | ninguno — producción terminal |
| **Producciones que usan `<digito>`** | `<octava>` · `<identificador>` · `<numero>` · `<texto>` |

## Ejemplo válido y su derivación

Cada ejemplo, y debajo el árbol que la gramática construye para él: cada nodo es una producción (con su número) y las hojas son terminales entre comillas. Derivación producida por el parser (`verificar.py`) que implementa estas 33 producciones; en `<identificador>`, `<numero>`, `<texto>` y `<nota>` se muestran directamente las hojas — cada carácter viene de `<letra>`, `<mayuscula>` o `<digito>`.

```
7
```

```
<digito> (32)
  "7"
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
