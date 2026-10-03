# Gramática BNF de TocaScript — una producción por archivo

**Grupo 8** · Valeria Alarcón · Andrew García · Nicolás Olaya

33 producciones. Todos los terminales entre comillas; todo se abre hasta `<letra>`, `<digito>` y `<nl>`. Cada ficha trae la producción con todo lo que abre, cómo se lee, qué usa y quién la usa, el ejemplo válido con su árbol de derivación, un ejemplo inválido y la nota de diseño.

## Convención

| Símbolo | Significado |
|---|---|
| `<nombre>` | **No terminal**: se abre en otra producción |
| `"x"` | **Terminal**: se escribe tal cual en el programa. Todos los terminales van entre comillas dobles — palabras clave, símbolos, letras y dígitos |
| `'"'` | La comilla doble como terminal, entre comillas simples porque las dobles ya marcan los demás terminales |
| `::=` | «se define como» |
| `\|` | Alternativa |
| `{ … }` | Repetición: cero o más veces |
| `[ … ]` | Opcional: cero o una vez |
| `<nl>` | Salto de línea. Fuera de llaves cada construcción termina en uno; dentro de `{ }` los saltos cuentan como espacio. Su terminal `"↵"` es el fin de línea del archivo (LF o CR LF) |
| espacio | Los espacios y tabulaciones entre símbolos no se escriben en las producciones: separan terminales consecutivos y el lexer los descarta. Solo dentro de `<texto>` el espacio es un terminal, `" "` |
| `#` | Comentario dentro del bloque: las etiquetas de terminales y no terminales, y las restricciones que el BNF no puede expresar (la de `<identificador>`) |
| líneas en blanco y comentarios | En un programa, las líneas en blanco y los comentarios (`#` al inicio de la línea o tras un espacio, hasta el fin de la línea) los descarta el lexer antes del análisis; no forman parte de la gramática. `#` pegado a una nota es el sostenido, `fa#4` |

## La gramática completa

```
# ═══════════════════════════════════════════════════════════════
#  GRAMÁTICA DE TocaScript · 33 producciones · Grupo 8
# ═══════════════════════════════════════════════════════════════
#
#  Convención:  <x> no terminal · "x" terminal · '"' la comilla doble como terminal
#               ::= se define como · | alternativa · { } cero o más · [ ] opcional
#               <nl> salto de línea (fuera de llaves; dentro cuenta como espacio)
#               los espacios entre símbolos no se escriben: separan terminales y el lexer los descarta
#               # comentario: etiquetas y restricciones que el BNF no puede expresar
#
#  NO TERMINALES (33) — llevan ángulos y se abren en su propia producción:
#    <programa> <cabecera> <ajuste> <pieza> <motivo> <seccion> <tipo_seccion> <evento> <nota> <nombre_nota> <octava>
#    <figura> <nombre_figura> <regla> <expresion> <termino> <factor> <condicion> <operador> <operando> <sumando> <primario>
#    <acciones> <accion> <variable> <identificador> <valor> <numero> <texto> <letra> <mayuscula> <digito> <nl>
#
#  TERMINALES — van entre comillas; ahí termina la derivación y son lo que el lexer reconoce:
#    Palabras clave de la regla  "AL" "TOCAR" "Y" "O" "NO"
#    Impresión (acción)          "mostrar"
#    Palabras clave de la pieza  "motivo" "seccion" "tipo" "pieza" "silencio"
#    Tipos de sección            "intro" "estrofa" "estribillo" "coda"
#    Nombres de nota             "do" "re" "mi" "fa" "sol" "la" "si"
#    Figuras                     "redonda" "blanca" "negra" "corchea" "semicorchea" "fusa"
#    Alteraciones y puntillo     "#" "b" "."
#    Operadores relacionales     ">" "<" ">=" "<=" "=" "<>"
#    Operadores aritméticos      "+" "-" "*" "/"
#    Booleanos                   "true" "false"
#    Símbolos                    "(" ")" "{" "}" "[" "]" ":" "_" " " '"' "↵"
#    Átomos                      "a … z" "A … Z" "0 … 9"
#

# ── Estructura del archivo ──
 1  <programa> ::= <cabecera> { <motivo> | <seccion> | <regla> } <pieza>
 2  <cabecera> ::= <ajuste> <nl>
                   <ajuste> <nl>
                   <ajuste> <nl>
                   { <ajuste> <nl> }
 3  <ajuste> ::= <variable> <valor>
 4  <pieza> ::= "pieza" <texto> "{" { <identificador> } "}" <nl>
 5  <motivo> ::= "motivo" <identificador> "{" { <evento> } "}" <nl>
 6  <seccion> ::= "seccion" <identificador> "tipo" <tipo_seccion>
                  "{" { <evento> | <identificador> } "}" <nl>
 7  <tipo_seccion> ::= "intro" | "estrofa" | "estribillo" | "coda"

# ── La música ──
 8  <evento> ::= <nota> ":" <figura>
               | "[" <nota> { <nota> } "]" ":" <figura>
               | "silencio" ":" <figura>
 9  <nota> ::= <nombre_nota> [ "#" | "b" ] <octava>
10  <nombre_nota> ::= "do" | "re" | "mi" | "fa" | "sol" | "la" | "si"
11  <octava> ::= <digito>
12  <figura> ::= <nombre_figura> [ "." ]
13  <nombre_figura> ::= "redonda" | "blanca" | "negra" | "corchea" | "semicorchea" | "fusa"

# ── La regla de interpretación ──
14  <regla> ::= "AL" <expresion> "TOCAR" <acciones> <nl>
15  <expresion> ::= <termino> { "O" <termino> }
16  <termino> ::= <factor> { "Y" <factor> }
17  <factor> ::= "NO" <factor>
               | "(" <expresion> ")"
               | <condicion>
               | <variable>
18  <condicion> ::= <operando> <operador> <operando>
19  <operador> ::= ">" | "<" | ">=" | "<=" | "=" | "<>"
20  <operando> ::= <sumando> { "+" <sumando> | "-" <sumando> }
21  <sumando> ::= <primario> { "*" <primario> | "/" <primario> }
22  <primario> ::= <variable> | <valor> | "(" <operando> ")"
23  <acciones> ::= <accion> { "Y" <accion> }
24  <accion> ::= <variable> "=" <operando>
               | "mostrar" <operando>
               | <identificador>

# ── Nombres y valores ──
25  <variable> ::= <identificador>
26  <identificador> ::= <letra> { <letra> | <digito> | "_" }
                        # y no puede coincidir con ninguna palabra reservada
27  <valor> ::= <numero> | "true" | "false" | <texto>
28  <numero> ::= <digito> { <digito> } [ "." <digito> { <digito> } ]
29  <texto> ::= '"' { <letra> | <mayuscula> | <digito> | " " | "/" } '"'

# ── Átomos ──
30  <letra> ::= "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m"
              | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z"
31  <mayuscula> ::= "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M"
                  | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z"
32  <digito> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
33  <nl> ::= "↵"
```

