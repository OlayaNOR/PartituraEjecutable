# Producción 2 · `<cabecera>`

**Estructura del archivo** · Gramática BNF de TocaScript · Grupo 8

## La producción

La producción `<cabecera>` y, debajo, todas las que abre hasta llegar a los átomos —terminales entre comillas—. Todo en un mismo sitio, como en el tablero.

```
 2  <cabecera> ::= <ajuste> <nl>
                   <ajuste> <nl>
                   <ajuste> <nl>

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
33  <nl> ::= "↵"
```

## Cómo se lee

Tres ajustes, uno por línea, cada uno seguido de su salto de línea. Los tres son obligatorios y, por convención de la pieza, son `tempo`, `compas` y `tonalidad`, en ese orden.

## Qué usa y quién la usa

| | |
|---|---|
| **Terminales que aparecen** (entre comillas) | — |
| **No terminales que aparecen** (se abren en otra producción) | `<ajuste>` · `<nl>` |
| **Producciones que usan `<cabecera>`** | `<programa>` |

## Ejemplo válido y su derivación

Cada ejemplo, y debajo el árbol que la gramática construye para él: cada nodo es una producción (con su número) y las hojas son terminales entre comillas. Derivación producida por el parser (`verificar.py`) que implementa estas 33 producciones; en `<identificador>`, `<numero>`, `<texto>` y `<nota>` se muestran directamente las hojas — cada carácter viene de `<letra>`, `<mayuscula>` o `<digito>`.

```
tempo 100
compas "4/4"
tonalidad "Do mayor"
```

```
<cabecera> (2)
  <ajuste> (3)
    <variable> (25)
      <identificador> (26)  → "t" "e" "m" "p" "o"
    <valor> (27)
      <numero> (28)  → "1" "0" "0"
  <nl> (33)  → "↵"
  <ajuste> (3)
    <variable> (25)
      <identificador> (26)  → "c" "o" "m" "p" "a" "s"
    <valor> (27)
      <texto> (29)  → '"' "4" "/" "4" '"'
  <nl> (33)  → "↵"
  <ajuste> (3)
    <variable> (25)
      <identificador> (26)  → "t" "o" "n" "a" "l" "i" "d" "a" "d"
    <valor> (27)
      <texto> (29)  → '"' "D" "o" " " "m" "a" "y" "o" "r" '"'
  <nl> (33)  → "↵"
```

## Ejemplo inválido

```
tempo 100 compas "4/4" tonalidad "Do mayor"

tempo 100
compas 4/4
tonalidad "Do mayor"
```

**Por qué no deriva:** Primer caso: las tres en una línea, pero tras el primer `<ajuste>` la producción exige `<nl>`, y lo que viene es `compas`. Segundo caso: `4/4` no es un `<valor>` — `4` es un número, y después sobra `/ 4` antes del salto. La única forma de escribir un compás es como `<texto>`, entre comillas.

## Nota de diseño

Son las tres cosas que toda partitura escribe antes de la primera nota: tempo, cifra de compás y tonalidad. **`tempo`, `compas` y `tonalidad` no son palabras reservadas: son variables**, las mismas que después consultan y modifican las reglas (`AL tempo > 140 …`, `TOCAR tempo = tempo - 10`). La verificación regla por regla lo destapó: con `"tempo"` como palabra clave, cinco de las quince reglas no derivaban, porque una palabra no puede ser terminal y variable a la vez. Se ajustó la gramática, no las reglas: la cabecera es una lista de ajustes de variable.

---
*Convención: `<x>` no terminal · `"x"` terminal · `'"'` la comilla doble como terminal · `{ }` cero o más · `[ ]` cero o uno · `|` alternativa · `<nl>` salto de línea*
