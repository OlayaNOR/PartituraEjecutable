# Lexer de TocaScript — Paso 1: de Java a Python

Trabajo de la guía *De Java a Python: construyendo un lexer*. Cada archivo corre solo: `python archivo.py`.

## `mini-ejercicios/` — lo que se entrega

| Archivo | Mini-ejercicio | Listo cuando |
|---|---|---|
| `paso1.py` | Guardar nombre y edad, imprimirlos, cambiar la edad por la del próximo año y volver a imprimir | corre sin errores y los `print` muestran lo esperado |
| `paso4.py` | Recorrer un texto e imprimir solo los dígitos (`a1b22c` → 1, 2, 2) | funciona sin dígitos y terminando en dígito |
| `paso5.py` | Lista de tuplas `("DIGITO", c)` por cada dígito | la lista queda vacía sin dígitos |
| `paso6.py` | `digitos(texto)` devuelve la lista; se llama con tres textos | devuelve, no imprime; se puede llamar varias veces |
| `paso7.py` | `digitos` lanza `SyntaxError` si hay algo que no es dígito ni letra; `try` / `except` con `a1b` y `a1@` | el mensaje nombra el carácter |
| `paso7_tocascript.py` | **Entregable final:** el paso 7 personalizado, el lexer corto de la **declaración de TocaScript** (IDENTIFICADOR, NUMERO, TEXTO, BOOLEANO, NL) | tokeniza `tempo 100`, `compas "4/4"`, `umbral 0.7` y avisa del carácter inesperado, el número mal formado o el texto sin cerrar |

## El lexer del parcial 2 (23 y 24 de octubre)

Las tareas de *Trabajo en el proyecto*. Cada archivo trae todo lo de la tarea anterior más lo nuevo;
**`paso6_3.py` es el lexer completo** y `pruebas.py` corre los 6 casos del parcial (`python pruebas.py`).

| Tarea | Archivo | Qué cambió | Listo cuando |
|---|---|---|---|
| 1 · Columna | `lexer.py` | cada tupla lleva la columna donde empieza: `columna = i - inicio_linea + 1` | `tempo 100` → `tempo` en 1, `100` en 7 |
| 2 · Línea | `lexer.py` | `(tipo, texto, línea, columna)`; en cada `\n` se suma la línea y `inicio_linea = i` | `tempo 100\ncompas "4/4"` → `compas` en línea 2, columna 1 |
| 3 · Identificadores | `lexer.py` | letra, luego letras, dígitos o `_` | `tempo`, `umbral`, `integer` salen completos |
| 4 · Reservadas y tipos | `paso4.py` | conjuntos `TIPOS`, `LOGICOS` y `RESERVADAS`, comparados con la palabra completa | `motivo tema` → TIPO + IDENTIFICADOR; `motivos` no se parte |
| 5 · Asignación y fin | `paso5.py` | `SIMBOLOS_LARGOS` (`>=` `<=` `<>`) primero con `startswith`, luego `SIMBOLOS_1` (`=` `<` `>`); el fin de instrucción es el `NL` | `motivo tema = 5` da sus tokens; `:=` y `;` dan error |
| 6 · Comentarios | `paso6.py` | `#` (al inicio o tras un espacio) hasta el `\n`, sin consumirlo | un comentario al final no cambia los tokens ni la línea siguiente |
| 6.1 · Errores con posición | `paso6_1.py` | todos los errores dicen `Línea L, columna C:` | `int x = 5 @` → línea 1, columna 11 |
| 6.2 · Decimales y cadenas | `paso6_2.py` | un decimal lleva un solo punto; un texto no pasa de línea | `precio = 3.14` → `3.14` entero; `3.4.5` y la cadena sin cerrar dan error en la línea donde empiezan |
| 6.3 · Operadores | `paso6_3.py` | `OPERADORES = {"+", "-", "*", "/"}` → token `OPERADOR` | `volumen = tempo + 5 * 2` y `volumen=tempo+5*2` dan los mismos 7 tokens |
| 7 · Pruebas | `pruebas.py` | 3 casos válidos y 3 inválidos con la salida esperada calculada a mano | 6 de 6 coinciden |

