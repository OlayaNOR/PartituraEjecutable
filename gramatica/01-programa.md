# Producción 1 · `<programa>`

**Estructura del archivo** · Gramática BNF de TocaScript · Grupo 8

## La producción

La producción `<programa>` y, debajo, todas las que abre hasta llegar a los átomos —terminales entre comillas—. Todo en un mismo sitio, como en el tablero.

```
 1  <programa> ::= <cabecera> { <motivo> | <seccion> | <regla> } <pieza>

 2  <cabecera> ::= "tempo" <numero> <nl>
                   "compas" <texto> <nl>
                   "tonalidad" <texto> <nl>
26  <numero> ::= <digito> { <digito> } [ "." <digito> { <digito> } ]
30  <digito> ::= "0" | "1" | "2" | "..." | "9"
31  <nl> ::= "↵"
27  <texto> ::= '"' { <letra> | <mayuscula> | <digito> | " " | "/" } '"'
28  <letra> ::= "a" | "b" | "c" | "..." | "z"
29  <mayuscula> ::= "A" | "B" | "C" | "..." | "Z"
 4  <motivo> ::= "motivo" <identificador> "{" { <evento> } "}" <nl>
24  <identificador> ::= <letra> { <letra> | <digito> | "_" }
 7  <evento> ::= <nota> ":" <figura> | "[" <nota> { <nota> } "]" ":" <figura> | "silencio" ":" <figura>
 8  <nota> ::= <nombre_nota> [ "#" | "b" ] <octava>
 9  <nombre_nota> ::= "do" | "re" | "mi" | "fa" | "sol" | "la" | "si"
10  <octava> ::= <digito>
11  <figura> ::= <nombre_figura> [ "." ]
12  <nombre_figura> ::= "redonda" | "blanca" | "negra" | "corchea" | "semicorchea" | "fusa"
 5  <seccion> ::= "seccion" <identificador> "tipo" <tipo_seccion>
                  "{" { <evento> | <identificador> } "}" <nl>
 6  <tipo_seccion> ::= "intro" | "estrofa" | "estribillo" | "coda"
13  <regla> ::= "AL" <expresion> "TOCAR" <acciones> <nl>
14  <expresion> ::= <termino> { "O" <termino> }
15  <termino> ::= <factor> { "Y" <factor> }
16  <factor> ::= "NO" <factor> | "(" <expresion> ")" | <condicion> | <variable>
17  <condicion> ::= <operando> <operador> <operando>
19  <operando> ::= <variable> | <valor> | <operando> <op_aritmetico> <operando>
23  <variable> ::= <identificador>
25  <valor> ::= <numero> | "true" | "false" | <texto>
20  <op_aritmetico> ::= "+" | "-" | "*" | "/"
18  <operador> ::= ">" | "<" | ">=" | "<=" | "=" | "<>"
21  <acciones> ::= <accion> { "Y" <accion> }
22  <accion> ::= <variable> "=" <operando> | <identificador>
 3  <pieza> ::= "pieza" <texto> "{" { <identificador> } "}" <nl>
```

## Cómo se lee

Un programa es una cabecera, luego cero o más declaraciones —motivos, secciones y reglas en cualquier orden— y al final la pieza.

## Qué usa y quién la usa

| | |
|---|---|
| **Terminales que aparecen** (entre comillas) | — |
| **No terminales que aparecen** (se abren en otra producción) | `<cabecera>` · `<motivo>` · `<seccion>` · `<regla>` · `<pieza>` |
| **Producciones que usan `<programa>`** | ninguna — es la producción de **arranque** |

## Ejemplo válido

```
tempo 100
compas "4/4"
tonalidad "Do mayor"

motivo frase1 { do4:negra re4:negra }
seccion cancion tipo estrofa { frase1 }
AL es_coda TOCAR dinamica = "pp"

pieza "Fray Santiago" { cancion }
```


## Ejemplo inválido

```
motivo frase1 { do4:negra }
tempo 100
```

**Por qué no deriva:** La cabecera tiene que ir primero: aquí hay un motivo antes de `"tempo"`.

## Nota de diseño

Es la producción de arranque. Las llaves `{ }` de esta línea son notación —«cero o más»—, no llaves del lenguaje: ésas van entre comillas, `"{"`.

---
*Convención: `<x>` no terminal · `"x"` terminal · `'"'` la comilla doble como terminal · `{ }` cero o más · `[ ]` cero o uno · `|` alternativa · `<nl>` salto de línea*
