# Producción 6 · `<seccion>`

**Estructura del archivo** · Gramática BNF de TocaScript · Grupo 8

## La producción

La producción `<seccion>` y, debajo, todas las que abre hasta llegar a los átomos —terminales entre comillas—. Todo en un mismo sitio, como en el tablero.

```
 6  <seccion> ::= "seccion" <identificador> "tipo" <tipo_seccion>
                  "{" { <evento> | <identificador> } "}" <nl>

26  <identificador> ::= <letra> { <letra> | <digito> | "_" }
                        # y no puede coincidir con ninguna palabra reservada
30  <letra> ::= "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m"
              | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z"
32  <digito> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
 7  <tipo_seccion> ::= "intro" | "estrofa" | "estribillo" | "coda"
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

La palabra `seccion`, un nombre, la palabra `tipo`, el tipo de sección, y entre llaves eventos o nombres de motivos. Termina en salto de línea.

## Qué usa y quién la usa

| | |
|---|---|
| **Terminales que aparecen** (entre comillas) | `"seccion"` · `"tipo"` · `"{"` · `"}"` |
| **No terminales que aparecen** (se abren en otra producción) | `<identificador>` · `<tipo_seccion>` · `<evento>` · `<nl>` |
| **Producciones que usan `<seccion>`** | `<programa>` |

## Ejemplo válido y su derivación

Cada ejemplo, y debajo el árbol que la gramática construye para él: cada nodo es una producción (con su número) y las hojas son terminales entre comillas. Derivación producida por el parser (`verificar.py`) que implementa estas 33 producciones; en `<identificador>`, `<numero>`, `<texto>` y `<nota>` se muestran directamente las hojas — cada carácter viene de `<letra>`, `<mayuscula>` o `<digito>`.

```
seccion cancion tipo estrofa { frase1 frase1 frase2 frase2 }
```

```
<seccion> (6)
  "seccion"
  <identificador> (26)  → "c" "a" "n" "c" "i" "o" "n"
  "tipo"
  <tipo_seccion> (7)
    "estrofa"
  "{"
  <identificador> (26)  → "f" "r" "a" "s" "e" "1"
  <identificador> (26)  → "f" "r" "a" "s" "e" "1"
  <identificador> (26)  → "f" "r" "a" "s" "e" "2"
  <identificador> (26)  → "f" "r" "a" "s" "e" "2"
  "}"
  <nl> (33)  → "↵"
```

```
seccion cierre tipo coda { [do3 mi3 sol3 do4]:redonda }
```

```
<seccion> (6)
  "seccion"
  <identificador> (26)  → "c" "i" "e" "r" "r" "e"
  "tipo"
  <tipo_seccion> (7)
    "coda"
  "{"
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
  "}"
  <nl> (33)  → "↵"
```

## Ejemplo inválido

```
seccion cancion { frase1 }
```

**Por qué no deriva:** Falta `"tipo" <tipo_seccion>`, que es obligatorio.

## Nota de diseño

El tipo es la bisagra entre las dos mitades del lenguaje: declarar `tipo estrofa` es lo que pone `es_estrofa` en `true` mientras suena la sección.

---
*Convención: `<x>` no terminal · `"x"` terminal · `'"'` la comilla doble como terminal · `{ }` cero o más · `[ ]` cero o uno · `|` alternativa · `<nl>` salto de línea*