```
'tempo 100\ncompas "4/4"'
   ('IDENTIFICADOR', 'tempo', 1, 1)
   ('NUMERO', '100', 1, 7)
   ('NL', '\\n', 1, 10)
   ('IDENTIFICADOR', 'compas', 2, 1)
   ('TEXTO', '4/4', 2, 8)
```

## Sesión 1 del 30 de octubre: lexer completo

Las tareas 8 a 12 siguen el mismo esquema: cada archivo trae todo lo del anterior más lo nuevo.
**`paso12.py` es ahora el lexer completo** y `pruebas_30oct.py` corre los 23 casos de la sesión
(los "listo cuando" de cada tarea más los 6 de la tarea 7, ahora con el `EOF`): `python pruebas_30oct.py`.

La guía plantea las tareas con Java; aquí se aplican a TocaScript, igual que en las tareas anteriores:

| Tarea | Archivo | Qué cambió | Listo cuando |
|---|---|---|---|
| 8 · Delimitadores | `paso8.py` | `( ) { } [ ] : , .` entran a `SIMBOLOS_1` → token `SIMBOLO`; el `.` de `3.14` lo consume antes el bloque del número | `(tempo+5)*2` da 7 tokens con sus columnas; `silencio:negra.` → `:` y `.` como SIMBOLO; `tema.parte` → IDENTIFICADOR, SIMBOLO, IDENTIFICADOR |
| 9 · Operadores de dos caracteres | `paso9.py` | `OPERADORES_LARGOS` (`>=` `<=` `<>`) se revisan primero con `startswith`; `<` y `>` pasan a `OPERADORES`. TocaScript no tiene `==` ni `!=` (su igual es `=` y su distinto `<>`); el `=` sigue como SIMBOLO porque también es la asignación | `x >= 5` da 3 tokens, `x > = 5` da 4 y `x ! 5` da error en la columna 3 |
| 10 · Control y booleanos | `paso10.py` | conjuntos `CONTROL` (`AL` `TOCAR` `repetir` `finales` `vez`, el control de TocaScript en vez de `if`/`else`/`while`) → RESERVADA, y `BOOLEANOS` (`true` `false`) → BOOLEANO; se compara con la palabra completa | `repetir` es RESERVADA; `repetirlo` y `repetir_x` son IDENTIFICADOR |
| 11 · Comentarios de bloque | `paso11.py` | `/* … */` se descarta aunque ocupe varias líneas; cada `\n` de adentro suma la línea y reinicia la columna sin generar `NL`. Se revisa antes que los operadores | un comentario de 3 líneas deja lo siguiente en la línea 4; sin cerrar → error en la línea y columna donde empezó |
| 12 · Fin de archivo | `paso12.py` | al terminar se agrega `("EOF", "", línea, columna)` con la posición final | `volumen = 5` da 3 tokens más EOF en 1:12; el texto vacío da solo `("EOF", "", 1, 1)` |

```
'tempo 120 /* uno\ndos\ntres */\nvolumen 80'
   ('IDENTIFICADOR', 'tempo', 1, 1)
   ('NUMERO', '120', 1, 7)
   ('NL', '\\n', 3, 8)
   ('IDENTIFICADOR', 'volumen', 4, 1)
   ('NUMERO', '80', 4, 9)
   ('EOF', '', 4, 11)
```

## Sesión 2 del 31 de octubre: lexer profesional

Las tareas 13 y 14 siguen el esquema de un archivo por tarea. En la 15 el lexer se reparte en módulos dentro de
**`compilador/`**, la carpeta donde irán las siguientes fases (parser, nodos, semántico, generador).
`pruebas_31oct.py` corre los 38 casos de la sesión: `python pruebas_31oct.py`.

