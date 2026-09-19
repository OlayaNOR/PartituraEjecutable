# Producción 19 · `<operador>`

**La regla de interpretación** · Gramática BNF de TocaScript · Grupo 8

## La producción

Producción terminal: todas sus alternativas van entre comillas, no abre nada más.

```
19  <operador> ::= ">" | "<" | ">=" | "<=" | "=" | "<>"
```

## Cómo se lee

Los seis signos de comparación.

## Qué usa y quién la usa

| | |
|---|---|
| **Terminales que aparecen** (entre comillas) | `">"` · `"<"` · `">="` · `"<="` · `"="` · `"<>"` |
| **No terminales que aparecen** (se abren en otra producción) | ninguno — producción terminal |
| **Producciones que usan `<operador>`** | `<condicion>` |

## Ejemplo válido y su derivación

Cada ejemplo, y debajo el árbol que la gramática construye para él: cada nodo es una producción (con su número) y las hojas son terminales entre comillas. Derivación producida por el parser (`verificar.py`) que implementa estas 33 producciones; en `<identificador>`, `<numero>`, `<texto>` y `<nota>` se muestran directamente las hojas — cada carácter viene de `<letra>`, `<mayuscula>` o `<digito>`.

```
>=
```

```
<operador> (19)
  ">="
```

```
<>
```

```
<operador> (19)
  "<>"
```

## Ejemplo inválido

```
=>
```

**Por qué no deriva:** `=>` no está entre las alternativas; el símbolo es `">="`.

## Nota de diseño

Producción terminal: ninguna alternativa se abre en nada más.

---
*Convención: `<x>` no terminal · `"x"` terminal · `'"'` la comilla doble como terminal · `{ }` cero o más · `[ ]` cero o uno · `|` alternativa · `<nl>` salto de línea*
