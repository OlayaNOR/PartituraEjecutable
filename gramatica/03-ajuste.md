# Producción 3 · `<ajuste>`

**Estructura del archivo** · Gramática BNF de TocaScript · Grupo 8

## La producción

La producción `<ajuste>` y, debajo, todas las que abre hasta llegar a los átomos —terminales entre comillas—. Todo en un mismo sitio, como en el tablero.

```
 3  <ajuste> ::= <variable> <valor>

25  <variable> ::= <identificador>
26  <identificador> ::= <letra> { <letra> | <digito> | "_" }
                        # y no puede coincidir con ninguna palabra reservada
30  <letra> ::= "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m"
              | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z"
32  <digito> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
27  <valor> ::= <numero> | "true" | "false" | <texto>
28  <numero> ::= <digito> { <digito> } [ "." <digito> { <digito> } ]
29  <texto> ::= '"' { <letra> | <mayuscula> | <digito> | " " | "/" } '"'
31  <mayuscula> ::= "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M"
                  | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z"
```

## Cómo se lee

Una variable seguida de un valor, sin signo igual. `tempo 100` es azúcar sintáctico de `tempo = 100`.

## Qué usa y quién la usa

| | |
|---|---|
| **Terminales que aparecen** (entre comillas) | — |
| **No terminales que aparecen** (se abren en otra producción) | `<variable>` · `<valor>` |
| **Producciones que usan `<ajuste>`** | `<cabecera>` |

## Ejemplo válido y su derivación

Cada ejemplo, y debajo el árbol que la gramática construye para él: cada nodo es una producción (con su número) y las hojas son terminales entre comillas. Derivación producida por el parser (`verificar.py`) que implementa estas 33 producciones; en `<identificador>`, `<numero>`, `<texto>` y `<nota>` se muestran directamente las hojas — cada carácter viene de `<letra>`, `<mayuscula>` o `<digito>`.

```
tempo 100
```

```
<ajuste> (3)
  <variable> (25)
    <identificador> (26)  → "t" "e" "m" "p" "o"
  <valor> (27)
    <numero> (28)  → "1" "0" "0"
```

```
compas "4/4"
```

```
<ajuste> (3)
  <variable> (25)
    <identificador> (26)  → "c" "o" "m" "p" "a" "s"
  <valor> (27)
    <texto> (29)  → '"' "4" "/" "4" '"'
```

```
tonalidad "Do mayor"
```

```
<ajuste> (3)
  <variable> (25)
    <identificador> (26)  → "t" "o" "n" "a" "l" "i" "d" "a" "d"
  <valor> (27)
    <texto> (29)  → '"' "D" "o" " " "m" "a" "y" "o" "r" '"'
```

## Ejemplo inválido

```
tempo = 100
Tempo 100
```

**Por qué no deriva:** El `=` no existe en la cabecera; ese signo solo aparece dentro de las reglas. `Tempo` empieza en mayúscula, y `<variable>` → `<identificador>` empieza por `<letra>`, que solo tiene minúsculas.

## Nota de diseño

La gramática fija la forma: variable y valor. Que las tres variables sean exactamente `tempo`, `compas` y `tonalidad`, y que el valor tenga el tipo correcto —número para el tempo, texto para las otras dos— lo comprueba el intérprete, no la gramática.

---
*Convención: `<x>` no terminal · `"x"` terminal · `'"'` la comilla doble como terminal · `{ }` cero o más · `[ ]` cero o uno · `|` alternativa · `<nl>` salto de línea*