## Índice

| # | Producción | Grupo | Archivo |
|---|---|---|---|
| 1 | `<programa>` | Estructura del archivo | [01-programa.md](01-programa.md) |
| 2 | `<cabecera>` | Estructura del archivo | [02-cabecera.md](02-cabecera.md) |
| 3 | `<ajuste>` | Estructura del archivo | [03-ajuste.md](03-ajuste.md) |
| 4 | `<pieza>` | Estructura del archivo | [04-pieza.md](04-pieza.md) |
| 5 | `<motivo>` | Estructura del archivo | [05-motivo.md](05-motivo.md) |
| 6 | `<seccion>` | Estructura del archivo | [06-seccion.md](06-seccion.md) |
| 7 | `<tipo_seccion>` | Estructura del archivo | [07-tipo-seccion.md](07-tipo-seccion.md) |
| 8 | `<evento>` | La música | [08-evento.md](08-evento.md) |
| 9 | `<nota>` | La música | [09-nota.md](09-nota.md) |
| 10 | `<nombre_nota>` | La música | [10-nombre-nota.md](10-nombre-nota.md) |
| 11 | `<octava>` | La música | [11-octava.md](11-octava.md) |
| 12 | `<figura>` | La música | [12-figura.md](12-figura.md) |
| 13 | `<nombre_figura>` | La música | [13-nombre-figura.md](13-nombre-figura.md) |
| 14 | `<regla>` | La regla de interpretación | [14-regla.md](14-regla.md) |
| 15 | `<expresion>` | La regla de interpretación | [15-expresion.md](15-expresion.md) |
| 16 | `<termino>` | La regla de interpretación | [16-termino.md](16-termino.md) |
| 17 | `<factor>` | La regla de interpretación | [17-factor.md](17-factor.md) |
| 18 | `<condicion>` | La regla de interpretación | [18-condicion.md](18-condicion.md) |
| 19 | `<operador>` | La regla de interpretación | [19-operador.md](19-operador.md) |
| 20 | `<operando>` | La regla de interpretación | [20-operando.md](20-operando.md) |
| 21 | `<sumando>` | La regla de interpretación | [21-sumando.md](21-sumando.md) |
| 22 | `<primario>` | La regla de interpretación | [22-primario.md](22-primario.md) |
| 23 | `<acciones>` | La regla de interpretación | [23-acciones.md](23-acciones.md) |
| 24 | `<accion>` | La regla de interpretación | [24-accion.md](24-accion.md) |
| 25 | `<variable>` | Nombres y valores | [25-variable.md](25-variable.md) |
| 26 | `<identificador>` | Nombres y valores | [26-identificador.md](26-identificador.md) |
| 27 | `<valor>` | Nombres y valores | [27-valor.md](27-valor.md) |
| 28 | `<numero>` | Nombres y valores | [28-numero.md](28-numero.md) |
| 29 | `<texto>` | Nombres y valores | [29-texto.md](29-texto.md) |
| 30 | `<letra>` | Átomos | [30-letra.md](30-letra.md) |
| 31 | `<mayuscula>` | Átomos | [31-mayuscula.md](31-mayuscula.md) |
| 32 | `<digito>` | Átomos | [32-digito.md](32-digito.md) |
| 33 | `<nl>` | Átomos | [33-nl.md](33-nl.md) |
