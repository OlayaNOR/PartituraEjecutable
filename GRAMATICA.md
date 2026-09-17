# Gramática de TocaScript en notación BNF

**Grupo 8** · Valeria Alarcón · Andrew García · Nicolás Olaya

Las **20 reglas de producción** que definen el lenguaje, escritas en la convención BNF que el
profesor presentó en la clase del 11 de septiembre.

---

## Convención de notación

El profesor dejó la convención abierta, pero exigió que fuera consistente:

> «Ejemplo de convención a adoptar (pueden variar ligeramente, **pero deben ser consistentes**).»

Ésta es la nuestra, y se aplica igual en las 20 reglas:

| Símbolo | Significado |
|---|---|
| `<nombre>` | **No terminal** — hay otra regla que lo explica |
| `nombre` (sin ángulos) | **Terminal** — ahí se acaba la derivación |
| `::=` | «se define como» |
| `\|` | alternativa: una u otra |
| `[ ... ]` | opcional: cero o una vez |
| `{ ... }` | repetición: cero o más veces |
| `" ... "` | **símbolo literal** del lenguaje, no meta-símbolo |
| `# ...` | comentario |

> [!IMPORTANT]
> **Por qué hacen falta las comillas**
>
> TocaScript usa llaves y corchetes **como parte de su sintaxis real**: `motivo frase1 { … }`,
> `[do4 mi4 sol4]`. Si escribiéramos esos mismos signos sin marcar, no habría forma de saber si
> `{ }` significa «repetición» o «aquí va una llave».
>
> Por eso todo símbolo que pertenece al lenguaje va **entre comillas**: `"{"` es una llave que se
> teclea; `{ }` sin comillas es repetición. Es exactamente la inconsistencia que el profesor
> admitió tener en su propio archivo — *«en algunas partes tengo el opcional con llaves y el otro
> con corchetes»* — y que pidió estandarizar.

> **El criterio de terminal, en palabras del profesor:**
> «Terminal es lo que no tenga llavecitas, y no terminal es lo que tenga llavecitas.»
> Las «llavecitas» son los ángulos `< >`.

Los nombres de los no terminales van **sin tildes**, como en su ejemplo (`<condicion>`, `<accion>`),
para que el lexer no tenga que lidiar con caracteres acentuados en los identificadores de la gramática.

---

## Las 20 reglas de producción

```
# ═══════════════════════════════════════════════════════════
#  GRAMÁTICA DE TocaScript  ·  Grupo 8  ·  Notación BNF
# ═══════════════════════════════════════════════════════════
#
#  <x>   no terminal        x    terminal
#  ::=   se define como     |    alternativa
#  [ ]   opcional           { }  cero o más veces
#  "x"   simbolo literal del lenguaje (no meta-simbolo)
#
# ───────────────────────────────────────────────────────────
#  BLOQUE A · La regla de interpretación          (8 reglas)
# ───────────────────────────────────────────────────────────
#
#  Sintaxis general de una regla:
#  AL <condicion> [Y|O <condicion>] TOCAR <accion>
#
#  1  <regla>      ::= AL <expresion> TOCAR <acciones>
#
#  2  <expresion>  ::= <termino> { O <termino> }
#
#  3  <termino>    ::= <factor> { Y <factor> }
#
#  4  <factor>     ::= NO <factor>
#                    | "(" <expresion> ")"
#                    | <condicion>
#                    | <variable>
#
#  5  <condicion>  ::= <operando> <operador> <operando>
#
#  6  <operando>   ::= <variable>
#                    | <valor>
#                    | <operando> <op_aritmetico> <operando>
#
#  7  <acciones>   ::= <accion> { Y <accion> }
#
#  8  <accion>     ::= <variable> "=" <operando>
#                    | <identificador>
#
# ───────────────────────────────────────────────────────────
#  BLOQUE B · Operadores y valores                (4 reglas)
# ───────────────────────────────────────────────────────────
#
#  9  <operador>      ::= > | < | >= | <= | = | <>
#
# 10  <op_aritmetico> ::= + | - | * | /
#
# 11  <variable>      ::= identificador en minusculas con guion_bajo
#
# 12  <valor>         ::= <numero> | true | false | <texto>
#
# ───────────────────────────────────────────────────────────
#  BLOQUE C · El programa                         (3 reglas)
# ───────────────────────────────────────────────────────────
#
# 13  <programa>  ::= <cabecera> { <motivo> | <seccion> | <regla> } <pieza>
#
# 14  <cabecera>  ::= tempo <numero>
#                     compas <texto>
#                     tonalidad <texto>
#
# 15  <pieza>     ::= pieza <texto> "{" { <identificador> } "}"
#
# ───────────────────────────────────────────────────────────
#  BLOQUE D · La música                           (5 reglas)
# ───────────────────────────────────────────────────────────
#
# 16  <motivo>   ::= motivo <identificador> "{" { <evento> } "}"
#
# 17  <seccion>  ::= seccion <identificador> tipo <tipo_seccion>
#                    "{" { <evento> | <identificador> } "}"
#
# 18  <evento>   ::= <nota> ":" <figura>
#                  | "[" <nota> { <nota> } "]" ":" <figura>
#                  | silencio ":" <figura>
#
# 19  <nota>     ::= ( do | re | mi | fa | sol | la | si )
#                    [ "#" | "b" ] <octava>
#
# 20  <figura>   ::= ( redonda | blanca | negra
#                    | corchea | semicorchea | fusa ) [ "." ]
#
# ═══════════════════════════════════════════════════════════
```

