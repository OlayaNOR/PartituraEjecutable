# TocaScript

## Documento general del lenguaje

**Grupo 8** · Valeria Alarcón · Andrew García · Nicolás Olaya  
Lenguajes Formales · Prof. David Cano Baquero · Septiembre de 2026

Este documento reúne en un solo sitio todo lo construido para TocaScript: el dominio y su porqué, las palabras clave, la sintaxis, las quince reglas, el diccionario completo de palabras reservadas, los tipos de dato, la gramática en BNF con su convención de notación, la distinción entre terminales y no terminales, una derivación completa y la decisión del lenguaje de implementación.

**Repositorio:** github.com/OlayaNOR/PartituraEjecutable

---

## 1 · El dominio: interpretación musical

TocaScript es un lenguaje para escribir música y, sobre todo, para **decidir cómo se interpreta**. Los archivos usan la extensión `.toca`.

### Por qué este dominio

Buscábamos un dominio que **ya tuviera reglas escritas**, para no inventárnoslas desde cero. La música las tiene: una partitura **ya es un lenguaje formal**.

| En la partitura | En un lenguaje formal |
|---|---|
| Notas, figuras, silencios | Alfabeto |
| Compás, tonalidad, cómo se combinan | Gramática |
| El músico que la lee | El intérprete |
| La interpretación | La ejecución |

El que lee una partitura y decide qué hacer con ella se llama **intérprete** — la misma palabra que usamos en software. De ahí salió el nombre del lenguaje y su verbo central, `TOCAR`.

### Qué decide el sistema

La partitura dice **qué** notas suenan. Las reglas dicen **cómo** suenan:

| Decisión | Ejemplo |
|---|---|
| Volumen | Sube en el clímax, baja en el cierre |
| Velocidad | Frena en los últimos compases |
| Articulación | Notas cortas cuando hay muchas voces |
| Instrumentos | Entra la percusión si el tema va intenso |

Un músico hace esto sin pensarlo. TocaScript lo escribe como reglas que el sistema aplica solo.

---

## 2 · Las palabras clave y por qué esas

Las reglas usan **cinco** palabras reservadas, todas en MAYÚSCULAS. Cada una está elegida por una razón del dominio.

| Palabra | Función | Por qué esa y no otra |
|---|---|---|
| `AL` | Abre la regla | Las reglas no se evalúan una vez: se revisan **en cada compás**. `AL` expresa algo que ocurre cada vez que se da la condición — *al llegar al estribillo, al pasar el compás 24*. `SI` diría "una vez". |
| `TOCAR` | Separa condición de acción | Es el verbo del dominio y la raíz del nombre. Una regla no «ejecuta una acción»: dice cómo hay que **tocar**. |
| `Y` | Conjunción | Como hablaría un músico: *fuerte y con percusión*. También une dos acciones. |
| `O` | Disyunción | *En la coda o en el final.* |
| `NO` | Negación | *«Cuando no haya percusión»* aparece dos veces entre las 15 reglas. Sin `NO` habría que inventar una variable `sin_percusion`, duplicando información. |

**Mayúsculas en las reglas, minúsculas en la pieza.** Esa distinción hace trabajo: una variable nunca puede chocar con una palabra reservada, y el lexer las separa con solo mirar la caja.

---

## 3 · La sintaxis general de una regla

```
AL <condicion> [Y|O <condicion>] TOCAR <accion>
```

Toda regla tiene la misma forma: `AL`, una condición, `TOCAR`, una acción. Las dos palabras clave son obligatorias y actúan como señales para el lexer: marcan dónde empieza y dónde termina la condición.

| Parte | Qué es | Ejemplo |
|---|---|---|
| `AL` | palabra clave | `AL` |
| `<condicion>` | variable · operador · valor | `es_estribillo Y intensidad > 0.7` |
| `TOCAR` | palabra clave | `TOCAR` |
| `<accion>` | identificador, o asignación | `activar_percusion` · `tempo = tempo - 10` |

**Formas adicionales que admite la sintaxis:**

| Forma | Ejemplo |
|---|---|
| Negación | `NO tiene_percusion` |
| Agrupación | `(es_coda O es_final)` |
| Condición booleana simple | `es_coda` — equivale a `es_coda = true` |
| Acción por asignación | `dinamica = "pp"` |
| Acciones múltiples | `dinamica = "fff" Y duplicar_octava` |
| Aritmética en el valor | `tempo = tempo - 10` |

