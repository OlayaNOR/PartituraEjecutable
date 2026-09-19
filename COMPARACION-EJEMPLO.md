# Comparación del ejemplo contra la gramática

**TocaScript · Grupo 8** · Cada línea del programa de ejemplo, con la producción que la genera, los tokens que ve el lexer y cómo se abre cada uno hasta los átomos.

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

| Línea | Producción | Tokens | Cómo se abre hasta el fondo |
|---|---|---|---|
| `tempo 100` | 2 `<cabecera>` | `"tempo"` · `100` · `<nl>` | `<numero>` (26) → `<digito> <digito> <digito>` (30) → `"1" "0" "0"` |
| `compas "4/4"` | 2 `<cabecera>` | `"compas"` · `"4/4"` · `<nl>` | `<texto>` (27) → `'"' <digito> "/" <digito> '"'` → `'"' "4" "/" "4" '"'` — la barra es un carácter del texto, no el operador |
| `tonalidad "Do mayor"` | 2 `<cabecera>` | `"tonalidad"` · `"Do mayor"` · `<nl>` | `<texto>` → `'"' <mayuscula> <letra> " " <letra>… '"'` — `D` viene de `<mayuscula>` (29), el espacio es la alternativa `" "` |
| *(línea en blanco)* | 31 `<nl>` | `<nl>` | Varios saltos seguidos equivalen a uno |
| `motivo frase1 { do4:negra … }` | 4 `<motivo>` | `"motivo"` · `frase1` · `"{"` · (`do4` `":"` `negra`)×4 · `"}"` · `<nl>` | `<identificador>` (24) → `<letra>`×5 `<digito>` → `f r a s e 1` · `<evento>` (7) → `<nota> ":" <figura>` → `<nombre_nota>` `"do"` + `<octava>` `"4"` (8–10) · `<nombre_figura>` `"negra"` (11–12) |
| `motivo frase2 { mi4:negra fa4:negra sol4:blanca }` | 4 `<motivo>` | igual, 3 eventos | `sol4:blanca` → `"sol"` `"4"` `":"` `"blanca"` |
| `seccion cancion tipo estrofa { frase1 … }` | 5 `<seccion>` | `"seccion"` · `cancion` · `"tipo"` · `"estrofa"` · `"{"` · `frase1`×2 `frase2`×2 · `"}"` · `<nl>` | `<tipo_seccion>` (6) → `"estrofa"` · dentro, cuatro `<identificador>` |
| `seccion cierre tipo coda { [do3 mi3 sol3 do4]:redonda }` | 5 `<seccion>` | `"seccion"` · `cierre` · `"tipo"` · `"coda"` · `"{"` · `"["` `do3` `mi3` `sol3` `do4` `"]"` `":"` `redonda` · `"}"` · `<nl>` | Segunda alternativa de `<evento>`: `"[" <nota> { <nota> } "]" ":" <figura>` |
| `AL es_estrofa O hay_repeticion TOCAR dinamica = "mp"` | 13 `<regla>` | `"AL"` · `es_estrofa` · `"O"` · `hay_repeticion` · `"TOCAR"` · `dinamica` · `"="` · `"mp"` · `<nl>` | `<expresion>` (14) → `<termino> "O" <termino>` → cada uno `<factor>` → `<variable>` → `<identificador>` · `<accion>` (22) → `<variable> "=" <operando>` → `<valor>` → `<texto>` → `'"' "m" "p" '"'` |
| `AL es_coda TOCAR dinamica = "pp"` | 13 `<regla>` | `"AL"` · `es_coda` · `"TOCAR"` · `dinamica` · `"="` · `"pp"` · `<nl>` | La expresión es un solo `<factor>` → `<variable>`: una booleana sola ya es condición |
| `AL (es_coda O es_final) Y NO tiene_percusion TOCAR tempo = tempo - 10` | 13 `<regla>` | `"AL"` · `"("` · `es_coda` · `"O"` · `es_final` · `")"` · `"Y"` · `"NO"` · `tiene_percusion` · `"TOCAR"` · `tempo` · `"="` · `tempo` · `"-"` · `10` · `<nl>` | `<termino>` (15) → `<factor> "Y" <factor>` · 1.º `"(" <expresion> ")"` · 2.º `"NO" <factor>` (16) · `<operando>` (19) → `<operando> <op_aritmetico> <operando>` → `tempo` `"-"` `<numero>` → `"1" "0"` |
| `pieza "Fray Santiago" { cancion cierre }` | 3 `<pieza>` | `"pieza"` · `"Fray Santiago"` · `"{"` · `cancion` · `cierre` · `"}"` · `<nl>` | `<texto>` → `'"' <mayuscula> <letra><letra><letra> " " <mayuscula> <letra>… '"'` |

## Lo que comprueba la gramática y lo que no

| Gramática (sintaxis) | Intérprete (semántica) |
|---|---|
| Que la cabecera tenga tres líneas en orden | Que `frase1` en la sección sea un motivo declarado |
| Que cada texto abra y cierre con `'"'` | Que `cancion` y `cierre` sean secciones existentes |
| Que cada evento lleve figura | Que `es_estrofa`, `tempo`, `dinamica` estén entre las 20 variables |
| Que los paréntesis cierren | Que `"mp"` sea una dinámica válida |
| Que cada regla ocupe una línea | Que `tempo - 10` no dé negativo |

## Cobertura

Las 31 producciones generan el ejemplo completo: cada token es un terminal entre comillas de la gramática, o se abre hasta `<letra>`, `<digito>` y `<nl>`. Nada queda sin derivar.
