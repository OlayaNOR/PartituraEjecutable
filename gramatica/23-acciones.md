# Producción 23 · `<acciones>`

**La regla de interpretación** · Gramática BNF de TocaScript · Grupo 8

## La producción

La producción `<acciones>` y, debajo, todas las que abre hasta llegar a los átomos —terminales entre comillas—. Todo en un mismo sitio, como en el tablero.

```
23  <acciones> ::= <accion> { "Y" <accion> }

24  <accion> ::= <variable> "=" <operando>
               | <identificador>
25  <variable> ::= <identificador>
26  <identificador> ::= <letra> { <letra> | <digito> | "_" }
                        # y no puede coincidir con ninguna palabra reservada
30  <letra> ::= "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m"
              | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z"
32  <digito> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
20  <operando> ::= <sumando> { "+" <sumando> | "-" <sumando> }
21  <sumando> ::= <primario> { "*" <primario> | "/" <primario> }
22  <primario> ::= <variable> | <valor> | "(" <operando> ")"
27  <valor> ::= <numero> | "true" | "false" | <texto>
28  <numero> ::= <digito> { <digito> } [ "." <digito> { <digito> } ]
29  <texto> ::= '"' { <letra> | <mayuscula> | <digito> | " " | "/" } '"'
31  <mayuscula> ::= "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M"
                  | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z"
```

## Cómo se lee

Una acción, o varias unidas por `Y`.

## Qué usa y quién la usa

| | |
|---|---|
| **Terminales que aparecen** (entre comillas) | `"Y"` |
| **No terminales que aparecen** (se abren en otra producción) | `<accion>` |
| **Producciones que usan `<acciones>`** | `<regla>` |

## Ejemplo válido y su derivación

Cada ejemplo, y debajo el árbol que la gramática construye para él: cada nodo es una producción (con su número) y las hojas son terminales entre comillas. Derivación producida por el parser (`verificar.py`) que implementa estas 33 producciones; en `<identificador>`, `<numero>`, `<texto>` y `<nota>` se muestran directamente las hojas — cada carácter viene de `<letra>`, `<mayuscula>` o `<digito>`.

```
dinamica = "fff" Y duplicar_octava
```

```
<acciones> (23)
  <accion> (24)
    <variable> (25)
      <identificador> (26)  → "d" "i" "n" "a" "m" "i" "c" "a"
    "="
    <operando> (20)
      <sumando> (21)
        <primario> (22)
          <valor> (27)
            <texto> (29)  → '"' "f" "f" "f" '"'
  "Y"
  <accion> (24)
    <identificador> (26)  → "d" "u" "p" "l" "i" "c" "a" "r" "_" "o" "c" "t" "a" "v" "a"
```

## Ejemplo inválido

```
dinamica = "fff", duplicar_octava
```

**Por qué no deriva:** Las acciones se unen con `"Y"`, no con coma.

## Nota de diseño

Aquí `Y` no compara: significa «y además». Lo distingue estar después de `TOCAR`.

---
*Convención: `<x>` no terminal · `"x"` terminal · `'"'` la comilla doble como terminal · `{ }` cero o más · `[ ]` cero o uno · `|` alternativa · `<nl>` salto de línea*