**Precedencia**, de más fuerte a más débil: `*` `/` → `+` `-` → comparaciones → `NO` → `Y` → `O`. Los paréntesis siempre mandan. La gramática la codifica con niveles: `<operando>` → `<sumando>` → `<primario>` para la aritmética y `<expresion>` → `<termino>` → `<factor>` para la lógica.

---

## 4 · Las 15 reglas y para qué sirven

Están en `reglas.txt`. Se reparten en tres grupos, según lo que pedía el enunciado.

### Grupo A · Una sola condición — 5 reglas

| # | Regla | Para qué sirve |
|---|---|---|
| R1 | `AL tempo > 140 TOCAR dinamica = "ff"` | Si la pieza va rápido, tócala fuerte. La música rápida pide energía. |
| R2 | `AL compas = "3/4" TOCAR acentuar_primer_tiempo` | En un compás de tres tiempos, marca el primero: es lo que hace que un vals suene a vals. Única regla que compara contra **texto**. |
| R3 | `AL es_coda TOCAR dinamica = "pp"` | En el cierre, baja al volumen más suave. Aquí no hay comparación: `es_coda` ya es una condición. |
| R4 | `AL es_intro TOCAR dinamica = "p"` | La introducción se toca suave: empezar bajito deja espacio para crecer. |
| R5 | `AL num_voces > 3 TOCAR articulacion = "staccato"` | Con más de tres instrumentos, notas cortas y separadas: acortarlas deja oír cada una. |

### Grupo B · Condiciones compuestas con Y / O — 6 reglas

| # | Regla | Para qué sirve |
|---|---|---|
| R6 | `AL es_estribillo Y intensidad > 0.7 TOCAR activar_percusion` | En el estribillo y con la música intensa, entra la batería. Tienen que cumplirse **las dos**. |
| R7 | `AL compas_actual > 24 O es_coda TOCAR aplicar_crescendo` | Pasado el compás 24 **o** en el cierre, sube el volumen poco a poco. Basta con **una**. |
| R8 | `AL tempo < 80 Y NO hay_repeticion TOCAR articulacion = "legato"` | Lento y sin repetir: notas pegadas y fluidas. |
| R9 | `AL es_estrofa O hay_repeticion TOCAR dinamica = "mp"` | Estrofas y repeticiones a volumen medio-bajo, para que el estribillo destaque por contraste. |
| R10 | `AL hay_repeticion Y repeticion_actual = 2 TOCAR subir_una_octava` | En la segunda vuelta, todo una octava más agudo: renueva sin cambiar la melodía. |
| R11 | `AL (es_coda O es_final) Y NO tiene_percusion TOCAR tempo = tempo - 10` | Cierre o final sin percusión: frena diez puntos. Con batería frenar suena mal. **Los paréntesis son obligatorios**: sin ellos `Y` se evalúa antes que `O` y la regla diría otra cosa. |

### Grupo C · Tipos distintos combinados — 4 reglas

En la misma condición conviven **un número** y **un booleano**: la comparación numérica devuelve `true`/`false`, y eso se conecta con `Y` a una variable que ya era booleana.

| # | Regla | Para qué sirve | Tipos |
|---|---|---|---|
| R12 | `AL intensidad >= 0.9 Y es_estribillo TOCAR dinamica = "fff" Y duplicar_octava` | El clímax: volumen máximo y melodía duplicada una octava arriba. | `double` + `boolean` |
| R13 | `AL nota_actual > 91 Y NO permitir_agudos TOCAR bajar_una_octava` | Protege de notas más agudas que el `sol6` si la pieza no las autorizó. | `int` + `boolean` |
| R14 | `AL num_voces >= 4 Y tiene_percusion TOCAR volumen = volumen - 15` | Cuatro voces o más con batería saturan: baja el volumen general. El valor nuevo se calcula a partir del actual. | `int` + `boolean` |
| R15 | `AL compas_actual >= duracion_total - 2 Y es_final TOCAR tempo = tempo * 0.85` | *Ritardando*: en los dos últimos compases, velocidad al 85 %. | `int` + `boolean` |

### Cuando dos reglas chocan

Las 15 se revisan en cada compás, en orden de declaración. Si dos fijan la misma propiedad en el mismo momento, **gana la última que se cumpla** y el sistema emite una advertencia. Ocurre a propósito entre la R3 y la R7 en la coda, para tener un caso concreto con el que justificar la política.

---

