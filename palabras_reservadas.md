# Palabras reservadas de TocaScript

**Grupo 8** · Dominio: interpretación musical

Una palabra reservada es un término que el lenguaje se guarda para sí mismo. **No puede usarse como nombre de variable, de motivo ni de acción.** Escribir `AL = 5` o `motivo repetir { }` es un error de sintaxis.

El lenguaje tiene dos partes y las palabras se agrupan igual:

| Parte | Para qué sirve | Se escribe |
|---|---|---|
| **Reglas** | Deciden cómo suena la pieza según lo que ocurra | MAYÚSCULAS |
| **Pieza** | Describe las notas, los motivos y las voces | minúsculas |

Esa diferencia de mayúsculas no es decorativa: es lo que permite distinguir de un vistazo una regla de una instrucción de la pieza, y es lo que evita que `AL` (regla) choque con cualquier palabra de la pieza.

---

# 1 · Convenciones léxicas

Antes de la lista, las reglas que gobiernan cómo se escribe cualquier cosa en el lenguaje.

| Elemento | Regla | Ejemplos válidos | Inválidos |
|---|---|---|---|
| **Identificador** | Empieza por letra minúscula, sigue con letras, dígitos o guion bajo | `tempo`, `compas_actual`, `frase1` | `Tempo`, `_x`, `2voces` |
| **Número entero** | Uno o más dígitos, con signo opcional | `96`, `-12`, `+5` | `1.` |
| **Número decimal** | Dígitos, punto, dígitos | `0.85`, `4.5` | `.5`, `0,85` |
| **Texto** | Entre comillas dobles, sin saltos de línea | `"ff"`, `"Do mayor"` | `'ff'` |
| **Booleano** | Solo dos valores | `true`, `false` | `verdadero`, `TRUE` |
| **Nota** | Nombre + alteración opcional + octava **obligatoria** | `do4`, `fa#4`, `mib3` | `do`, `fa#` |
| **Figura** | Dos puntos + nombre + puntillo opcional | `:negra`, `:negra.` | `:corchea3` |
| **Comentario** | `#` hasta el final de la línea | `# R1 - acento fuerte` | |

**El lenguaje distingue mayúsculas de minúsculas.** `AL` es una palabra reservada; `al` sería un identificador cualquiera.

**El fin de línea importa.** Una regla ocupa una línea. Dentro de un bloque `{ }` de la pieza, cada evento va en su línea o separado por espacios.

### El caso de `#`

`#` es a la vez marcador de comentario y símbolo de sostenido en `fa#4`. No hay ambigüedad porque el analizador léxico aplica **máxima coincidencia**: el patrón de nota

```
(do|re|mi|fa|sol|la|si) [#|b]? [0-9]
```

se reconoce como una sola unidad antes de que `#` pueda empezar un comentario. Por eso **la octava es obligatoria**: sin ella, `fa#` sería ambiguo. Escribir `fa#` sin octava es un error.

---

# 2 · Palabras reservadas de las reglas

Las cinco palabras que construyen una regla.

| Palabra | Categoría | Significado |
|---|---|---|
| `AL` | Palabra clave | Abre la regla. Lo que sigue es la condición que debe cumplirse. |
| `TOCAR` | Palabra clave | Separa la condición de la acción. Lo que sigue es lo que se ejecuta. |
| `Y` | Operador lógico | Conjunción. Las dos condiciones que une tienen que cumplirse. También une dos acciones para que se ejecuten ambas. |
| `O` | Operador lógico | Disyunción. Basta con que se cumpla una de las dos. |
| `NO` | Operador lógico | Negación. Invierte el valor de la condición que le sigue. |

### Por qué estas y no otras

| Palabra | Por qué |
|---|---|
| `AL` | Las reglas no se evalúan una vez: se revisan en **cada compás**. `AL` expresa algo que ocurre cada vez que se da la condición, no una decisión puntual. Y encaja con la forma de hablar del dominio: *al llegar al estribillo*, *al pasar el compás 24*. |
| `TOCAR` | Es el verbo central del lenguaje y la raíz de su nombre. Una regla no «ejecuta una acción»: dice cómo hay que **tocar** la música cuando se cumple la condición. |
| `Y` `O` | Son las palabras que un músico usaría: *fuerte y con percusión*, *en la coda o en el final*. |
| `NO` | «Cuando **no** haya percusión» aparece dos veces entre las 15 reglas. Sin `NO` habría que inventar una variable `sin_percusion`, duplicando información que ya existe. |

---

# 3 · Operadores

### Relacionales

| Operador | Categoría | Significado |
|---|---|---|
| `>` | Operador relacional | Mayor que. |
| `<` | Operador relacional | Menor que. |
| `>=` | Operador relacional | Mayor o igual que. |
| `<=` | Operador relacional | Menor o igual que. |
| `=` | Operador relacional | Igual a. |
| `<>` | Operador relacional | Distinto de. |

`>=`, `<=` y `<>` existen porque «cuatro voces o más» es una condición natural del dominio. Con solo `>` habría que escribir `num_voces > 3`, que dice lo mismo pero se lee peor.

