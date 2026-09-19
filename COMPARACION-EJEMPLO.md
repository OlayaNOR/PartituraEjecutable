# Comparación del ejemplo contra la gramática

**TocaScript · Grupo 8** · El programa de ejemplo, línea por línea, con la producción que la genera y los tokens que ve el lexer. Y el árbol completo del programa, producido por el parser (`verificar.py`) que implementa las 33 producciones.

## El programa

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

## Línea por línea

| Línea | Producción | Tokens del lexer | Categorías que aparecen |
|---|---|---|---|
| `tempo 100` | 3 `<ajuste>` (dentro de `<cabecera>`) | `tempo` · `100` | `<identificador>` (26); `<numero>` (28) |
| `compas "4/4"` | 3 `<ajuste>` (dentro de `<cabecera>`) | `compas` · `"4/4"` | `<identificador>` (26); `<texto>` (29) |
| `tonalidad "Do mayor"` | 3 `<ajuste>` (dentro de `<cabecera>`) | `tonalidad` · `"Do mayor"` | `<identificador>` (26); `<texto>` (29) |
| `(vacía)` | — | línea en blanco | `<nl>` extra; el lexer los colapsa |
| `motivo frase1 { do4:negra re4:negra mi4:negra do4:negra }` | 5 `<motivo>` | `motivo` · `frase1` · `{` · `do4` · `:` · `negra` · `re4` · `:` · `negra` · `mi4` · `:` · `negra` · `do4` · `:` · `negra` · `}` | `<identificador>` (26); `<nombre_figura>` (13); `<nota>` (9); terminal `":"`; terminal `"motivo"`; terminal `"{"`; terminal `"}"` |
| `motivo frase2 { mi4:negra fa4:negra sol4:blanca }` | 5 `<motivo>` | `motivo` · `frase2` · `{` · `mi4` · `:` · `negra` · `fa4` · `:` · `negra` · `sol4` · `:` · `blanca` · `}` | `<identificador>` (26); `<nombre_figura>` (13); `<nota>` (9); terminal `":"`; terminal `"motivo"`; terminal `"{"`; terminal `"}"` |
| `(vacía)` | — | línea en blanco | `<nl>` extra; el lexer los colapsa |
| `seccion cancion tipo estrofa { frase1 frase1 frase2 frase2 }` | 6 `<seccion>` | `seccion` · `cancion` · `tipo` · `estrofa` · `{` · `frase1` · `frase1` · `frase2` · `frase2` · `}` | `<identificador>` (26); `<tipo_seccion>` (7); terminal `"seccion"`; terminal `"tipo"`; terminal `"{"`; terminal `"}"` |
| `seccion cierre tipo coda { [do3 mi3 sol3 do4]:redonda }` | 6 `<seccion>` | `seccion` · `cierre` · `tipo` · `coda` · `{` · `[` · `do3` · `mi3` · `sol3` · `do4` · `]` · `:` · `redonda` · `}` | `<identificador>` (26); `<nombre_figura>` (13); `<nota>` (9); `<tipo_seccion>` (7); terminal `":"`; terminal `"["`; terminal `"]"`; terminal `"seccion"`; terminal `"tipo"`; terminal `"{"`; terminal `"}"` |
| `(vacía)` | — | línea en blanco | `<nl>` extra; el lexer los colapsa |
| `AL es_estrofa O hay_repeticion TOCAR dinamica = "mp"` | 14 `<regla>` | `AL` · `es_estrofa` · `O` · `hay_repeticion` · `TOCAR` · `dinamica` · `=` · `"mp"` | `<identificador>` (26); `<texto>` (29); terminal `"="` (comparación en `<condicion>`, asignación en `<accion>`); terminal `"AL"`; terminal `"O"`; terminal `"TOCAR"` |
| `AL es_coda TOCAR dinamica = "pp"` | 14 `<regla>` | `AL` · `es_coda` · `TOCAR` · `dinamica` · `=` · `"pp"` | `<identificador>` (26); `<texto>` (29); terminal `"="` (comparación en `<condicion>`, asignación en `<accion>`); terminal `"AL"`; terminal `"TOCAR"` |
| `AL (es_coda O es_final) Y NO tiene_percusion TOCAR tempo = tempo - 10` | 14 `<regla>` | `AL` · `(` · `es_coda` · `O` · `es_final` · `)` · `Y` · `NO` · `tiene_percusion` · `TOCAR` · `tempo` · `=` · `tempo` · `-` · `10` | `<identificador>` (26); `<numero>` (28); terminal `"("`; terminal `")"`; terminal `"-"`; terminal `"="` (comparación en `<condicion>`, asignación en `<accion>`); terminal `"AL"`; terminal `"NO"`; terminal `"O"`; terminal `"TOCAR"`; terminal `"Y"` |
| `(vacía)` | — | línea en blanco | `<nl>` extra; el lexer los colapsa |
| `pieza "Fray Santiago" { cancion cierre }` | 4 `<pieza>` | `pieza` · `"Fray Santiago"` · `{` · `cancion` · `cierre` · `}` | `<identificador>` (26); `<texto>` (29); terminal `"pieza"`; terminal `"{"`; terminal `"}"` |

