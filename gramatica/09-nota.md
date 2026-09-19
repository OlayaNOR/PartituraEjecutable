# Producción 9 · `<nota>`

**La música** · Gramática BNF de TocaScript · Grupo 8

## La producción

La producción `<nota>` y, debajo, todas las que abre hasta llegar a los átomos —terminales entre comillas—. Todo en un mismo sitio, como en el tablero.

```
 9  <nota> ::= <nombre_nota> [ "#" | "b" ] <octava>

10  <nombre_nota> ::= "do" | "re" | "mi" | "fa" | "sol" | "la" | "si"
11  <octava> ::= <digito>
32  <digito> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
```

## Cómo se lee

Un nombre de nota, una alteración opcional —sostenido o bemol— y la octava, obligatoria.

## Qué usa y quién la usa

| | |
|---|---|
| **Terminales que aparecen** (entre comillas) | `"#"` · `"b"` |
| **No terminales que aparecen** (se abren en otra producción) | `<nombre_nota>` · `<octava>` |
| **Producciones que usan `<nota>`** | `<evento>` |

## Ejemplo válido y su derivación

Cada ejemplo, y debajo el árbol que la gramática construye para él: cada nodo es una producción (con su número) y las hojas son terminales entre comillas. Derivación producida por el parser (`verificar.py`) que implementa estas 33 producciones; en `<identificador>`, `<numero>`, `<texto>` y `<nota>` se muestran directamente las hojas — cada carácter viene de `<letra>`, `<mayuscula>` o `<digito>`.

```
do4
```

```
<nota> (9)
  <nombre_nota> (10)
    "do"
  <octava> (11)
    <digito> (32)
      "4"
```

```
fa#4
```

```
<nota> (9)
  <nombre_nota> (10)
    "fa"
  "#"
  <octava> (11)
    <digito> (32)
      "4"
```

```
mib3
```

```
<nota> (9)
  <nombre_nota> (10)
    "mi"
  "b"
  <octava> (11)
    <digito> (32)
      "3"
```

## Ejemplo inválido

```
do
fa4#
```

**Por qué no deriva:** `do` sin octava no deriva. `fa4#` tiene la alteración después de la octava; el orden es nombre, alteración, octava.

## Nota de diseño

Las notas se escriben pegadas: `do4` es un solo token para el lexer.

---
*Convención: `<x>` no terminal · `"x"` terminal · `'"'` la comilla doble como terminal · `{ }` cero o más · `[ ]` cero o uno · `|` alternativa · `<nl>` salto de línea*
