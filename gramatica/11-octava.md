# Producción 11 · `<octava>`

**La música** · Gramática BNF de TocaScript · Grupo 8

## La producción

La producción `<octava>` y, debajo, todas las que abre hasta llegar a los átomos —terminales entre comillas—. Todo en un mismo sitio, como en el tablero.

```
11  <octava> ::= <digito>

32  <digito> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
```

## Cómo se lee

Un solo dígito.

## Qué usa y quién la usa

| | |
|---|---|
| **Terminales que aparecen** (entre comillas) | — |
| **No terminales que aparecen** (se abren en otra producción) | `<digito>` |
| **Producciones que usan `<octava>`** | `<nota>` |

## Ejemplo válido y su derivación

Cada ejemplo, y debajo el árbol que la gramática construye para él: cada nodo es una producción (con su número) y las hojas son terminales entre comillas. Derivación producida por el parser (`verificar.py`) que implementa estas 33 producciones; en `<identificador>`, `<numero>`, `<texto>` y `<nota>` se muestran directamente las hojas — cada carácter viene de `<letra>`, `<mayuscula>` o `<digito>`.

```
4
```

```
<octava> (11)
  <digito> (32)
    "4"
```

```
3
```

```
<octava> (11)
  <digito> (32)
    "3"
```

## Ejemplo inválido

```
10
```

**Por qué no deriva:** Dos dígitos no derivan: `<octava>` es un `<digito>`, no una repetición.

## Nota de diseño

`do4` es el do central, 60 en MIDI.

---
*Convención: `<x>` no terminal · `"x"` terminal · `'"'` la comilla doble como terminal · `{ }` cero o más · `[ ]` cero o uno · `|` alternativa · `<nl>` salto de línea*
