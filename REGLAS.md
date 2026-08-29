# Guía detallada de las 15 reglas

**Grupo 8** · Las reglas en su forma oficial están en [`reglas.txt`](reglas.txt). Este documento explica **qué hace cada una y por qué**, y cómo funciona el sistema que las procesa.

No hace falta saber música para leerlo: los términos musicales van explicados donde aparecen.

---

# Cómo se usan las reglas

Una regla **nunca se invoca**. Se escribe una vez y el sistema la vigila sola.

## El ciclo

El sistema recorre la pieza **compás por compás** — un compás es cada trozo de igual duración en que se divide la música, como los renglones de un cuaderno. Antes de hacer sonar cada compás:

1. **Toma una foto del estado** — en qué compás va, qué sección suena, cuántas voces hay, cuánta intensidad
2. **Evalúa las 15 reglas** contra esa foto, en orden de declaración
3. **Aplica las acciones** de las reglas que se cumplieron
4. **Suena el compás**, ya con los ajustes aplicados

Y repite. En ningún lado del programa se escribe «aplicar la regla 6».

## De dónde salen las variables

**Las booleanas de sección** las declara la propia sección de la pieza:

```
seccion coro tipo estribillo { ... }
```

Mientras suena `coro`, `es_estribillo` vale `true`. Los tipos disponibles son `intro`, `estrofa`, `estribillo` y `coda`; `es_final` lo marca el sistema en la última sección de la pieza.

**`intensidad`** se deriva de la dinámica vigente, que es el volumen escrito en la partitura:

| Dinámica | `"pp"` | `"p"` | `"mp"` | `"mf"` | `"f"` | `"ff"` | `"fff"` |
|---|---|---|---|---|---|---|---|
| intensidad | 0.1 | 0.25 | 0.4 | 0.55 | 0.7 | 0.85 | 1.0 |

**Las demás** las lleva el sistema solo: `compas_actual`, `duracion_total`, `num_voces`, `nota_actual`, `repeticion_actual`, `volumen` y `tiene_percusion`. `permitir_agudos` es una bandera que declara la pieza.

## La foto se toma antes, no durante

Las reglas leen el estado **como estaba al empezar el compás**, no como va quedando. Si la regla 6 activa la percusión, la regla 14 en ese mismo compás sigue viendo `tiene_percusion` en `false`; lo verá en `true` en el compás siguiente.

Sin esta regla tendrías cascadas en las que una regla dispara a otra dentro del mismo compás, y el resultado dependería del orden de formas difíciles de predecir.

## Un recorrido completo

Pieza de 12 compases a tempo 96:

| Compás | Sección | Reglas que se cumplen | Resultado |
|---|---|---|---|
| 1–2 | intro | **R4** (`es_intro`) | dinámica `"p"` |
| 3–6 | estrofa | **R9** (`es_estrofa`) | dinámica `"mp"` |
| 7 | estribillo · int. 0.8 | **R6** (`es_estribillo Y intensidad > 0.7`) | entra la percusión |
| 8 | estribillo | **R5** (`num_voces > 3`)<br>**R14** (`num_voces >= 4 Y tiene_percusion`) | staccato · volumen −15 |
| 9–10 | estribillo · int. 0.9 | **R12** (`intensidad >= 0.9 Y es_estribillo`) | clímax: `"fff"` y melodía duplicada |
| 11 | coda | **R3** (`es_coda`) → `"pp"`<br>**R7** (`… O es_coda`) → crescendo<br>**R11** — *no se cumple* | ⚠️ chocan, gana la R7<br>la R11 no dispara: hay percusión desde el compás 7 |
| 12 | coda · final | **R15** (`compas_actual >= 12 − 2 Y es_final`) | tempo 96 → 81.6, frena al cerrar |

Tres cosas que este recorrido enseña:

