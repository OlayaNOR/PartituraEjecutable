# Producción 5 · `<motivo>`

**Estructura del archivo** · Gramática BNF de TocaScript · Grupo 8

## La producción

La producción `<motivo>` y, debajo, todas las que abre hasta llegar a los átomos —terminales entre comillas—. Todo en un mismo sitio, como en el tablero.

```
 5  <motivo> ::= "motivo" <identificador> "{" { <evento> } "}" <nl>

26  <identificador> ::= <letra> { <letra> | <digito> | "_" }
                        # y no puede coincidir con ninguna palabra reservada
30  <letra> ::= "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m"
              | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z"
32  <digito> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
 8  <evento> ::= <nota> ":" <figura>
               | "[" <nota> { <nota> } "]" ":" <figura>
               | "silencio" ":" <figura>
 9  <nota> ::= <nombre_nota> [ "#" | "b" ] <octava>
10  <nombre_nota> ::= "do" | "re" | "mi" | "fa" | "sol" | "la" | "si"
11  <octava> ::= <digito>
12  <figura> ::= <nombre_figura> [ "." ]
13  <nombre_figura> ::= "redonda" | "blanca" | "negra" | "corchea" | "semicorchea" | "fusa"
33  <nl> ::= "↵"
```

## Cómo se lee

La palabra `motivo`, un nombre, y entre llaves cero o más eventos. Termina en salto de línea.

## Qué usa y quién la usa

| | |
|---|---|
| **Terminales que aparecen** (entre comillas) | `"motivo"` · `"{"` · `"}"` |
| **No terminales que aparecen** (se abren en otra producción) | `<identificador>` · `<evento>` · `<nl>` |
| **Producciones que usan `<motivo>`** | `<programa>` |

## Ejemplo válido y su derivación

Cada ejemplo, y debajo el árbol que la gramática construye para él: cada nodo es una producción (con su número) y las hojas son terminales entre comillas. Derivación producida por el parser (`verificar.py`) que implementa estas 33 producciones; en `<identificador>`, `<numero>`, `<texto>` y `<nota>` se muestran directamente las hojas — cada carácter viene de `<letra>`, `<mayuscula>` o `<digito>`.

```
motivo frase1 { do4:negra re4:negra mi4:negra do4:negra }
```

```
<motivo> (5)
  "motivo"
  <identificador> (26)  → "f" "r" "a" "s" "e" "1"
  "{"
  <evento> (8)
    <nota> (9)  → "do" "4"
    ":"
    <figura> (12)
      <nombre_figura> (13)
        "negra"
  <evento> (8)
    <nota> (9)  → "re" "4"
    ":"
    <figura> (12)
      <nombre_figura> (13)
        "negra"
  <evento> (8)
    <nota> (9)  → "mi" "4"
    ":"
    <figura> (12)
      <nombre_figura> (13)
        "negra"
  <evento> (8)
    <nota> (9)  → "do" "4"
    ":"
    <figura> (12)
      <nombre_figura> (13)
        "negra"
  "}"
  <nl> (33)  → "↵"
```

## Ejemplo inválido

```
motivo frase1 do4:negra re4:negra
```

**Por qué no deriva:** Faltan las llaves `"{"` y `"}"`.

## Nota de diseño

Dentro de las llaves los saltos de línea cuentan como espacio; el `<nl>` obligatorio es el que va tras la llave de cierre.

---
*Convención: `<x>` no terminal · `"x"` terminal · `'"'` la comilla doble como terminal · `{ }` cero o más · `[ ]` cero o uno · `|` alternativa · `<nl>` salto de línea*
