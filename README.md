# TocaScript

**Grupo 8** · Lenguajes Formales

**Integrantes:** Alarcon · Olaya · Garcia

---

## Dominio del sistema

**Interpretación musical.**

El sistema procesa reglas que deciden **cómo debe sonar una pieza** según lo que esté ocurriendo mientras suena: qué tan rápida va, en qué sección está, cuántos instrumentos hay tocando, qué tan intensa es la música en ese momento.

Un músico hace esto todo el tiempo sin pensarlo: baja el volumen al final de una canción, ataca más fuerte cuando el tema es rápido, acorta las notas cuando hay mucha gente tocando a la vez. TocaScript escribe esas decisiones como reglas que el sistema aplica solo.

Los archivos del lenguaje usan la extensión **`.toca`**.

---

## Sintaxis general de una regla

```
# Sintaxis general de una regla:
# AL <condicion> [Y|O <condicion>] TOCAR <accion>
#
# <condicion>  ::= <variable> <operador> <valor>
# <operador>   ::= > | < | = | >= | <= | <>
# <variable>   ::= identificador en minusculas con guion_bajo
# <valor>      ::= numero (entero o decimal) | true | false | "texto"
# <accion>     ::= identificador en minusculas con guion_bajo
#                | <variable> = <valor>
```

### Gramática completa

```
<regla>       ::= AL <expresion> TOCAR <acciones>

<expresion>   ::= <termino> [ O <termino> ]*
<termino>     ::= <factor> [ Y <factor> ]*
<factor>      ::= NO <factor>
                | ( <expresion> )
                | <condicion>
                | <variable>

<condicion>   ::= <operando> <operador> <operando>
<operador>    ::= > | < | = | >= | <= | <>
<operando>    ::= <variable> | <valor> | <aritmetica>
<aritmetica>  ::= <operando> ( + | - | * | / ) <operando>

<acciones>    ::= <accion> [ Y <accion> ]*
<accion>      ::= <variable> = <operando>
                | identificador_en_minusculas

<variable>    ::= identificador_en_minusculas
<valor>       ::= numero | true | false | "texto"
```

La gramática de `<expresion>` está escrita en tres niveles —`expresion`, `termino`, `factor`— porque así queda codificada la precedencia sin necesidad de reglas aparte: `NO` liga más fuerte que `Y`, y `Y` más fuerte que `O`.

### Por qué estas palabras clave

| Palabra | Por qué |
|---|---|
| **`AL`** | Las reglas no se evalúan una vez: se revisan en **cada compás**. `AL` expresa algo que ocurre cada vez que se da la condición, no una decisión puntual. Y encaja con el dominio: *al llegar al estribillo*, *al pasar el compás 24*. |
| **`TOCAR`** | Es el verbo central del lenguaje y la raíz de su nombre. Una regla no «ejecuta una acción»: dice cómo hay que **tocar** la música cuando se cumple la condición. |
| **`NO`** | «Cuando **no** haya percusión» aparece dos veces entre las 15 reglas. Sin `NO` habría que inventar una variable `sin_percusion`, duplicando información. |
| **`( )`** | Sin paréntesis, `Y` se evalúa antes que `O` y la regla 11 significaría otra cosa. |

### Otras decisiones de sintaxis

| Decisión | Forma | Por qué |
|---|---|---|
| Operadores `>=` `<=` `<>` | `num_voces >= 4` | «cuatro voces o más» es una condición natural del dominio; con solo `>` habría que escribir `num_voces > 3`, que dice lo mismo pero se lee peor |
| Condición booleana simple | `es_coda` | equivale a `es_coda = true`; la forma corta evita decir lo mismo dos veces |
| Acción por asignación | `dinamica = "ff"` | la mayoría de acciones musicales fijan una propiedad, no invocan un procedimiento |
| Acciones múltiples y aritmética | `<accion> Y <accion>`<br>`tempo = tempo - 10` | la regla 12 hace dos cosas; las reglas 11, 14 y 15 calculan el valor nuevo a partir del actual |