---

## Terminales y no terminales

La distinción importa porque **el analizador léxico reconoce los terminales**: son los que le dicen
dónde acaba una sentencia.

### No terminales — 20

Uno por cada regla de producción. Son los que llevan `< >`, y todos se abren en otra línea:

`<regla>` · `<expresion>` · `<termino>` · `<factor>` · `<condicion>` · `<operando>` ·
`<acciones>` · `<accion>` · `<operador>` · `<op_aritmetico>` · `<variable>` · `<valor>` ·
`<programa>` · `<cabecera>` · `<pieza>` · `<motivo>` · `<seccion>` · `<evento>` · `<nota>` · `<figura>`

> `<tipo_seccion>`, `<identificador>`, `<numero>`, `<texto>` y `<octava>` aparecen en el lado
> derecho pero no tienen regla propia entre las 20: son las categorías léxicas que el lexer
> resuelve directamente. La gramática completa (51 producciones) sí las desarrolla.

### Terminales

Ahí se acaba la derivación: no hay ninguna regla que los vuelva a abrir.

| Categoría | Terminales |
|---|---|
| **Palabras clave de la regla** | `AL` `TOCAR` `Y` `O` `NO` |
| **Palabras clave de la pieza** | `tempo` `compas` `tonalidad` `motivo` `seccion` `tipo` `pieza` `silencio` |
| **Tipos de sección** | `intro` `estrofa` `estribillo` `coda` |
| **Figuras rítmicas** | `redonda` `blanca` `negra` `corchea` `semicorchea` `fusa` |
| **Nombres de nota** | `do` `re` `mi` `fa` `sol` `la` `si` |
| **Alteraciones** | `#` `b` |
| **Operadores relacionales** | `>` `<` `>=` `<=` `=` `<>` |
| **Operadores aritméticos** | `+` `-` `*` `/` |
| **Booleanos** | `true` `false` |
| **Delimitadores** | `(` `)` `{` `}` `[` `]` `:` `"` `.` `=` |

---

## Cómo se deriva una regla real

La regla 11 del catálogo, derivada paso a paso desde `<regla>`:

```
AL (es_coda O es_final) Y NO tiene_percusion TOCAR tempo = tempo - 10
```

| Paso | Se aplica | Resultado |
|---|---|---|
| 1 | `<regla>` | `AL <expresion> TOCAR <acciones>` |
| 2 | `<expresion>` → un solo `<termino>` | `AL <termino> TOCAR <acciones>` |
| 3 | `<termino>` → `<factor> Y <factor>` | `AL <factor> Y <factor> TOCAR <acciones>` |
| 4 | 1.er `<factor>` → `( <expresion> )` | `AL ( <expresion> ) Y <factor> …` |
| 5 | esa `<expresion>` → `<termino> O <termino>` | `AL ( es_coda O es_final ) Y <factor> …` |
| 6 | 2.º `<factor>` → `NO <factor>` → `<variable>` | `… Y NO tiene_percusion TOCAR <acciones>` |
| 7 | `<acciones>` → `<accion>` → `<variable> = <operando>` | `… TOCAR tempo = <operando>` |
| 8 | `<operando>` → `<operando> <op_aritmetico> <operando>` | `… TOCAR tempo = tempo - 10` |

Los tres niveles `<expresion>` → `<termino>` → `<factor>` **no son decoración**: codifican la
precedencia sin necesidad de reglas aparte. `NO` liga más fuerte que `Y`, y `Y` más que `O`.
Sin ellos, la regla 11 significaría otra cosa.

---

## Relación con el resto del repositorio

| Archivo | Qué aporta |
|---|---|
| [`reglas.txt`](reglas.txt) | Las 15 reglas de interpretación, que son **instancias** de la regla nº 1 |
| [`palabras_reservadas.md`](palabras_reservadas.md) | Los 66 términos reservados: la lista completa de terminales |
| [`REGLAS.md`](REGLAS.md) | Qué hace cada regla y por qué, en lenguaje llano |
| [`README.md`](README.md) | El lenguaje completo, con la gramática extendida |

---

*Grupo 8 · Lenguajes Formales · Prof. David Cano Baquero*
