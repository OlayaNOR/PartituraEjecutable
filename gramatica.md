# Gramática de TocaScript en notación BNF

**Grupo 8** · Valeria Alarcón · Andrew García · Nicolás Olaya

Las **33 reglas de producción** que definen el lenguaje, en la convención BNF del curso: todos los terminales entre comillas y todo no terminal abierto hasta los átomos. Una ficha por producción en [`gramatica/`](gramatica/README.md); la verificación de las 15 reglas de `reglas.txt` en [`VERIFICACION-REGLAS.md`](VERIFICACION-REGLAS.md).

---

## Convención de notación

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

> [!IMPORTANT]
> **Por qué todos los terminales van entre comillas**
>
> TocaScript usa llaves y corchetes **como parte de su sintaxis real**: `motivo frase1 { … }`, `[do4 mi4 sol4]`. Escritos sin marcar, no habría forma de saber si `{ }` significa «repetición» o «aquí va una llave». Por eso todo lo que se teclea va entre comillas —`"{"` es una llave del programa; `{ }` sin comillas es repetición— y, por coherencia, también las palabras clave: `"AL"`, `"motivo"`, `"do"`. La comilla doble como terminal se escribe `'"'`.

> **El criterio de terminal:** terminal es lo que no lleva ángulos `< >`; no terminal es lo que los lleva y se abre en otra producción. **El lexer solo necesita reconocer los terminales.**

Los nombres de los no terminales van sin tildes (`<condicion>`, `<accion>`), para que el lexer no dependa de la codificación del archivo.

---

## Las 33 producciones

Terminales y no terminales etiquetados como comentario al inicio del bloque.

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

---

## Terminales y no terminales

### No terminales — 33

Uno por cada producción; todos se abren en otra:

`<programa>` · `<cabecera>` · `<ajuste>` · `<pieza>` · `<motivo>` · `<seccion>` · `<tipo_seccion>` · `<evento>` · `<nota>` · `<nombre_nota>` · `<octava>` · `<figura>` · `<nombre_figura>` · `<regla>` · `<expresion>` · `<termino>` · `<factor>` · `<condicion>` · `<operador>` · `<operando>` · `<sumando>` · `<primario>` · `<acciones>` · `<accion>` · `<variable>` · `<identificador>` · `<valor>` · `<numero>` · `<texto>` · `<letra>` · `<mayuscula>` · `<digito>` · `<nl>`

### Terminales

Todo lo que va entre comillas en la gramática. Ahí termina la derivación, y son lo único que el lexer necesita reconocer:

| Categoría | Terminales |
|---|---|
| Palabras clave de la regla | `"AL"` `"TOCAR"` `"Y"` `"O"` `"NO"` |
| Palabras clave de la pieza | `"motivo"` `"seccion"` `"tipo"` `"pieza"` `"silencio"` |
| Tipos de sección | `"intro"` `"estrofa"` `"estribillo"` `"coda"` |
| Nombres de nota | `"do"` `"re"` `"mi"` `"fa"` `"sol"` `"la"` `"si"` |
| Figuras | `"redonda"` `"blanca"` `"negra"` `"corchea"` `"semicorchea"` `"fusa"` |
| Alteraciones y puntillo | `"#"` `"b"` `"."` |
| Operadores relacionales | `">"` `"<"` `">="` `"<="` `"="` `"<>"` |
| Operadores aritméticos | `"+"` `"-"` `"*"` `"/"` |
| Booleanos | `"true"` `"false"` |
| Símbolos | `"("` `")"` `"{"` `"}"` `"["` `"]"` `":"` `"_"` `" "` `'"'` `"↵"` |
| Átomos | `"a … z"` `"A … Z"` `"0 … 9"` |

`tempo`, `compas` y `tonalidad` **no** son terminales: son variables (`<variable>` → `<identificador>`) que la cabecera fija y las reglas consultan. Los 72 términos reservados del lenguaje completo (incluido lo que no entra en este parcial: voces, `repetir`, `exportar`) están en [`palabras_reservadas.md`](palabras_reservadas.md).

---

## Verificación regla por regla

Las 15 reglas de `reglas.txt` se derivaron una a una con un parser (`verificar.py`) que implementa estas 33 producciones: **15 de 15 generadas**. La primera pasada falló en cinco (R1, R2, R8, R11, R15) porque la cabecera declaraba `"tempo"` y `"compas"` como palabras clave y las reglas los usan como variables; se ajustó la gramática —la cabecera pasó a ser tres `<ajuste> ::= <variable> <valor>`— y no las reglas. Detalle, tokens y árbol de cada regla en [`VERIFICACION-REGLAS.md`](VERIFICACION-REGLAS.md).

## Cómo se deriva una regla real

La regla 11, la que más construcciones usa a la vez — paréntesis, `O`, `Y`, `NO` y aritmética:

```
AL (es_coda O es_final) Y NO tiene_percusion TOCAR tempo = tempo - 10
```

```
<regla> (14)
  "AL"
  <expresion> (15)
    <termino> (16)
      <factor> (17)
        "("
        <expresion> (15)
          <termino> (16)
            <factor> (17)
              <variable> (25)
                <identificador> (26)  → "e" "s" "_" "c" "o" "d" "a"
          "O"
          <termino> (16)
            <factor> (17)
              <variable> (25)
                <identificador> (26)  → "e" "s" "_" "f" "i" "n" "a" "l"
        ")"
      "Y"
      <factor> (17)
        "NO"
        <factor> (17)
          <variable> (25)
            <identificador> (26)  → "t" "i" "e" "n" "e" "_" "p" "e" "r" "c" "u" "s" "i" "o" "n"
  "TOCAR"
  <acciones> (23)
    <accion> (24)
      <variable> (25)
        <identificador> (26)  → "t" "e" "m" "p" "o"
      "="
      <operando> (20)
        <sumando> (21)
          <primario> (22)
            <variable> (25)
              <identificador> (26)  → "t" "e" "m" "p" "o"
        "-"
        <sumando> (21)
          <primario> (22)
            <valor> (27)
              <numero> (28)  → "1" "0"
  <nl> (33)  → "↵"
```

Los tres niveles `<expresion>` → `<termino>` → `<factor>` **no son decoración**: codifican la precedencia sin reglas aparte. `NO` liga más fuerte que `Y`, y `Y` más que `O`. Sin los paréntesis, `Y` se agruparía antes que `O` y la regla diría *«si es la coda, o bien si es el final sin percusión»*, que no es lo mismo.

---

## Relación con el resto del repositorio

| Archivo | Qué aporta |
|---|---|
| [`reglas.txt`](reglas.txt) | Las 15 reglas de interpretación: instancias de `<regla>` |
| [`VERIFICACION-REGLAS.md`](VERIFICACION-REGLAS.md) | Las 15 derivadas una a una |
| [`gramatica/`](gramatica/README.md) | Una ficha por producción, con desglose, ejemplos y derivación |
| [`palabras_reservadas.md`](palabras_reservadas.md) | Los 72 términos reservados del lenguaje completo |
| [`COMPARACION-EJEMPLO.md`](COMPARACION-EJEMPLO.md) | El programa de ejemplo derivado línea por línea |
| [`DOCUMENTO.md`](DOCUMENTO.md) | Todo el lenguaje en un solo sitio |

*Grupo 8 · Lenguajes Formales · Prof. David Cano Baquero*
