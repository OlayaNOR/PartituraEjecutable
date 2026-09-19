# Producción 1 · `<programa>`

**Estructura del archivo** · Gramática BNF de TocaScript · Grupo 8

## La producción

La producción `<programa>` y, debajo, todas las que abre hasta llegar a los átomos —terminales entre comillas—. Todo en un mismo sitio, como en el tablero.

```
 1  <programa> ::= <cabecera> { <motivo> | <seccion> | <regla> } <pieza>

 2  <cabecera> ::= <ajuste> <nl>
                   <ajuste> <nl>
                   <ajuste> <nl>
 3  <ajuste> ::= <variable> <valor>
25  <variable> ::= <identificador>
26  <identificador> ::= <letra> { <letra> | <digito> | "_" }
                        # y no puede coincidir con ninguna palabra reservada
30  <letra> ::= "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m"
              | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z"
32  <digito> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
27  <valor> ::= <numero> | "true" | "false" | <texto>
28  <numero> ::= <digito> { <digito> } [ "." <digito> { <digito> } ]
29  <texto> ::= '"' { <letra> | <mayuscula> | <digito> | " " | "/" } '"'
31  <mayuscula> ::= "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M"
                  | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z"
33  <nl> ::= "↵"
 5  <motivo> ::= "motivo" <identificador> "{" { <evento> } "}" <nl>
 8  <evento> ::= <nota> ":" <figura>
               | "[" <nota> { <nota> } "]" ":" <figura>
               | "silencio" ":" <figura>
 9  <nota> ::= <nombre_nota> [ "#" | "b" ] <octava>
10  <nombre_nota> ::= "do" | "re" | "mi" | "fa" | "sol" | "la" | "si"
11  <octava> ::= <digito>
12  <figura> ::= <nombre_figura> [ "." ]
13  <nombre_figura> ::= "redonda" | "blanca" | "negra" | "corchea" | "semicorchea" | "fusa"
 6  <seccion> ::= "seccion" <identificador> "tipo" <tipo_seccion>
                  "{" { <evento> | <identificador> } "}" <nl>
 7  <tipo_seccion> ::= "intro" | "estrofa" | "estribillo" | "coda"
14  <regla> ::= "AL" <expresion> "TOCAR" <acciones> <nl>
15  <expresion> ::= <termino> { "O" <termino> }
16  <termino> ::= <factor> { "Y" <factor> }
17  <factor> ::= "NO" <factor>
               | "(" <expresion> ")"
               | <condicion>
               | <variable>
18  <condicion> ::= <operando> <operador> <operando>
20  <operando> ::= <sumando> { "+" <sumando> | "-" <sumando> }
21  <sumando> ::= <primario> { "*" <primario> | "/" <primario> }
22  <primario> ::= <variable> | <valor> | "(" <operando> ")"
19  <operador> ::= ">" | "<" | ">=" | "<=" | "=" | "<>"
23  <acciones> ::= <accion> { "Y" <accion> }
24  <accion> ::= <variable> "=" <operando>
               | <identificador>
 4  <pieza> ::= "pieza" <texto> "{" { <identificador> } "}" <nl>
```

## Cómo se lee

Un programa es una cabecera, luego cero o más declaraciones —motivos, secciones y reglas en cualquier orden— y al final la pieza.

## Qué usa y quién la usa

| | |
|---|---|
| **Terminales que aparecen** (entre comillas) | — |
| **No terminales que aparecen** (se abren en otra producción) | `<cabecera>` · `<motivo>` · `<seccion>` · `<regla>` · `<pieza>` |
| **Producciones que usan `<programa>`** | ninguna — es la producción de arranque |

## Ejemplo válido y su derivación

Cada ejemplo, y debajo el árbol que la gramática construye para él: cada nodo es una producción (con su número) y las hojas son terminales entre comillas. Derivación producida por el parser (`verificar.py`) que implementa estas 33 producciones; en `<identificador>`, `<numero>`, `<texto>` y `<nota>` se muestran directamente las hojas — cada carácter viene de `<letra>`, `<mayuscula>` o `<digito>`.

```
tempo 100
compas "4/4"
tonalidad "Do mayor"

motivo frase1 { do4:negra re4:negra }
seccion cancion tipo estrofa { frase1 }
AL es_coda TOCAR dinamica = "pp"

pieza "Fray Santiago" { cancion }
```

```
<programa> (1)
  <cabecera> (2)
    <ajuste> (3)  → <variable> <valor>
    <nl> (33)  → "↵"
    <ajuste> (3)  → <variable> <valor>
    <nl> (33)  → "↵"
    <ajuste> (3)  → <variable> <valor>
    <nl> (33)  → "↵"
  <motivo> (5)
    "motivo"
    <identificador> (26)  → <letra> <letra> <letra> <letra> <letra> <digito>
    "{"
    <evento> (8)  → <nota> ":" <figura>
    <evento> (8)  → <nota> ":" <figura>
    "}"
    <nl> (33)  → "↵"
  <seccion> (6)
    "seccion"
    <identificador> (26)  → <letra> <letra> <letra> <letra> <letra> <letra> <letra>
    "tipo"
    <tipo_seccion> (7)  → "estrofa"
    "{"
    <identificador> (26)  → <letra> <letra> <letra> <letra> <letra> <digito>
    "}"
    <nl> (33)  → "↵"
  <regla> (14)
    "AL"
    <expresion> (15)  → <termino>
    "TOCAR"
    <acciones> (23)  → <accion>
    <nl> (33)  → "↵"
  <pieza> (4)
    "pieza"
    <texto> (29)  → '"' <mayuscula> <letra> <letra> <letra> " " <mayuscula> <letra> <letra> <letra> <letra> <letra> <letra> <letra> '"'
    "{"
    <identificador> (26)  → <letra> <letra> <letra> <letra> <letra> <letra> <letra>
    "}"
    <nl> (33)  → "↵"
```

## Ejemplo inválido

```
motivo frase1 { do4:negra }
tempo 100
compas "4/4"
tonalidad "Do mayor"
pieza "x" { }
```

**Por qué no deriva:** La cabecera tiene que ir primero: aquí hay un motivo antes de `tempo`.

## Nota de diseño

Es la producción de arranque: toda derivación empieza aquí. Las llaves `{ }` de esta línea son notación —«cero o más»—, no llaves del lenguaje; ésas van entre comillas, `"{"`.

---
*Convención: `<x>` no terminal · `"x"` terminal · `'"'` la comilla doble como terminal · `{ }` cero o más · `[ ]` cero o uno · `|` alternativa · `<nl>` salto de línea*
