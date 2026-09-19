# Producción 13 · `<nombre_figura>`

**La música** · Gramática BNF de TocaScript · Grupo 8

## La producción

Producción terminal: todas sus alternativas van entre comillas, no abre nada más.

```
13  <nombre_figura> ::= "redonda" | "blanca" | "negra" | "corchea" | "semicorchea" | "fusa"
```

## Cómo se lee

Uno de los seis nombres de duración.

## Qué usa y quién la usa

| | |
|---|---|
| **Terminales que aparecen** (entre comillas) | `"redonda"` · `"blanca"` · `"negra"` · `"corchea"` · `"semicorchea"` · `"fusa"` |
| **No terminales que aparecen** (se abren en otra producción) | ninguno — producción terminal |
| **Producciones que usan `<nombre_figura>`** | `<figura>` |

## Ejemplo válido y su derivación

Cada ejemplo, y debajo el árbol que la gramática construye para él: cada nodo es una producción (con su número) y las hojas son terminales entre comillas. Derivación producida por el parser (`verificar.py`) que implementa estas 33 producciones; en `<identificador>`, `<numero>`, `<texto>` y `<nota>` se muestran directamente las hojas — cada carácter viene de `<letra>`, `<mayuscula>` o `<digito>`.

```
negra
```

```
<nombre_figura> (13)
  "negra"
```

```
corchea
```

```
<nombre_figura> (13)
  "corchea"
```

## Ejemplo inválido

```
cuarto
```

**Por qué no deriva:** `cuarto` no está entre las seis alternativas.

## Nota de diseño

De más larga a más corta: 4 · 2 · 1 · ½ · ¼ · ⅛ tiempos.

---
*Convención: `<x>` no terminal · `"x"` terminal · `'"'` la comilla doble como terminal · `{ }` cero o más · `[ ]` cero o uno · `|` alternativa · `<nl>` salto de línea*
