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

## `lexer.py` — el lexer que crece hasta el parcial 2

Parte de `paso7_tocascript.py` y va sumando las tareas de *Trabajo en el proyecto* (parcial 2: 23 y 24 de octubre).

| Tarea | Qué cambió | Listo cuando |
|---|---|---|
| 1 · Columna | cada tupla lleva la columna donde empieza: `columna = i - inicio_linea + 1` | `tempo 100` → `tempo` en 1, `100` en 7 |
| 2 · Línea | `(tipo, texto, línea, columna)`; en cada `\n` se suma la línea y `inicio_linea = i` (la columna vuelve a 1) | `tempo 100\ncompas "4/4"` → `compas` en línea 2, columna 1 |
| 3 · Identificadores | ya estaba: letra, luego letras, dígitos o `_` | `tempo`, `umbral`, `integer` salen completos |

```
'tempo 100\ncompas "4/4"'
   ('IDENTIFICADOR', 'tempo', 1, 1)
   ('NUMERO', '100', 1, 7)
   ('NL', '\\n', 1, 10)
   ('IDENTIFICADOR', 'compas', 2, 1)
   ('TEXTO', '4/4', 2, 8)
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
| Comentario | `//` | `#` hasta el fin de línea | no entra en la versión corta; lo descarta el lexer completo |

```
'tempo 100'     -> [('IDENTIFICADOR', 'tempo'), ('NUMERO', '100')]
'compas "4/4"'  -> [('IDENTIFICADOR', 'compas'), ('TEXTO', '4/4')]
'tempo = 100'   -> ERROR: Carácter inesperado '='
```

El lexer completo del lenguaje está en `../verificar.py`, función `tokenizar`.