## 5 · El diccionario de palabras reservadas

TocaScript reserva **72 términos** en su lenguaje completo; la lista está en `palabras_reservadas.md`. Aquí se agrupan por categoría los que usa esta gramática.

### 5.1 · Palabras clave de las reglas

| Palabra | Categoría | Significado |
|---|---|---|
| `AL` | Palabra clave | Abre la regla. Lo que sigue es la condición. |
| `TOCAR` | Palabra clave | Separa la condición de la acción. |
| `Y` | Operador lógico | Conjunción. También une dos acciones. |
| `O` | Operador lógico | Disyunción. |
| `NO` | Operador lógico | Negación. |

### 5.2 · Operadores

| Símbolo | Categoría | Significado |
|---|---|---|
| `>` `<` `>=` `<=` | Relacional | Mayor, menor, mayor o igual, menor o igual |
| `=` | Relacional / asignación | Antes de `TOCAR` compara; después de `TOCAR` asigna |
| `<>` | Relacional | Distinto de |
| `+` `-` `*` `/` | Aritmético | Suma, resta, multiplicación, división (el `/` también separa las cifras del compás dentro de un texto: `"4/4"`) |

### 5.3 · Literales y símbolos

| Símbolo | Categoría | Significado |
|---|---|---|
| `true` `false` | Literal booleano | Verdadero, falso |
| `"` | Delimitador | Abre y cierra un texto |
| `(` `)` | Delimitador | Agrupan condiciones; encierran parámetros de un motivo |
| `{` `}` | Delimitador | Delimitan un bloque: motivo, sección, voz, repetición |
| `[` `]` | Delimitador | Encierran las notas de un acorde: `[do4 mi4 sol4]` |
| `:` | Delimitador | Une un evento con su figura: `do4:negra` |
| `,` | Delimitador | Separa parámetros |
| `.` | Delimitador | Puntillo (`:negra.`) y punto decimal |
| `~` | Delimitador | Ligadura entre dos figuras |
| `#` | Símbolo | Comentario hasta fin de línea; sostenido dentro de una nota |
| `%` | Símbolo | Porcentaje: `velocidad 200%` |

### 5.4 · Palabras clave de la pieza

| Palabra | Significado |
|---|---|
| `motivo` | Declara un fragmento con nombre y reutilizable |
| `acorde` | Declara un grupo de notas con nombre que suenan a la vez |
| `seccion` | Declara una parte de la pieza |
| `tipo` | Rol de una sección: `intro`, `estrofa`, `estribillo`, `coda` |
| `pieza` | Ordena las secciones en el tiempo. Es el punto de entrada |
| `voz` | Declara una línea musical independiente |
| `simultaneo` | Bloque cuyas voces empiezan a la vez |
| `tocar` | Ejecuta un motivo |
| `repetir` | Repite un bloque *n* veces |
| `finales` · `vez` | Casillas de una repetición que termina distinto cada vuelta |
| `con` | Asocia una voz a su instrumento |
| `silencio` | Evento en el que no suena nada; lleva figura como cualquier nota |
| `sin` `reglas` | Bloque al que no se le aplica ninguna regla |
| `exportar` | Escribe el resultado en un archivo |
| `transportado` · `semitonos` | Desplaza un motivo en altura |
| `invertido` · `retrogradado` | Espeja los intervalos · toca al revés |
| `velocidad` | Cambia la velocidad de un motivo |
| `en` | Cambia la tonalidad de un motivo |
| `crescendo` · `hasta` · `durante` | Sube el volumen progresivamente, con destino y duración |

### 5.5 · Literales musicales

| Palabras | Categoría | Significado |
|---|---|---|
| `intro` `estrofa` `estribillo` `coda` | Tipo de sección | Ponen en `true` la variable `es_intro`, `es_estrofa`, `es_estribillo`, `es_coda` |
| `redonda` `blanca` `negra` `corchea` `semicorchea` `fusa` | Figura rítmica | 4 · 2 · 1 · ½ · ¼ · ⅛ tiempos |
| `do` `re` `mi` `fa` `sol` `la` `si` | Nombre de nota | Requiere octava (`do4`); admite alteración (`fa#4`, `mib4`) |

---

## 6 · Los tipos de dato

### 6.1 · Tipos del lenguaje

TocaScript **no define un sistema de tipos propio** — fue una decisión deliberada para no gastar el semestre en ello. Trabaja con cuatro tipos de valor, que en la implementación se mapean a los de Java/Python:

