# Producción 7 · `<tipo_seccion>`

**Estructura del archivo** · Gramática BNF de TocaScript · Grupo 8

## La producción

Producción terminal: todas sus alternativas van entre comillas, no abre nada más.

```
 7  <tipo_seccion> ::= "intro" | "estrofa" | "estribillo" | "coda"
```

## Cómo se lee

Una de cuatro palabras.

## Qué usa y quién la usa

| | |
|---|---|
| **Terminales que aparecen** (entre comillas) | `"intro"` · `"estrofa"` · `"estribillo"` · `"coda"` |
| **No terminales que aparecen** (se abren en otra producción) | ninguno — producción terminal |
| **Producciones que usan `<tipo_seccion>`** | `<seccion>` |

## Ejemplo válido y su derivación

Cada ejemplo, y debajo el árbol que la gramática construye para él: cada nodo es una producción (con su número) y las hojas son terminales entre comillas. Derivación producida por el parser (`verificar.py`) que implementa estas 33 producciones; en `<identificador>`, `<numero>`, `<texto>` y `<nota>` se muestran directamente las hojas — cada carácter viene de `<letra>`, `<mayuscula>` o `<digito>`.

```
tipo estrofa
```

```
<tipo_seccion> (7)
  "estrofa"
```

```
tipo coda
```

```
<tipo_seccion> (7)
  "coda"
```

## Ejemplo inválido

```
tipo puente
```

**Por qué no deriva:** `puente` no está entre las cuatro alternativas.

## Nota de diseño

Cada tipo enciende su variable booleana: `intro` → `es_intro`, `estrofa` → `es_estrofa`, `estribillo` → `es_estribillo`, `coda` → `es_coda`.

---
*Convención: `<x>` no terminal · `"x"` terminal · `'"'` la comilla doble como terminal · `{ }` cero o más · `[ ]` cero o uno · `|` alternativa · `<nl>` salto de línea*