| Tarea | Archivo | Qué cambió | Listo cuando |
|---|---|---|---|
| 13 · Clase Token | `paso13.py` | `@dataclass class Token` con `tipo`, `texto`, `linea` y `columna`; cada `tokens.append((...))` pasa a `tokens.append(Token(...))`. `__str__` imprime `NUMERO('5') en 1:9` | los 23 casos de `pruebas_30oct.py` dan lo mismo (se comparan con `astuple`) |
| 14 · Excepción propia | `paso14.py` | `class ErrorLexico(Exception)` guarda `mensaje`, `linea` y `columna`; los 6 `raise SyntaxError` pasan a `raise ErrorLexico(...)` con el formato `Error léxico en línea L, columna C: …`, y el carácter desconocido dice `carácter '@' no reconocido` | `try / except ErrorLexico as e` lee `e.linea` y `e.columna`; `tempo 120\nvolumen 2 @` → 2 y 11 |
| 15 · Leer un archivo | `compilador/` | `tokens.py` (Token y ErrorLexico), `lexer.py` (`tokenizar`) y `main.py`, que lee `sys.argv[1]` con `encoding="utf-8"` y muestra la tabla `LINEA COL TIPO TEXTO`. Con error léxico imprime solo el mensaje y sale con código 1. El tabulador se descarta como el espacio, porque ahora se leen archivos | `python main.py programa.txt` muestra la tabla y `python main.py programa_invalido.txt` da el error en 1:11 sin traza |
| 16 · Programa de ejemplo | `compilador/ejemplo.txt` | 36 líneas de TocaScript: cabecera con decimal y cadenas, comentario de línea y de bloque, motivos con acorde y puntillo, `repetir`, una sección, tres reglas `AL … TOCAR` con `>=`, `<`, `<>`, `Y`, `NO`, `*`, `+`, `-`, `mostrar`, y la pieza | se tokeniza sin errores y las 3 primeras líneas coinciden con el cálculo a mano |

```
cd compilador
python main.py programa.txt
LINEA  COL  TIPO           TEXTO
1      1    IDENTIFICADOR  tempo
1      7    NUMERO         120
1      10   NL             \n
2      1    IDENTIFICADOR  volumen
2      9    SIMBOLO        =
2      11   NUMERO         5
2      12   NL             \n
3      1    EOF

python main.py programa_invalido.txt
Error léxico en línea 1, columna 11: carácter '@' no reconocido
```

Las 3 primeras líneas de `ejemplo.txt`, calculadas a mano (la 1 es comentario y solo deja su `NL`):

```
# programa de ejemplo      ('NL', '\\n', 1, 22)
tempo 120                  ('IDENTIFICADOR', 'tempo', 2, 1)  ('NUMERO', '120', 2, 7)  ('NL', '\\n', 2, 10)
umbral 0.75                ('IDENTIFICADOR', 'umbral', 3, 1)  ('NUMERO', '0.75', 3, 8)  ('NL', '\\n', 3, 12)
```

## `paso2.py` y `paso3.py`

Los pasos 2 y 3 de la guía no tienen mini-ejercicio; son apuntes de apoyo (`len`, `t[i]`, `t[a:b]`, `if` / `elif` con `isdigit` e `isalpha`).

## La declaración de TocaScript frente a `int edad = 20;`

```
<cabecera> ::= <ajuste> <nl> <ajuste> <nl> <ajuste> <nl> { <ajuste> <nl> }
<ajuste>   ::= <variable> <valor>
```

| | Java | TocaScript | En el lexer |
|---|---|---|---|
| Tipo | `int` | no hay: el valor lleva el suyo | no existe el token TIPO; el valor es NUMERO, TEXTO o BOOLEANO |
| Signo igual | `=` | no hay en la cabecera | `=` es error léxico aquí |
| Fin de instrucción | `;` | salto de línea | `\n` **es un token** (`NL`), no se ignora |
| Nombre de variable | letra, luego letras/dígitos | `<letra>` solo minúsculas, luego letras, dígitos o `_` | una mayúscula en el nombre es *identificador inválido*; `AL`, `TOCAR` y `mostrar` salen como RESERVADA |
| Comentario | `//` y `/* … */` | `#` hasta el fin de línea y `/* … */` de bloque | no entra en la versión corta; lo descarta el lexer completo |

```
'tempo 100'     -> [('IDENTIFICADOR', 'tempo'), ('NUMERO', '100')]
'compas "4/4"'  -> [('IDENTIFICADOR', 'compas'), ('TEXTO', '4/4')]
'tempo = 100'   -> ERROR: Carácter inesperado '='
```

El lexer completo del lenguaje está en `../verificar.py`, función `tokenizar`.
