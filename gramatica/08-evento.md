# Producción 8 · `<evento>`

**La música** · Gramática BNF de TocaScript · Grupo 8

## La producción

La producción `<evento>` y, debajo, todas las que abre hasta llegar a los átomos —terminales entre comillas—. Todo en un mismo sitio, como en el tablero.

```
 8  <evento> ::= <nota> ":" <figura>
               | "[" <nota> { <nota> } "]" ":" <figura>
               | "silencio" ":" <figura>

 9  <nota> ::= <nombre_nota> [ "#" | "b" ] <octava>
10  <nombre_nota> ::= "do" | "re" | "mi" | "fa" | "sol" | "la" | "si"
11  <octava> ::= <digito>
32  <digito> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
12  <figura> ::= <nombre_figura> [ "." ]
13  <nombre_figura> ::= "redonda" | "blanca" | "negra" | "corchea" | "semicorchea" | "fusa"
```

## Cómo se lee

Una nota con su figura; o varias notas entre corchetes —un acorde— con su figura; o la palabra `silencio` con su figura.

## Qué usa y quién la usa

| | |
|---|---|
| **Terminales que aparecen** (entre comillas) | `":"` · `"["` · `"]"` · `":"` · `"silencio"` · `":"` |
| **No terminales que aparecen** (se abren en otra producción) | `<nota>` · `<figura>` |
| **Producciones que usan `<evento>`** | `<motivo>` · `<seccion>` |

## Ejemplo válido y su derivación

Cada ejemplo, y debajo el árbol que la gramática construye para él: cada nodo es una producción (con su número) y las hojas son terminales entre comillas. Derivación producida por el parser (`verificar.py`) que implementa estas 33 producciones; en `<identificador>`, `<numero>`, `<texto>` y `<nota>` se muestran directamente las hojas — cada carácter viene de `<letra>`, `<mayuscula>` o `<digito>`.

```
do4:negra
```

```
<evento> (8)
  <nota> (9)  → "do" "4"
  ":"
  <figura> (12)
    <nombre_figura> (13)
      "negra"
```

```
[do3 mi3 sol3 do4]:redonda
```

```
<evento> (8)
  "["
  <nota> (9)  → "do" "3"
  <nota> (9)  → "mi" "3"
  <nota> (9)  → "sol" "3"
  <nota> (9)  → "do" "4"
  "]"
  ":"
  <figura> (12)
    <nombre_figura> (13)
      "redonda"
```

```
silencio:redonda
```

```
<evento> (8)
  "silencio"
  ":"
  <figura> (12)
    <nombre_figura> (13)
      "redonda"
```

## Ejemplo inválido

```
do4
[do3 mi3]
```

**Por qué no deriva:** A los dos les falta `":" <figura>`. La figura es obligatoria: en música todo dura algo, incluso el silencio.

## Nota de diseño

Los corchetes van entre comillas porque son símbolos del lenguaje, no el «opcional» de la notación.

---
*Convención: `<x>` no terminal · `"x"` terminal · `'"'` la comilla doble como terminal · `{ }` cero o más · `[ ]` cero o uno · `|` alternativa · `<nl>` salto de línea*
