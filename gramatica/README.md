# Gramática BNF de TocaScript — una producción por archivo

**Grupo 8** · Valeria Alarcón · Andrew García · Nicolás Olaya

31 producciones. Todos los terminales van entre comillas y todo se abre hasta `<letra>`, `<digito>` y `<nl>`: ninguna categoría queda sin definir.

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
| `<nl>` | Salto de línea. Fuera de llaves cada construcción termina en uno; dentro de `{ }` los saltos cuentan como espacio |

## La gramática completa

```

# ── Estructura del archivo ──
 1  <programa> ::= <cabecera> { <motivo> | <seccion> | <regla> } <pieza>
 2  <cabecera> ::= "tempo" <numero> <nl>
                   "compas" <texto> <nl>
                   "tonalidad" <texto> <nl>
 3  <pieza> ::= "pieza" <texto> "{" { <identificador> } "}" <nl>
 4  <motivo> ::= "motivo" <identificador> "{" { <evento> } "}" <nl>
 5  <seccion> ::= "seccion" <identificador> "tipo" <tipo_seccion>
                  "{" { <evento> | <identificador> } "}" <nl>
 6  <tipo_seccion> ::= "intro" | "estrofa" | "estribillo" | "coda"

# ── La música ──
 7  <evento> ::= <nota> ":" <figura> | "[" <nota> { <nota> } "]" ":" <figura> | "silencio" ":" <figura>
 8  <nota> ::= <nombre_nota> [ "#" | "b" ] <octava>
 9  <nombre_nota> ::= "do" | "re" | "mi" | "fa" | "sol" | "la" | "si"
10  <octava> ::= <digito>
11  <figura> ::= <nombre_figura> [ "." ]
12  <nombre_figura> ::= "redonda" | "blanca" | "negra" | "corchea" | "semicorchea" | "fusa"

# ── La regla de interpretación ──
13  <regla> ::= "AL" <expresion> "TOCAR" <acciones> <nl>
14  <expresion> ::= <termino> { "O" <termino> }
15  <termino> ::= <factor> { "Y" <factor> }
16  <factor> ::= "NO" <factor> | "(" <expresion> ")" | <condicion> | <variable>
17  <condicion> ::= <operando> <operador> <operando>
18  <operador> ::= ">" | "<" | ">=" | "<=" | "=" | "<>"
19  <operando> ::= <variable> | <valor> | <operando> <op_aritmetico> <operando>
20  <op_aritmetico> ::= "+" | "-" | "*" | "/"
21  <acciones> ::= <accion> { "Y" <accion> }
22  <accion> ::= <variable> "=" <operando> | <identificador>

# ── Nombres y valores ──
23  <variable> ::= <identificador>
24  <identificador> ::= <letra> { <letra> | <digito> | "_" }
25  <valor> ::= <numero> | "true" | "false" | <texto>
26  <numero> ::= <digito> { <digito> } [ "." <digito> { <digito> } ]
27  <texto> ::= '"' { <letra> | <mayuscula> | <digito> | " " | "/" } '"'

# ── Átomos ──
28  <letra> ::= "a" | "b" | "c" | "..." | "z"
29  <mayuscula> ::= "A" | "B" | "C" | "..." | "Z"
30  <digito> ::= "0" | "1" | "2" | "..." | "9"
31  <nl> ::= "↵"
```

## Índice

| # | Producción | Grupo | Archivo |
|---|---|---|---|
| 1 | `<programa>` | Estructura del archivo | [01-programa.md](01-programa.md) |
| 2 | `<cabecera>` | Estructura del archivo | [02-cabecera.md](02-cabecera.md) |
| 3 | `<pieza>` | Estructura del archivo | [03-pieza.md](03-pieza.md) |
| 4 | `<motivo>` | Estructura del archivo | [04-motivo.md](04-motivo.md) |
| 5 | `<seccion>` | Estructura del archivo | [05-seccion.md](05-seccion.md) |
| 6 | `<tipo_seccion>` | Estructura del archivo | [06-tipo-seccion.md](06-tipo-seccion.md) |
| 7 | `<evento>` | La música | [07-evento.md](07-evento.md) |
| 8 | `<nota>` | La música | [08-nota.md](08-nota.md) |
| 9 | `<nombre_nota>` | La música | [09-nombre-nota.md](09-nombre-nota.md) |
| 10 | `<octava>` | La música | [10-octava.md](10-octava.md) |
| 11 | `<figura>` | La música | [11-figura.md](11-figura.md) |
| 12 | `<nombre_figura>` | La música | [12-nombre-figura.md](12-nombre-figura.md) |
| 13 | `<regla>` | La regla de interpretación | [13-regla.md](13-regla.md) |
| 14 | `<expresion>` | La regla de interpretación | [14-expresion.md](14-expresion.md) |
| 15 | `<termino>` | La regla de interpretación | [15-termino.md](15-termino.md) |
| 16 | `<factor>` | La regla de interpretación | [16-factor.md](16-factor.md) |
| 17 | `<condicion>` | La regla de interpretación | [17-condicion.md](17-condicion.md) |
| 18 | `<operador>` | La regla de interpretación | [18-operador.md](18-operador.md) |
| 19 | `<operando>` | La regla de interpretación | [19-operando.md](19-operando.md) |
| 20 | `<op_aritmetico>` | La regla de interpretación | [20-op-aritmetico.md](20-op-aritmetico.md) |
| 21 | `<acciones>` | La regla de interpretación | [21-acciones.md](21-acciones.md) |
| 22 | `<accion>` | La regla de interpretación | [22-accion.md](22-accion.md) |
| 23 | `<variable>` | Nombres y valores | [23-variable.md](23-variable.md) |
| 24 | `<identificador>` | Nombres y valores | [24-identificador.md](24-identificador.md) |
| 25 | `<valor>` | Nombres y valores | [25-valor.md](25-valor.md) |
| 26 | `<numero>` | Nombres y valores | [26-numero.md](26-numero.md) |
| 27 | `<texto>` | Nombres y valores | [27-texto.md](27-texto.md) |
| 28 | `<letra>` | Átomos | [28-letra.md](28-letra.md) |
| 29 | `<mayuscula>` | Átomos | [29-mayuscula.md](29-mayuscula.md) |
| 30 | `<digito>` | Átomos | [30-digito.md](30-digito.md) |
| 31 | `<nl>` | Átomos | [31-nl.md](31-nl.md) |