- **La R2 nunca se cumple** en esta pieza: espera un compás de `"3/4"` y la pieza está en `"4/4"`. No es un error, pero como `compas` se fija una sola vez en la cabecera y no cambia, el sistema puede detectarlo **antes de ejecutar** y avisar: *«la regla 2 nunca se cumplirá»*. Es análisis estático, no de ejecución.
- **La R11 no dispara, y está bien.** Pide que no haya percusión, pero la R6 la activó en el compás 7. El resultado es correcto: la pieza no frena porque la percusión marca un pulso fijo.
- **Las R3 y R7 sí chocan de verdad**, y es a propósito. Ver la nota al final.

---

# Grupo A · Una sola condición

Se pregunta **una sola cosa**. Sin `Y`, sin `O`. *Son cinco.*

### R1 — acento fuerte

```
AL tempo > 140 TOCAR dinamica = "ff"
```

Si la pieza va rápido, a más de 140 pulsos por minuto, tócala fuerte. La música rápida pide energía: sonaría raro un tema veloz tocado suavecito.

### R2 — acento de vals

```
AL compas = "3/4" TOCAR acentuar_primer_tiempo
```

En un compás de tres tiempos, marca el primero con más fuerza. Es lo que hace que un vals suene a vals: el *chun*-ta-ta. En un compás de cuatro no aplica, porque ahí el acento se reparte distinto.

> Esta es la única de las quince que compara contra un **texto**. Las demás comparan números o booleanos, así que entre las tres se ejercitan los tres tipos de dato del lenguaje.

### R3 — cierre suave

```
AL es_coda TOCAR dinamica = "pp"
```

En el cierre de la pieza, baja al volumen más suave. Es la forma clásica de terminar, apagándose. La *coda* es la sección final de una canción.

> Aquí no hay comparación: `es_coda` ya vale `true` o `false` por sí sola, así que **ya es una condición**. La forma larga equivalente es `es_coda = true`.

### R4 — entrada tenue

```
AL es_intro TOCAR dinamica = "p"
```

La introducción se toca suave. Empezar bajito deja espacio para crecer después.

### R5 — aclarar la textura

```
AL num_voces > 3 TOCAR articulacion = "staccato"
```

Si hay más de tres instrumentos sonando a la vez, que toquen las notas cortas y separadas (*staccato*) en vez de largas y pegadas. Con muchos instrumentos el sonido se vuelve un manchón; acortar las notas deja oír cada una.

---

# Grupo B · Condiciones compuestas con Y / O

Dos o más condiciones unidas por conectores. *Son seis.*

### R6 — empuje del estribillo

```
AL es_estribillo Y intensidad > 0.7 TOCAR activar_percusion
```

Si estamos en el estribillo —la parte que se repite— y además la música va intensa, entra la batería. El estribillo es el momento más alto de una canción y la percusión lo levanta todavía más.

**Ojo:** tienen que cumplirse **las dos**. Un estribillo tranquilo no activa la batería.

### R7 — final abierto

```
AL compas_actual > 24 O es_coda TOCAR aplicar_crescendo
```

Si ya pasamos el compás 24 **o bien** estamos en el cierre, sube el volumen poco a poco. Anuncia que la pieza se acerca al final.

**Ojo:** con `O` basta con que se cumpla **una** de las dos.

### R8 — textura ligera

```
AL tempo < 80 Y NO hay_repeticion TOCAR articulacion = "legato"
```

Si la pieza va lenta y no estamos dentro de una repetición, toca las notas pegadas y fluidas (*legato*). Lo lento pide suavidad, pero durante una repetición conviene marcar más para que se note que es la misma parte otra vez.

**Ojo:** `NO hay_repeticion` significa *«cuando NO estemos repitiendo»*.

### R9 — contraste de secciones

```
AL es_estrofa O hay_repeticion TOCAR dinamica = "mp"
```

En las estrofas y dentro de cualquier repetición, volumen medio-bajo. Deja al estribillo destacar por contraste: si todo suena igual de fuerte, nada resalta.

> **Nota de diseño.** Esta regla decía antes `es_estrofa O es_intro`, y eso creaba un choque real: en la introducción también se cumplía la R4, y como la R9 se declara después le ganaba siempre, dejando la R4 sin efecto. Se cambió `es_intro` por `hay_repeticion`, que cubre el mismo propósito sin pisar a nadie.

### R10 — segunda vuelta

