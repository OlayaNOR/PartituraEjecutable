# Producción 2 · `<cabecera>`

**Estructura del archivo** · Gramática BNF de TocaScript · Grupo 8

## La producción

La producción `<cabecera>` y, debajo, todas las que abre hasta llegar a los átomos —terminales entre comillas—. Todo en un mismo sitio, como en el tablero.

```
 2  <cabecera> ::= "tempo" <numero> <nl>
                   "compas" <texto> <nl>
                   "tonalidad" <texto> <nl>

26  <numero> ::= <digito> { <digito> } [ "." <digito> { <digito> } ]
30  <digito> ::= "0" | "1" | "2" | "..." | "9"
31  <nl> ::= "↵"
27  <texto> ::= '"' { <letra> | <mayuscula> | <digito> | " " | "/" } '"'
28  <letra> ::= "a" | "b" | "c" | "..." | "z"
29  <mayuscula> ::= "A" | "B" | "C" | "..." | "Z"
```

## Cómo se lee

Tres líneas, en este orden y todas obligatorias: la palabra `tempo` y un número; la palabra `compas` y un texto; la palabra `tonalidad` y un texto. Cada línea termina en salto de línea.

## Qué usa y quién la usa

| | |
|---|---|
| **Terminales que aparecen** (entre comillas) | `"tempo"` · `"compas"` · `"tonalidad"` |
| **No terminales que aparecen** (se abren en otra producción) | `<numero>` · `<nl>` · `<texto>` |
| **Producciones que usan `<cabecera>`** | `<programa>` |

## Ejemplo válido

```
tempo 100
compas "4/4"
tonalidad "Do mayor"
```

## Derivación del ejemplo hasta los átomos

Cada flecha aplica una producción; entre paréntesis, cuál. Al final solo quedan terminales entre comillas.

```
<cabecera>
→ "tempo" <numero> <nl>  "compas" <texto> <nl>  "tonalidad" <texto> <nl>   (2)
→ "tempo" <digito> <digito> <digito> <nl> …   (26 numero)
→ "tempo" "1" "0" "0" <nl> …   (30 digito)
→ … "compas" '"' <digito> "/" <digito> '"' <nl> …   (27 texto)
→ … "compas" '"' "4" "/" "4" '"' <nl> …   (30 digito)
→ … "tonalidad" '"' <mayuscula> <letra> " " <letra> <letra> <letra> <letra> <letra> '"' <nl>   (27 texto)
→ … "tonalidad" '"' "D" "o" " " "m" "a" "y" "o" "r" '"' <nl>   (29 mayuscula · 28 letra)

Resultado, leyendo solo los terminales:
tempo 100 ↵
compas "4/4" ↵
tonalidad "Do mayor" ↵
```

## Ejemplo inválido

```
tempo 100 compas "4/4" tonalidad "Do mayor"

tempo 100
compas 4/4
tonalidad "Do mayor"
```

**Por qué no deriva:** Primer caso: las tres en una línea, pero tras `<numero>` la producción exige `<nl>`. Segundo caso: `4/4` sin comillas no es un `<texto>` — `<texto>` empieza y termina en `'"'` (producción 27).

## Nota de diseño

Son las tres cosas que toda partitura escribe antes de la primera nota: la indicación de tempo, la cifra de compás y la armadura. No inventamos una cabecera: copiamos la de la partitura. Son obligatorias porque el sistema las necesita antes de sonar nada —sin tempo no sabe cuánto dura una negra, sin compás no sabe cuándo termina un compás— y van en orden fijo para que el parser lea tres líneas conocidas y ya. `tempo 100` es azúcar de `tempo = 100`: no declara la variable, le da valor inicial. Es la misma variable `tempo` que después consulta la regla 1 y modifica la regla 11. `compas` va entre comillas precisamente porque la barra de `4/4` sería, sin ellas, el operador de división.

---
*Convención: `<x>` no terminal · `"x"` terminal · `'"'` la comilla doble como terminal · `{ }` cero o más · `[ ]` cero o uno · `|` alternativa · `<nl>` salto de línea*