---

## Convención de escritura

| Elemento | Convención | Ejemplo |
|---|---|---|
| Palabras reservadas | MAYÚSCULAS | `AL`, `TOCAR`, `Y`, `O`, `NO` |
| Variables | minúsculas con guion bajo | `compas_actual`, `tiene_percusion` |
| Acciones | minúsculas con guion bajo | `activar_percusion`, `subir_una_octava` |
| Literales de texto | entre comillas dobles | `"ff"`, `"staccato"` |
| Comentarios | empiezan con `#` | `# R1 - acento fuerte` |
| Formato | una regla por línea | ver abajo |

**Precedencia**, de más fuerte a más débil: `NO` → comparaciones → `Y` → `O`. Los paréntesis siempre mandan.

**El lenguaje distingue mayúsculas de minúsculas**, y esa distinción hace trabajo: las palabras de las reglas van en mayúsculas y las de la pieza en minúsculas, así se separan de un vistazo y nunca chocan entre sí.

Los **73 términos reservados** del lenguaje —palabras clave, operadores, delimitadores, figuras y notas— están documentados uno por uno, con su categoría y significado, en [`palabras_reservadas.md`](palabras_reservadas.md). Ahí están también las convenciones léxicas: qué forma tiene un identificador, un número, un literal de texto o una nota.

---

## Las 15 reglas

En su forma oficial están en [`reglas.txt`](reglas.txt). La explicación detallada de cada una, con el porqué musical, está en [`REGLAS.md`](REGLAS.md).

### Grupo A · Una sola condición · *5 reglas*

| # | Regla | En lenguaje natural |
|---|---|---|
| R1 | `AL tempo > 140 TOCAR dinamica = "ff"` | Si la pieza va a más de 140 pulsos por minuto, tócala fuerte. |
| R2 | `AL compas = "3/4" TOCAR acentuar_primer_tiempo` | En un compás de tres tiempos, marca el primero. |
| R3 | `AL es_coda TOCAR dinamica = "pp"` | En el cierre de la pieza, baja al volumen más suave. |
| R4 | `AL es_intro TOCAR dinamica = "p"` | La introducción se toca suave. |
| R5 | `AL num_voces > 3 TOCAR articulacion = "staccato"` | Si hay más de tres instrumentos a la vez, que toquen las notas cortas y separadas. |

### Grupo B · Condiciones compuestas con Y / O · *6 reglas*

| # | Regla | En lenguaje natural |
|---|---|---|
| R6 | `AL es_estribillo Y intensidad > 0.7 TOCAR activar_percusion` | Si estamos en el estribillo y la música va intensa, entra la batería. |
| R7 | `AL compas_actual > 24 O es_coda TOCAR aplicar_crescendo` | Si pasamos el compás 24 o estamos en el cierre, sube el volumen poco a poco. |
| R8 | `AL tempo < 80 Y NO hay_repeticion TOCAR articulacion = "legato"` | Si la pieza va lenta y no estamos repitiendo, toca las notas pegadas y fluidas. |
| R9 | `AL es_estrofa O hay_repeticion TOCAR dinamica = "mp"` | En las estrofas y dentro de cualquier repetición, volumen medio-bajo. |
| R10 | `AL hay_repeticion Y repeticion_actual = 2 TOCAR subir_una_octava` | En la segunda vuelta de una repetición, toca todo una octava más agudo. |
| R11 | `AL (es_coda O es_final) Y NO tiene_percusion TOCAR tempo = tempo - 10` | Si es el cierre o la última sección y no hay percusión, frena diez puntos. |

### Grupo C · Tipos distintos combinados · *4 reglas*

