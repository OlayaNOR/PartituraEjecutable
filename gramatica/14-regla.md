# Producción 14 · `<regla>`

**La regla de interpretación** · Gramática BNF de TocaScript · Grupo 8

## La producción

La producción `<regla>` y, debajo, todas las que abre hasta llegar a los átomos —terminales entre comillas—. Todo en un mismo sitio, como en el tablero.

```
14  <regla> ::= "AL" <expresion> "TOCAR" <acciones> <nl>

15  <expresion> ::= <termino> { "O" <termino> }
16  <termino> ::= <factor> { "Y" <factor> }
17  <factor> ::= "NO" <factor>
               | "(" <expresion> ")"
               | <condicion>
               | <variable>
18  <condicion> ::= <operando> <operador> <operando>
20  <operando> ::= <sumando> { "+" <sumando> | "-" <sumando> }
21  <sumando> ::= <primario> { "*" <primario> | "/" <primario> }
22  <primario> ::= <variable> | <valor> | "(" <operando> ")"
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
19  <operador> ::= ">" | "<" | ">=" | "<=" | "=" | "<>"
23  <acciones> ::= <accion> { "Y" <accion> }
24  <accion> ::= <variable> "=" <operando>
               | <identificador>
33  <nl> ::= "↵"
```

## Cómo se lee

La palabra `AL`, una expresión, la palabra `TOCAR`, una o más acciones, y el fin de la línea. Una regla ocupa exactamente una línea.

## Qué usa y quién la usa

| | |
|---|---|
| **Terminales que aparecen** (entre comillas) | `"AL"` · `"TOCAR"` |
| **No terminales que aparecen** (se abren en otra producción) | `<expresion>` · `<acciones>` · `<nl>` |
| **Producciones que usan `<regla>`** | `<programa>` |

## Ejemplo válido y su derivación

Cada ejemplo, y debajo el árbol que la gramática construye para él: cada nodo es una producción (con su número) y las hojas son terminales entre comillas. Derivación producida por el parser (`verificar.py`) que implementa estas 33 producciones; en `<identificador>`, `<numero>`, `<texto>` y `<nota>` se muestran directamente las hojas — cada carácter viene de `<letra>`, `<mayuscula>` o `<digito>`.

```
AL es_coda TOCAR dinamica = "pp"
```

```
<regla> (14)
  "AL"
  <expresion> (15)
    <termino> (16)
      <factor> (17)
        <variable> (25)
          <identificador> (26)  → "e" "s" "_" "c" "o" "d" "a"
  "TOCAR"
  <acciones> (23)
    <accion> (24)
      <variable> (25)
        <identificador> (26)  → "d" "i" "n" "a" "m" "i" "c" "a"
      "="
      <operando> (20)
        <sumando> (21)
          <primario> (22)
            <valor> (27)
              <texto> (29)  → '"' "p" "p" '"'
  <nl> (33)  → "↵"
```

```
AL es_estribillo Y intensidad > 0.7 TOCAR activar_percusion
```

```
<regla> (14)
  "AL"
  <expresion> (15)
    <termino> (16)
      <factor> (17)
        <variable> (25)
          <identificador> (26)  → "e" "s" "_" "e" "s" "t" "r" "i" "b" "i" "l" "l" "o"
      "Y"
      <factor> (17)
        <condicion> (18)
          <operando> (20)
            <sumando> (21)
              <primario> (22)
                <variable> (25)
                  <identificador> (26)  → "i" "n" "t" "e" "n" "s" "i" "d" "a" "d"
          <operador> (19)
            ">"
          <operando> (20)
            <sumando> (21)
              <primario> (22)
                <valor> (27)
                  <numero> (28)  → "0" "." "7"
  "TOCAR"
  <acciones> (23)
    <accion> (24)
      <identificador> (26)  → "a" "c" "t" "i" "v" "a" "r" "_" "p" "e" "r" "c" "u" "s" "i" "o" "n"
  <nl> (33)  → "↵"
```

## Ejemplo inválido

```
AL es_coda
TOCAR dinamica = "pp"
```

**Por qué no deriva:** La regla se partió en dos líneas: `<nl>` va después de `<acciones>`, no antes de `"TOCAR"`.

## Nota de diseño

`AL` y `TOCAR` son terminales obligatorios: marcan dónde empieza y dónde acaba la condición, así que el lexer puede cortar la regla en dos mitades sin entender la expresión. `AL` en vez de `SI` porque las reglas se revisan en cada compás —«al llegar al estribillo»—, y `TOCAR` en vez de `ENTONCES` porque es el verbo del dominio y la raíz del nombre del lenguaje. Las dos van en MAYÚSCULAS: las palabras de las reglas en mayúsculas y los nombres en minúsculas, así nunca chocan.

---
*Convención: `<x>` no terminal · `"x"` terminal · `'"'` la comilla doble como terminal · `{ }` cero o más · `[ ]` cero o uno · `|` alternativa · `<nl>` salto de línea*