| Tipo | Forma | Ejemplos válidos | Inválidos |
|---|---|---|---|
| Número entero | Uno o más dígitos, sin signo: el `-` es siempre un operador | `96` `140` | `-12` `1.` |
| Número decimal | Dígitos, punto, dígitos | `0.85` `4.5` | `.5` `0,85` |
| Booleano | Solo dos valores | `true` `false` | `verdadero` `TRUE` |
| Texto | Entre comillas dobles, sin saltos de línea | `"ff"` `"Do mayor"` | `'ff'` |

Y dos categorías léxicas propias del dominio:

| Categoría | Forma | Ejemplos |
|---|---|---|
| Nota | Nombre + alteración opcional + octava obligatoria | `do4` `fa#4` `mib3` |
| Figura | Dos puntos + nombre + puntillo opcional | `:negra` `:negra.` |
| Identificador | Letra minúscula, luego letras, dígitos o guion bajo | `tempo` `compas_actual` `frase1` |

### 6.2 · Clasificación de las variables

Las condiciones solo pueden hablar de estas variables. Cualquier otro nombre dentro de una condición es un error.

**Numéricas**

| Variable | Tipo | Ejemplo | Qué guarda |
|---|---|---|---|
| `tempo` | `int` | `96` | Velocidad en pulsos por minuto |
| `compas_actual` | `int` | `16` | En qué compás vamos; empieza en 1 |
| `duracion_total` | `int` | `14` | Cuántos compases tiene la pieza |
| `intensidad` | `double` | `0.85` | De 0.0 a 1.0; se deriva de la dinámica |
| `num_voces` | `int` | `3` | Cuántas líneas suenan a la vez |
| `nota_actual` | `int` | `60` | Altura de la nota en notación MIDI; 60 es `do4` |
| `repeticion_actual` | `int` | `2` | En qué vuelta vamos dentro de una repetición |
| `volumen` | `int` | `100` | Volumen de salida, 0 a 127 |

**Booleanas**

| Variable | Tipo | Es `true` cuando… |
|---|---|---|
| `es_intro` | `boolean` | Estamos en la introducción |
| `es_estrofa` | `boolean` | Estamos en una estrofa |
| `es_estribillo` | `boolean` | Estamos en el estribillo |
| `es_coda` | `boolean` | Estamos en la coda |
| `es_final` | `boolean` | Es la última sección |
| `hay_repeticion` | `boolean` | El compás está dentro de un bloque que se repite |
| `tiene_percusion` | `boolean` | Alguna voz activa usa percusión |
| `permitir_agudos` | `boolean` | La pieza autoriza sonidos muy agudos |

**De texto**

| Variable | Tipo | Ejemplo | Qué guarda |
|---|---|---|---|
| `dinamica` | `String` | `"ff"` | `"pp"` `"p"` `"mp"` `"mf"` `"f"` `"ff"` `"fff"` |
| `articulacion` | `String` | `"legato"` | `"legato"` `"staccato"` `"normal"` |
| `compas` | `String` | `"4/4"` | Cuántos tiempos entran en cada compás |
| `tonalidad` | `String` | `"Do mayor"` | Tonalidad de la pieza |

La `intensidad` se deriva de la dinámica vigente: `"pp"` 0.1 · `"p"` 0.25 · `"mp"` 0.4 · `"mf"` 0.55 · `"f"` 0.7 · `"ff"` 0.85 · `"fff"` 1.0.

---

## 7 · La gramática en BNF: 33 producciones

Todos los terminales van entre comillas dobles —palabras clave, símbolos, letras y dígitos— y todo no terminal se abre en otra producción hasta llegar a `<letra>`, `<digito>` y `<nl>`. Ninguna categoría queda sin definir. Terminales y no terminales van etiquetados como comentario al inicio del bloque, y cada producción tiene su ficha propia.

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

Los tres niveles `<expresion>` → `<termino>` → `<factor>` codifican la precedencia sin reglas aparte: `NO` liga más fuerte que `Y`, y `Y` más fuerte que `O`.

**Verificación regla por regla.** Las 15 reglas de `reglas.txt` se derivaron una a una con un parser (`verificar.py`) que implementa estas 33 producciones: 15 de 15. La primera pasada falló en cinco porque la cabecera declaraba `"tempo"` y `"compas"` como palabras clave y las reglas los usan como variables; se ajustó la gramática —la cabecera es ahora tres `<ajuste> ::= <variable> <valor>`— y no las reglas. El detalle está en el documento aparte *Verificación regla por regla*.