## El árbol del programa (dos niveles)

```
<programa> (1)
  <cabecera> (2)
    <ajuste> (3)  → <variable> <valor>
    <nl> (33)  → "↵"
    <ajuste> (3)  → <variable> <valor>
    <nl> (33)  → "↵"
    <ajuste> (3)  → <variable> <valor>
    <nl> (33)  → "↵"
  <motivo> (5)
    "motivo"
    <identificador> (26)  → <letra> <letra> <letra> <letra> <letra> <digito>
    "{"
    <evento> (8)  → <nota> ":" <figura>
    <evento> (8)  → <nota> ":" <figura>
    <evento> (8)  → <nota> ":" <figura>
    <evento> (8)  → <nota> ":" <figura>
    "}"
    <nl> (33)  → "↵"
  <motivo> (5)
    "motivo"
    <identificador> (26)  → <letra> <letra> <letra> <letra> <letra> <digito>
    "{"
    <evento> (8)  → <nota> ":" <figura>
    <evento> (8)  → <nota> ":" <figura>
    <evento> (8)  → <nota> ":" <figura>
    "}"
    <nl> (33)  → "↵"
  <seccion> (6)
    "seccion"
    <identificador> (26)  → <letra> <letra> <letra> <letra> <letra> <letra> <letra>
    "tipo"
    <tipo_seccion> (7)  → "estrofa"
    "{"
    <identificador> (26)  → <letra> <letra> <letra> <letra> <letra> <digito>
    <identificador> (26)  → <letra> <letra> <letra> <letra> <letra> <digito>
    <identificador> (26)  → <letra> <letra> <letra> <letra> <letra> <digito>
    <identificador> (26)  → <letra> <letra> <letra> <letra> <letra> <digito>
    "}"
    <nl> (33)  → "↵"
  <seccion> (6)
    "seccion"
    <identificador> (26)  → <letra> <letra> <letra> <letra> <letra> <letra>
    "tipo"
    <tipo_seccion> (7)  → "coda"
    "{"
    <evento> (8)  → "[" <nota> <nota> <nota> <nota> "]" ":" <figura>
    "}"
    <nl> (33)  → "↵"
  <regla> (14)
    "AL"
    <expresion> (15)  → <termino> "O" <termino>
    "TOCAR"
    <acciones> (23)  → <accion>
    <nl> (33)  → "↵"
  <regla> (14)
    "AL"
    <expresion> (15)  → <termino>
    "TOCAR"
    <acciones> (23)  → <accion>
    <nl> (33)  → "↵"
  <regla> (14)
    "AL"
    <expresion> (15)  → <termino>
    "TOCAR"
    <acciones> (23)  → <accion>
    <nl> (33)  → "↵"
  <pieza> (4)
    "pieza"
    <texto> (29)  → '"' <mayuscula> <letra> <letra> <letra> " " <mayuscula> <letra> <letra> <letra> <letra> <letra> <letra> <letra> '"'
    "{"
    <identificador> (26)  → <letra> <letra> <letra> <letra> <letra> <letra> <letra>
    <identificador> (26)  → <letra> <letra> <letra> <letra> <letra> <letra>
    "}"
    <nl> (33)  → "↵"
```

El árbol completo tiene **371 nodos no terminales** y **298 hojas terminales**. Las hojas, leídas de izquierda a derecha, son el programa entero, símbolo a símbolo.

## Lo que la gramática comprueba y lo que no

| Gramática (sintaxis) | Intérprete (semántica) |
|---|---|
| Que la cabecera tenga tres ajustes, uno por línea | Que los tres sean `tempo`, `compas` y `tonalidad`, y con el tipo correcto |
| Que cada texto abra y cierre con `'"'` | Que `frase1` en la sección sea un motivo declarado |
| Que cada evento lleve figura | Que `cancion` y `cierre` sean secciones existentes |
| Que los paréntesis cierren | Que `es_estrofa`, `tempo`, `dinamica` estén entre las 20 variables |
| Que cada regla ocupe una línea | Que `"mp"` sea una dinámica válida |

## Cobertura

Las 33 producciones generan el ejemplo completo: cada token es un terminal entre comillas, o se abre hasta `<letra>`, `<digito>` y `<nl>`. El archivo `ejemplos/frere-jacques.toca` del repositorio usa además `simultaneo`, `voz … con …`, `repetir` y `exportar`, que pertenecen a la gramática extendida y no se sustentan en este parcial.