```
AL hay_repeticion Y repeticion_actual = 2 TOCAR subir_una_octava
```

Cuando estamos repitiendo y además es la segunda vuelta, toca todo una octava más agudo. Repetir algo idéntico aburre; subirlo de tono lo renueva sin cambiar la melodía. Una octava es la misma nota, más aguda.

### R11 — aire al final

```
AL (es_coda O es_final) Y NO tiene_percusion TOCAR tempo = tempo - 10
```

Si estamos en el cierre o en la última sección, y además no hay percusión sonando, baja la velocidad diez puntos. Ralentizar al final da sensación de cierre, pero con batería sonando frenar suena mal: la percusión marca un pulso fijo.

**Ojo con los paréntesis:** son obligatorios. Sin ellos, `Y` se evalúa antes que `O` y la regla pasaría a decir *«si es la coda, o bien si es el final sin percusión»*, que no es lo mismo.

---

# Grupo C · Tipos distintos combinados

En la misma condición conviven **un número** y **un booleano**. *Son cuatro.*

Cómo funciona: una comparación como `intensidad >= 0.9` es una pregunta numérica cuya respuesta es `true` o `false`. Esa respuesta se conecta con `Y` a una variable que ya era booleana de nacimiento. Así conviven los dos tipos.

### R12 — clímax

```
AL intensidad >= 0.9 Y es_estribillo TOCAR dinamica = "fff" Y duplicar_octava
```

Si la intensidad está casi al máximo y estamos en el estribillo, sube al volumen más alto y duplica la melodía una octava arriba. Es el punto más alto de la pieza: duplicarla más aguda la hace sonar el doble de grande.

**Los dos tipos:** `intensidad` es `double` · `es_estribillo` es `boolean`.

### R13 — seguridad de tesitura

```
AL nota_actual > 91 Y NO permitir_agudos TOCAR bajar_una_octava
```

Si la nota que va a sonar es más aguda que el `sol6` y la pieza no autorizó agudos, bájala una octava. Protege de notas tan agudas que ningún instrumento real puede tocarlas, o que suenan chillonas. *Tesitura* es el rango de notas que un instrumento alcanza.

**Los dos tipos:** `nota_actual` es `int` — 91 es el `sol6` en notación MIDI — · `permitir_agudos` es `boolean`.

### R14 — no saturar la mezcla

```
AL num_voces >= 4 Y tiene_percusion TOCAR volumen = volumen - 15
```

Si hay cuatro o más voces sonando y una de ellas es percusión, baja el volumen general quince puntos. Muchos instrumentos a la vez más batería satura el sonido y distorsiona.

**Los dos tipos:** `num_voces` es `int` · `tiene_percusion` es `boolean`.
**Detalle:** el volumen nuevo se calcula a partir del actual, no se fija en un valor.

### R15 — ritardando final

```
AL compas_actual >= duracion_total - 2 Y es_final TOCAR tempo = tempo * 0.85
```

Cuando faltan dos compases o menos para terminar y estamos en la última sección, baja la velocidad al 85%. *Ritardando* es frenar poco a poco al final; es la forma más común de cerrar una pieza.

**Los dos tipos:** `compas_actual` y `duracion_total` son `int` · `es_final` es `boolean`.

---

## Dos aclaraciones honestas

**1. Los grupos B y C se solapan.** Las reglas 6, 7, 8 y 10 *también* mezclan un número con un booleano. Se clasificaron en el grupo B porque lo que las define principalmente es el uso de conectores lógicos. Las únicas del grupo B con condición puramente booleana son la **R9** y la **R11**.

**2. Qué pasa cuando dos reglas chocan.** Las 15 se revisan en cada compás, en orden. Si dos fijan la misma propiedad en el mismo momento, **gana la última que se cumpla** y el sistema emite una advertencia.

Ejemplo real dentro de estas 15: en la coda, la **R3** baja la dinámica a `"pp"` y la **R7** pide un crescendo. Como la R7 va después, gana la R7. No es un descuido: está así a propósito para tener un caso concreto con el que justificar la política de resolución de conflictos.

---

*Grupo 8 · Alarcon · Olaya · Garcia · Lenguajes Formales*