| # | Regla | En lenguaje natural | Tipos |
|---|---|---|---|
| R12 | `AL intensidad >= 0.9 Y es_estribillo TOCAR dinamica = "fff" Y duplicar_octava` | Si la intensidad está casi al máximo y estamos en el estribillo, sube al volumen más alto y duplica la melodía una octava arriba. | `double` + `boolean` |
| R13 | `AL nota_actual > 91 Y NO permitir_agudos TOCAR bajar_una_octava` | Si la nota es más aguda que el `sol6` y la pieza no autorizó agudos, bájala una octava. | `int` + `boolean` |
| R14 | `AL num_voces >= 4 Y tiene_percusion TOCAR volumen = volumen - 15` | Si hay cuatro o más voces y una es percusión, baja el volumen general quince puntos. | `int` + `boolean` |
| R15 | `AL compas_actual >= duracion_total - 2 Y es_final TOCAR tempo = tempo * 0.85` | Cuando faltan dos compases o menos y es la última sección, baja la velocidad al 85%. | `int` + `boolean` |

### Clasificación

| Grupo | Qué las define | Reglas | Total |
|---|---|---|---|
| A | Una sola condición | R1 R2 R3 R4 R5 | **5** |
| B | Compuestas con `Y` / `O` | R6 R7 R8 R9 R10 R11 | **6** |
| C | Numérico + booleano en la misma condición | R12 R13 R14 R15 | **4** |

> Las reglas 6, 7, 8 y 10 *también* mezclan numérico con booleano. Se clasificaron en el grupo B porque lo que las define principalmente es el uso de conectores lógicos.

---

## Clasificación de variables

Las condiciones solo pueden hablar de estas variables. Cualquier otro nombre dentro de una condición es un error.

### Numéricas

| Variable | Tipo Java | Ejemplo | Qué guarda |
|---|---|---|---|
| `tempo` | `int` | `96` | Velocidad de la pieza en pulsos por minuto. 60 es lento, 120 normal, 180 rápido. |
| `compas_actual` | `int` | `16` | En qué trozo de la pieza vamos. Empieza en 1 y sube. |
| `duracion_total` | `int` | `14` | Cuántos compases tiene la pieza completa. |
| `intensidad` | `double` | `0.85` | Qué tan intensa va la música, de 0.0 a 1.0. Se deriva de la dinámica. |
| `num_voces` | `int` | `3` | Cuántas líneas musicales suenan a la vez. |
| `nota_actual` | `int` | `60` | Altura de la nota que suena, en notación MIDI. 60 es el `do4`. |
| `repeticion_actual` | `int` | `2` | En qué vuelta vamos dentro de una repetición. |
| `volumen` | `int` | `100` | Volumen de salida, de 0 a 127. |

### Booleanas

| Variable | Tipo Java | Ejemplo | Es `true` cuando… |
|---|---|---|---|
| `es_intro` | `boolean` | `true` | Estamos en la introducción de la pieza. |
| `es_estrofa` | `boolean` | `false` | Estamos en una estrofa. |
| `es_estribillo` | `boolean` | `true` | Estamos en el estribillo, la parte que se repite. |
| `es_coda` | `boolean` | `false` | Estamos en la coda, el cierre. |
| `es_final` | `boolean` | `false` | Es la última sección de la pieza. |
| `hay_repeticion` | `boolean` | `true` | El compás está dentro de un bloque que se repite. |
| `tiene_percusion` | `boolean` | `false` | Alguna voz activa usa batería o percusión. |
| `permitir_agudos` | `boolean` | `true` | La pieza autoriza sonidos muy agudos. |

### De texto

| Variable | Tipo Java | Ejemplo | Qué guarda |
|---|---|---|---|
| `dinamica` | `String` | `"ff"` | Volumen actual: `"pp"`, `"p"`, `"mp"`, `"mf"`, `"f"`, `"ff"`, `"fff"`. |
| `articulacion` | `String` | `"legato"` | Cómo se atacan las notas: `"legato"`, `"staccato"`, `"normal"`. |
| `compas` | `String` | `"4/4"` | Cuántos tiempos entran en cada compás. |
| `tonalidad` | `String` | `"Do mayor"` | Tonalidad de la pieza. |