### Aritméticos

| Operador | Categoría | Significado |
|---|---|---|
| `+` | Operador aritmético | Suma. |
| `-` | Operador aritmético | Resta. También marca un número negativo. |
| `*` | Operador aritmético | Multiplicación. |
| `/` | Operador aritmético | División. También separa las cifras de un compás: `4/4`. |

Solo aparecen en el valor de una acción: `tempo = tempo - 10`, `tempo = tempo * 0.85`.

### El doble papel de `=`

`=` significa dos cosas distintas, y **la posición decide cuál**:

| Dónde aparece | Qué significa | Ejemplo |
|---|---|---|
| Antes de `TOCAR` | Comparación | `AL compas_actual = 16 TOCAR …` |
| Después de `TOCAR` | Asignación | `… TOCAR dinamica = "ff"` |

No hay ambigüedad porque `TOCAR` marca la frontera: todo lo que va antes es una condición, todo lo que va después es una acción. El analizador sintáctico ya sabe en cuál de las dos está.

### Precedencia

De más fuerte a más débil:

```
1.  ( )                        agrupación
2.  * /                        multiplicación y división
3.  + -                        suma y resta
4.  NO                         negación
5.  >  <  =  >=  <=  <>        comparaciones
6.  Y                          conjunción
7.  O                          disyunción
```

**Por qué importa.** La regla 11 se escribe así:

```
AL (es_coda O es_final) Y NO tiene_percusion TOCAR tempo = tempo - 10
```

Sin los paréntesis, `Y` se evaluaría antes que `O` y la regla pasaría a significar *«si es la coda, o bien si es el final sin percusión»* — que no es lo que se quiere.

---

# 4 · Literales y símbolos

| Símbolo | Categoría | Significado |
|---|---|---|
| `true` | Literal booleano | Verdadero. |
| `false` | Literal booleano | Falso. |
| `"` | Delimitador | Abre y cierra un literal de texto. |
| `(` `)` | Delimitador | Agrupan condiciones y encierran los parámetros de un motivo. |
| `{` `}` | Delimitador | Delimitan un bloque: motivo, sección, voz, repetición. |
| `[` `]` | Delimitador | Encierran las notas de un acorde: `[do4 mi4 sol4]`. |
| `:` | Delimitador | Une un evento con su figura rítmica: `do4:negra`. |
| `,` | Delimitador | Separa parámetros: `escala(do4, 8)`. |
| `.` | Delimitador | Puntillo, alarga la figura a la mitad: `:negra.` También el punto decimal. |
| `~` | Delimitador | Ligadura, une dos figuras en un solo sonido: `la4:blanca ~ la4:negra`. |
| `#` | Símbolo | Comentario hasta fin de línea. También sostenido dentro de una nota. |
| `%` | Símbolo | Porcentaje, en `velocidad 200%`. |

---

# 5 · Palabras reservadas de la pieza

Estas construyen la música sobre la que actúan las reglas. Todas en minúsculas.

### Estructura

| Palabra | Categoría | Significado |
|---|---|---|
| `motivo` | Palabra clave | Declara un fragmento con nombre y reutilizable. |
| `acorde` | Palabra clave | Declara un grupo de notas con nombre que suenan a la vez. |
| `seccion` | Palabra clave | Declara una parte de la pieza. |
| `tipo` | Palabra clave | Indica el rol de una sección: `intro`, `estrofa`, `estribillo` o `coda`. |
| `pieza` | Palabra clave | Ordena las secciones en el tiempo. Es el punto de entrada. |
| `voz` | Palabra clave | Declara una línea musical independiente. |
| `simultaneo` | Palabra clave | Bloque cuyas voces empiezan todas en el mismo instante. |

### Ejecución y repetición

| Palabra | Categoría | Significado |
|---|---|---|
| `tocar` | Palabra clave | Ejecuta un motivo. |
| `repetir` | Palabra clave | Repite un bloque un número de veces: `repetir 4 { … }`. |
| `finales` | Palabra clave | Abre las casillas de una repetición que termina distinto cada vuelta. |
| `vez` | Palabra clave | Numera una casilla dentro de `finales`: `vez 1`, `vez 2`. |
| `con` | Palabra clave | Asocia una voz a su instrumento: `voz bajo con contrabajo`. |
| `silencio` | Palabra clave | Un evento en el que no suena nada. Lleva figura como cualquier nota. |
| `sin` `reglas` | Palabras clave | Bloque al que no se le aplica ninguna regla: `sin reglas { … }`. |
| `exportar` | Palabra clave | Escribe el resultado en un archivo. |

### Transformaciones

| Palabra | Categoría | Significado |
|---|---|---|
| `transportado` | Palabra clave | Toca el motivo desplazado en altura: `transportado +5 semitonos`. |
| `invertido` | Palabra clave | Espeja los intervalos del motivo. |
| `retrogradado` | Palabra clave | Toca el motivo al revés. |
| `semitonos` | Palabra clave | Unidad del transporte. Doce semitonos son una octava. |
| `velocidad` | Palabra clave | Cambia la velocidad de un motivo: `velocidad 200%`. |
| `en` | Palabra clave | Cambia la tonalidad de un motivo: `tocar cabeza en do menor`. |
| `crescendo` | Palabra clave | Sube el volumen de forma progresiva. |
| `hasta` | Palabra clave | Destino de un crescendo: `crescendo hasta ff`. |
| `durante` | Palabra clave | Duración de un efecto: `durante 2 compases`. |