---

## 8 · La convención de notación, estandarizada

Aplicada igual en las 33 producciones:

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

**Por qué todos los terminales van entre comillas.** TocaScript usa llaves y corchetes como parte de su sintaxis real: `motivo frase1 { … }`, `[do4 mi4 sol4]`. Escritos sin marcar, no habría forma de saber si `{ }` significa «repetición» o «aquí va una llave». Por eso todo lo que se teclea va entre comillas —`"{"` es una llave del programa; `{ }` sin comillas es repetición— y, por coherencia, también las palabras clave: `"AL"`, `"motivo"`, `"do"`.

Los nombres de los no terminales van **sin tildes** (`<condicion>`, `<accion>`), para que el lexer no tenga que lidiar con caracteres acentuados.

---

## 9 · Terminales y no terminales

El criterio, en palabras del profesor: *«terminal es lo que no tenga llavecitas, y no terminal es lo que tenga llavecitas»*. Las llavecitas son los ángulos `< >`.

La distinción importa porque **el lexer reconoce los terminales**: son los que le dicen dónde acaba una sentencia.

### No terminales — 33

Uno por cada producción; todos se abren en otra:

`<programa>` `<cabecera>` `<ajuste>` `<pieza>` `<motivo>` `<seccion>` `<tipo_seccion>` `<evento>` `<nota>` `<nombre_nota>` `<octava>` `<figura>` `<nombre_figura>` `<regla>` `<expresion>` `<termino>` `<factor>` `<condicion>` `<operador>` `<operando>` `<sumando>` `<primario>` `<acciones>` `<accion>` `<variable>` `<identificador>` `<valor>` `<numero>` `<texto>` `<letra>` `<mayuscula>` `<digito>` `<nl>`

### Terminales

Todo lo que va entre comillas en la gramática. Son los términos reservados que el lenguaje usa en estas 33 producciones, más los átomos de los que se construyen nombres, números y textos:

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

`tempo`, `compas` y `tonalidad` no son terminales sino variables: la cabecera las fija y las reglas las consultan. La lista completa de los 72 términos reservados del lenguaje extendido está en la sección 5.

**Ejemplo mínimo** — el evento `do4:negra`:

```
<evento> (8)
  <nota> (9)  → "do" "4"
  ":"
  <figura> (12)
    <nombre_figura> (13)
      "negra"
```

Todo lo que tiene ángulos se abre en algo más; `"do"`, `"4"`, `":"` y `"negra"` ya no: son las hojas, son terminales.

---

## 10 · Una derivación completa

La regla 11 del catálogo, derivada paso a paso desde `<regla>`:

```
AL (es_coda O es_final) Y NO tiene_percusion TOCAR tempo = tempo - 10
```

| Paso | Se aplica | Queda |
|---|---|---|
| 1 | `<regla>` (14) | `"AL" <expresion> "TOCAR" <acciones> <nl>` |
| 2 | `<expresion>` (15) → un solo `<termino>` | `"AL" <termino> "TOCAR" <acciones> <nl>` |
| 3 | `<termino>` (16) → `<factor> "Y" <factor>` | `"AL" <factor> "Y" <factor> "TOCAR" <acciones> <nl>` |
| 4 | 1.er `<factor>` (17) → `"(" <expresion> ")"` | `"AL" "(" <expresion> ")" "Y" <factor> …` |
| 5 | esa `<expresion>` → `<termino> "O" <termino>` → `<variable>` cada uno | `"AL" "(" es_coda "O" es_final ")" "Y" <factor> …` |
| 6 | 2.º `<factor>` → `"NO" <factor>` → `<variable>` | `… "Y" "NO" tiene_percusion "TOCAR" <acciones> <nl>` |
| 7 | `<acciones>` (23) → `<accion>` (24) → `<variable> "=" <operando>` | `… "TOCAR" tempo "=" <operando> <nl>` |
| 8 | `<operando>` (20) → `<sumando> "-" <sumando>` → `<primario>` (22) → `<variable>` y `<valor>` | `… "TOCAR" tempo "=" tempo "-" 10 <nl>` |
| 9 | `<nl>` (33) → `"↵"`; cada variable y número se abre hasta `<letra>` y `<digito>` | la regla completa |

