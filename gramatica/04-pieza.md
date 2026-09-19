# Producción 4 · `<pieza>`

**Estructura del archivo** · Gramática BNF de TocaScript · Grupo 8

## La producción

La producción `<pieza>` y, debajo, todas las que abre hasta llegar a los átomos —terminales entre comillas—. Todo en un mismo sitio, como en el tablero.

```
 4  <pieza> ::= "pieza" <texto> "{" { <identificador> } "}" <nl>

29  <texto> ::= '"' { <letra> | <mayuscula> | <digito> | " " | "/" } '"'
30  <letra> ::= "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m"
              | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z"
31  <mayuscula> ::= "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M"
                  | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z"
32  <digito> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
26  <identificador> ::= <letra> { <letra> | <digito> | "_" }
                        # y no puede coincidir con ninguna palabra reservada
33  <nl> ::= "↵"
```

## Cómo se lee

La palabra `pieza`, un título entre comillas, y entre llaves la lista ordenada de nombres de sección. Termina en salto de línea.

## Qué usa y quién la usa

| | |
|---|---|
| **Terminales que aparecen** (entre comillas) | `"pieza"` · `"{"` · `"}"` |
| **No terminales que aparecen** (se abren en otra producción) | `<texto>` · `<identificador>` · `<nl>` |
| **Producciones que usan `<pieza>`** | `<programa>` |

## Ejemplo válido y su derivación

Cada ejemplo, y debajo el árbol que la gramática construye para él: cada nodo es una producción (con su número) y las hojas son terminales entre comillas. Derivación producida por el parser (`verificar.py`) que implementa estas 33 producciones; en `<identificador>`, `<numero>`, `<texto>` y `<nota>` se muestran directamente las hojas — cada carácter viene de `<letra>`, `<mayuscula>` o `<digito>`.

```
pieza "Fray Santiago" { cancion cierre }
```

```
<pieza> (4)
  "pieza"
  <texto> (29)  → '"' "F" "r" "a" "y" " " "S" "a" "n" "t" "i" "a" "g" "o" '"'
  "{"
  <identificador> (26)  → "c" "a" "n" "c" "i" "o" "n"
  <identificador> (26)  → "c" "i" "e" "r" "r" "e"
  "}"
  <nl> (33)  → "↵"
```

## Ejemplo inválido

```
pieza Fray Santiago { cancion cierre }
```

**Por qué no deriva:** El título tiene que ser un `<texto>`, con comillas. Sin ellas, `Fray` y `Santiago` serían identificadores — y además `Fray` empieza en mayúscula, que no es `<letra>`.

## Nota de diseño

Es el punto de entrada, el `main`. Que `cancion` y `cierre` existan como secciones lo comprueba el intérprete.

---
*Convención: `<x>` no terminal · `"x"` terminal · `'"'` la comilla doble como terminal · `{ }` cero o más · `[ ]` cero o uno · `|` alternativa · `<nl>` salto de línea*