### Acciones disponibles

| Acción | Qué hace |
|---|---|
| `acentuar_primer_tiempo` | Ataca con más fuerza el primer tiempo de cada compás. |
| `activar_percusion` | Suma una voz de batería. |
| `aplicar_crescendo` | Sube el volumen de forma progresiva. |
| `subir_una_octava` | Toca todo doce semitonos más agudo. |
| `bajar_una_octava` | Toca todo doce semitonos más grave. |
| `duplicar_octava` | Dobla la melodía una octava arriba, sonando las dos a la vez. |

Además, cualquier variable puede recibir un valor directamente: `dinamica = "ff"`, `tempo = tempo - 10`.

### La cabecera de una pieza son asignaciones

Las primeras líneas de un archivo `.toca` fijan las variables de la pieza:

```
tempo 100
compas "4/4"
tonalidad "Do mayor"
```

`tempo 100` es azúcar sintáctico de `tempo = 100`. Gracias a eso, **la misma variable que la pieza fija en su cabecera es la que las reglas consultan después**: no hay dos conceptos, hay uno solo. Por eso `tempo`, `compas` y `tonalidad` aparecen en la tabla de variables y no en la de palabras reservadas.

Los nombres de instrumento son **literales de texto**, no palabras del lenguaje: `voz bajo con "contrabajo"`. Así el conjunto de instrumentos queda abierto sin tener que reservar una palabra por cada uno.

---

## Conceptos musicales mínimos

Para leer las reglas sin saber música. Nada más que esto hace falta.

| Término | En palabras simples |
|---|---|
| **Compás** | La pieza se divide en trozos de igual duración, como los renglones de un cuaderno. |
| **Tempo** | La velocidad de la pieza, en pulsos por minuto. |
| **Dinámica** | El volumen escrito en la partitura. De más suave a más fuerte: `pp`, `p`, `mp`, `mf`, `f`, `ff`, `fff`. |
| **Voz** | Una línea musical independiente. Varias voces suenan a la vez, como distintos instrumentos de una banda. |
| **Articulación** | Cómo se atacan las notas: *legato* es pegadas y fluidas, *staccato* es cortas y separadas. |
| **Estrofa / estribillo / coda** | Las partes de una canción. El estribillo es lo que se repite, la coda es el cierre. |
| **Octava** | La misma nota, más aguda o más grave. Subir una octava son doce semitonos. |
| **Crescendo** | Subir el volumen poco a poco. |
| **Ritardando** | Frenar poco a poco, normalmente al final. |

---

## Cómo se aplican las reglas

Una regla **nunca se invoca**. Se escribe una vez y el sistema la vigila sola.

El sistema recorre la pieza compás por compás. Antes de hacer sonar cada uno:

1. **Toma una foto del estado** — compás, sección, voces, intensidad
2. **Evalúa las 15 reglas** contra esa foto, en orden de declaración
3. **Aplica las acciones** de las que se cumplieron
4. **Suena el compás**, ya con los ajustes

Las reglas leen el estado **como estaba al empezar el compás**, no como va quedando. Así el orden solo importa para las escrituras, nunca para las lecturas.

Si dos reglas fijan la misma propiedad en el mismo compás, **gana la última que se cumpla** y el sistema emite una advertencia. Ocurre a propósito entre las reglas 3 y 7 en la coda, para tener un caso concreto con el que justificar la política.

El recorrido completo, compás a compás, está en [`REGLAS.md`](REGLAS.md).

---

## Estructura del repositorio

```
PartituraEjecutable/
├── README.md                  ← este archivo
├── reglas.txt                 ← las 15 reglas en su forma oficial
├── palabras_reservadas.md     ← palabras reservadas, significado y categoría
└── REGLAS.md                  ← explicación detallada de cada regla
```

---

*Grupo 8 · Alarcon · Olaya · Garcia · Lenguajes Formales*