Las hojas, leídas de izquierda a derecha, son la regla completa. El primer factor abre un paréntesis que vuelve a contener una expresión entera: ahí está la recursión. Y los tres niveles hacen que `NO` se resuelva antes que `Y`, y `Y` antes que `O`; la aritmética baja igual por operando, sumando y primario. Sin esos niveles, esta regla significaría *«si es la coda, o bien si es el final sin percusión»*, que no es lo mismo.

---

## 11 · Lenguaje de implementación: Python

Elegimos **Python**, siguiendo la recomendación del profesor: trae librerías que ahorran trabajo, y el semestre no da para escribirlo todo desde cero.

| Decisión | Por qué |
|---|---|
| Intérprete de recorrido de árbol | Se ejecuta el AST directamente tras el parsing. El rendimiento no se evalúa. |
| Tipado dinámico | No diseñamos un sistema de tipos propio: es el subproyecto más caro del semestre y no aporta a la nota. |
| Exportar MIDI con librerías | Existen; no hay que escribir el formato a mano. |

### Cómo se ejecuta: el ciclo por compás

Una regla **nunca se invoca**. Se escribe una vez y el sistema la vigila. En cada compás:

1. **Toma una foto del estado** — compás, sección, voces, intensidad.
2. **Evalúa las 15 reglas** contra esa foto, en orden de declaración.
3. **Aplica las acciones** de las que se cumplieron.
4. **Suena el compás**, ya con los ajustes. Y repite.

La foto se toma **antes**, no durante: las reglas leen el estado como estaba al empezar el compás. Sin eso, una regla podría disparar a otra dentro del mismo compás y el resultado dependería del orden.

### El pipeline y dónde vamos

```
Reglas + .toca  →  Lexer  →  Tokens  →  Parser  →  Motor de inferencia  →  Acciones
   entregado      siguiente
```

---

## 12 · Un programa de ejemplo

*Fray Santiago* (Frère Jacques) en `.toca`, escrito solo con lo que las 33 producciones generan. La comparación línea por línea contra la gramática está en el documento aparte.

```
tempo 100
compas "4/4"
tonalidad "Do mayor"

motivo frase1 { do4:negra re4:negra mi4:negra do4:negra }
motivo frase2 { mi4:negra fa4:negra sol4:blanca }

seccion cancion tipo estrofa { frase1 frase1 frase2 frase2 }
seccion cierre tipo coda { [do3 mi3 sol3 do4]:redonda }

AL es_estrofa O hay_repeticion TOCAR dinamica = "mp"
AL es_coda TOCAR dinamica = "pp"
AL (es_coda O es_final) Y NO tiene_percusion TOCAR tempo = tempo - 10

pieza "Fray Santiago" { cancion cierre }
```

El archivo completo del repositorio (`ejemplos/frere-jacques.toca`) usa además `simultaneo`, `voz`, `repetir` y `exportar`, que pertenecen a la gramática extendida.

---

## 13 · Bibliografía

Aho, A. V., Lam, M. S., Sethi, R. & Ullman, J. D. — *Compilers: Principles, Techniques and Tools*.

| Página | Respalda |
|---|---|
| 25 | Las reglas y los básicos del lenguaje → las 15 reglas |
| 81 | Lexers y tokens → el analizador léxico |
| 132 | Palabras reservadas e identificadores → `palabras_reservadas.md` |
| 191–200 | Sintaxis y definición formal de la gramática → la gramática BNF |

---

## Archivos del repositorio

| Archivo | Qué contiene |
|---|---|
| `README.md` | El lenguaje completo, las 15 reglas y la tabla de variables |
| `reglas.txt` | Las 15 reglas en su forma oficial |
| `REGLAS.md` | Qué hace cada regla y por qué |
| `palabras_reservadas.md` | Los 72 términos con categoría y significado |
| `gramatica.md` | Las 33 producciones BNF, terminales y no terminales etiquetados, y la derivación de la regla 11 |
| `gramatica/` | Una ficha por producción, con desglose, ejemplos y derivación |
| `VERIFICACION-REGLAS.md` | Las 15 reglas derivadas una a una |
| `verificar.py` | El parser que implementa las 33 producciones y produce todas las derivaciones |
| `COMPARACION-EJEMPLO.md` | El programa de ejemplo derivado línea por línea |
| `LibroLengujesFormales.rtf` | La consulta bibliográfica |
| `ejemplos/frere-jacques.toca` | El programa de referencia |

*Grupo 8 · Alarcón · García · Olaya · Lenguajes Formales · 2026*
