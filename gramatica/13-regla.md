# Producción 13 · `<regla>`

**La regla de interpretación** · Gramática BNF de TocaScript · Grupo 8

## La producción

La producción `<regla>` y, debajo, todas las que abre hasta llegar a los átomos —terminales entre comillas—. Todo en un mismo sitio, como en el tablero.

```
13  <regla> ::= "AL" <expresion> "TOCAR" <acciones> <nl>

14  <expresion> ::= <termino> { "O" <termino> }
15  <termino> ::= <factor> { "Y" <factor> }
16  <factor> ::= "NO" <factor> | "(" <expresion> ")" | <condicion> | <variable>
17  <condicion> ::= <operando> <operador> <operando>
19  <operando> ::= <variable> | <valor> | <operando> <op_aritmetico> <operando>
23  <variable> ::= <identificador>
24  <identificador> ::= <letra> { <letra> | <digito> | "_" }
28  <letra> ::= "a" | "b" | "c" | "..." | "z"
30  <digito> ::= "0" | "1" | "2" | "..." | "9"
25  <valor> ::= <numero> | "true" | "false" | <texto>
26  <numero> ::= <digito> { <digito> } [ "." <digito> { <digito> } ]
27  <texto> ::= '"' { <letra> | <mayuscula> | <digito> | " " | "/" } '"'
29  <mayuscula> ::= "A" | "B" | "C" | "..." | "Z"
20  <op_aritmetico> ::= "+" | "-" | "*" | "/"
18  <operador> ::= ">" | "<" | ">=" | "<=" | "=" | "<>"
21  <acciones> ::= <accion> { "Y" <accion> }
22  <accion> ::= <variable> "=" <operando> | <identificador>
31  <nl> ::= "↵"
```

## Cómo se lee

La palabra `AL`, una expresión, la palabra `TOCAR`, una o más acciones, y el fin de la línea. Una regla ocupa exactamente una línea.

## Qué usa y quién la usa

| | |
|---|---|
| **Terminales que aparecen** (entre comillas) | `"AL"` · `"TOCAR"` |
| **No terminales que aparecen** (se abren en otra producción) | `<expresion>` · `<acciones>` · `<nl>` |
| **Producciones que usan `<regla>`** | `<programa>` |

## Ejemplo válido

```
AL es_coda TOCAR dinamica = "pp"
```

## Derivación del ejemplo hasta los átomos

Cada flecha aplica una producción; entre paréntesis, cuál. Al final solo quedan terminales entre comillas.

```
<regla>
→ "AL" <expresion> "TOCAR" <acciones> <nl>   (13)
→ "AL" <termino> "TOCAR" <acciones> <nl>   (14 expresion, un solo término)
→ "AL" <factor> "TOCAR" <acciones> <nl>   (15 termino, un solo factor)
→ "AL" <variable> "TOCAR" <acciones> <nl>   (16 factor, 4.ª alternativa)
→ "AL" <identificador> "TOCAR" <acciones> <nl>   (23 variable)
→ "AL" <letra> <letra> "_" <letra> <letra> <letra> <letra> "TOCAR" <acciones> <nl>  (24 identificador)
→ "AL" "e" "s" "_" "c" "o" "d" "a" "TOCAR" <acciones> <nl>   (28 letra)
→ … "TOCAR" <accion> <nl>   (21 acciones, una sola)
→ … "TOCAR" <variable> "=" <operando> <nl>   (22 accion, 1.ª alternativa)
→ … "TOCAR" "d" "i" "n" "a" "m" "i" "c" "a" "=" <valor> <nl>   (23, 24, 28 · 19 operando)
→ … "=" <texto> <nl>   (25 valor)
→ … "=" '"' <letra> <letra> '"' <nl>  →  '"' "p" "p" '"' <nl>   (27 texto · 28 letra)

Resultado:  AL es_coda TOCAR dinamica = "pp" ↵
```

## Ejemplo inválido

```
AL es_coda
TOCAR dinamica = "pp"
```

**Por qué no deriva:** La regla se partió en dos líneas: `<nl>` va después de `<acciones>`, no antes de `"TOCAR"`.

## Nota de diseño

`AL` y `TOCAR` son terminales obligatorios: marcan dónde empieza y dónde acaba la condición, así que el lexer puede cortar la regla en dos mitades sin entender la expresión. `AL` en vez de `SI` porque las reglas se revisan en cada compás —«al llegar al estribillo»—, y `TOCAR` en vez de `ENTONCES` porque es el verbo del dominio y la raíz del nombre del lenguaje. Las dos van en MAYÚSCULAS: las palabras de las reglas van en mayúsculas y los nombres de la pieza en minúsculas, así nunca chocan.

---
*Convención: `<x>` no terminal · `"x"` terminal · `'"'` la comilla doble como terminal · `{ }` cero o más · `[ ]` cero o uno · `|` alternativa · `<nl>` salto de línea*