### Tipos de sección

| Palabra | Categoría | Significado |
|---|---|---|
| `intro` | Literal de sección | Introducción. Pone `es_intro` en `true`. |
| `estrofa` | Literal de sección | Estrofa. Pone `es_estrofa` en `true`. |
| `estribillo` | Literal de sección | Estribillo, la parte que se repite. Pone `es_estribillo` en `true`. |
| `coda` | Literal de sección | Cierre. Pone `es_coda` en `true`. |

### Figuras rítmicas

Indican cuánto dura un evento. Cada una vale la mitad de la anterior.

| Palabra | Categoría | Duración en un compás de 4/4 |
|---|---|---|
| `redonda` | Literal de figura | 4 tiempos, el compás entero |
| `blanca` | Literal de figura | 2 tiempos |
| `negra` | Literal de figura | 1 tiempo |
| `corchea` | Literal de figura | medio tiempo |
| `semicorchea` | Literal de figura | un cuarto de tiempo |
| `fusa` | Literal de figura | un octavo de tiempo |

### Nombres de nota

| Palabra | Categoría | Significado |
|---|---|---|
| `do` `re` `mi` `fa` `sol` `la` `si` | Literal de nota | Nombre de la nota. Requiere octava: `do4`. Admite alteración: `fa#4` sostenido, `mib4` bemol. |

---

# 6 · Qué NO es palabra reservada

Todo lo demás lo define el grupo y podría llamarse de otra forma.

| Término | Qué es | Ejemplos |
|---|---|---|
| **Variables del dominio** | Guardan el estado sobre el que deciden las reglas | `tempo`, `compas`, `compas_actual`, `intensidad`, `num_voces`, `es_coda`, `hay_repeticion`, `dinamica`, `articulacion` |
| **Acciones** | Lo que una regla ordena hacer | `acentuar_primer_tiempo`, `activar_percusion`, `subir_una_octava`, `duplicar_octava` |
| **Nombres propios** | Motivos, secciones, voces y acordes que declara el programa | `cabeza`, `estribillo_final`, `melodia`, `Fa`, `Sol7` |
| **Literales de texto** | Son valores, no palabras del lenguaje | `"ff"`, `"legato"`, `"piano"` |
| **Nombres de instrumento** | Literales de texto, no palabras reservadas: `voz bajo con "contrabajo"`. Así el conjunto queda abierto sin reservar una palabra por cada instrumento | `"piano"`, `"flauta"`, `"violonchelo"` |

**Un detalle importante:** `tempo`, `compas`, `tonalidad`, `dinamica`, `articulacion` y `volumen` **son variables, no palabras reservadas**, aunque en la cabecera de una pieza parezcan comandos. La línea

```
tempo 96
```

es azúcar sintáctico de

```
tempo = 96
```

Gracias a eso, la misma variable que la pieza fija en su cabecera es la que las reglas consultan después. No hay dos conceptos, hay uno solo.

La lista completa de variables con su tipo de dato en Java está en el [README](README.md).

---

# 7 · Resumen

| Categoría | Cuántas | Cuáles |
|---|---|---|
| Palabras clave de regla | 2 | `AL` `TOCAR` |
| Operadores lógicos | 3 | `Y` `O` `NO` |
| Operadores relacionales | 6 | `>` `<` `=` `>=` `<=` `<>` |
| Operadores aritméticos | 4 | `+` `-` `*` `/` |
| Literales booleanos | 2 | `true` `false` |
| Delimitadores y símbolos | 13 | `"` `(` `)` `{` `}` `[` `]` `:` `,` `.` `~` `#` `%` |
| Palabras clave de estructura | 7 | `motivo` `acorde` `seccion` `tipo` `pieza` `voz` `simultaneo` |
| Palabras clave de ejecución | 9 | `tocar` `repetir` `finales` `vez` `con` `silencio` `sin` `reglas` `exportar` |
| Palabras clave de transformación | 9 | `transportado` `invertido` `retrogradado` `semitonos` `velocidad` `en` `crescendo` `hasta` `durante` |
| Literales de sección | 4 | `intro` `estrofa` `estribillo` `coda` |
| Literales de figura | 6 | `redonda` `blanca` `negra` `corchea` `semicorchea` `fusa` |
| Literales de nota | 7 | `do` `re` `mi` `fa` `sol` `la` `si` |

**72 términos reservados en total.** Los primeros seis bloques —los que construyen una regla— suman **30** y son los únicos que hacen falta para leer [`reglas.txt`](reglas.txt). Los otros 42 describen la pieza.

---

*Grupo 8 · Alarcon · Olaya · Garcia · Lenguajes Formales*
