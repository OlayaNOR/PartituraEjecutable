# Producción 26 · `<identificador>`

**Nombres y valores** · Gramática BNF de TocaScript · Grupo 8

## La producción

La producción `<identificador>` y, debajo, todas las que abre hasta llegar a los átomos —terminales entre comillas—. Todo en un mismo sitio, como en el tablero.

```
26  <identificador> ::= <letra> { <letra> | <digito> | "_" }
                        # y no puede coincidir con ninguna palabra reservada

30  <letra> ::= "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m"
              | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z"
32  <digito> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
```

## Cómo se lee

Una letra minúscula, seguida de cero o más letras, dígitos o guiones bajos. Y **no puede ser una palabra reservada**: `true`, `motivo`, `coda`, `negra`… ya tienen dueño. Esa restricción no se puede escribir en BNF puro, por eso va como comentario, y es el lexer quien la aplica al clasificar cada token.

## Qué usa y quién la usa

| | |
|---|---|
| **Terminales que aparecen** (entre comillas) | `"_"` |
| **No terminales que aparecen** (se abren en otra producción) | `<letra>` · `<digito>` |
| **Producciones que usan `<identificador>`** | `<pieza>` · `<motivo>` · `<seccion>` · `<accion>` · `<variable>` |

## Ejemplo válido y su derivación

Cada ejemplo, y debajo el árbol que la gramática construye para él: cada nodo es una producción (con su número) y las hojas son terminales entre comillas. Derivación producida por el parser (`verificar.py`) que implementa estas 33 producciones; en `<identificador>`, `<numero>`, `<texto>` y `<nota>` se muestran directamente las hojas — cada carácter viene de `<letra>`, `<mayuscula>` o `<digito>`.

```
frase1
```

```
<identificador> (26)
  <letra> (30)
    "f"
  <letra> (30)
    "r"
  <letra> (30)
    "a"
  <letra> (30)
    "s"
  <letra> (30)
    "e"
  <digito> (32)
    "1"
```

```
compas_actual
```

```
<identificador> (26)
  <letra> (30)
    "c"
  <letra> (30)
    "o"
  <letra> (30)
    "m"
  <letra> (30)
    "p"
  <letra> (30)
    "a"
  <letra> (30)
    "s"
  "_"
  <letra> (30)
    "a"
  <letra> (30)
    "c"
  <letra> (30)
    "t"
  <letra> (30)
    "u"
  <letra> (30)
    "a"
  <letra> (30)
    "l"
```

## Ejemplo inválido

```
_frase
2voces
```

**Por qué no deriva:** No puede empezar por guion bajo ni por dígito: el primer símbolo es `<letra>`.

## Nota de diseño

Es la frontera entre las dos mitades del lenguaje: lo que empieza en minúscula es un nombre; las palabras en MAYÚSCULAS son las de las reglas. Sin la restricción del comentario la gramática sería ambigua: `true` podría derivarse como `<valor>` y también como `<identificador>` (`"t" "r" "u" "e"`), con dos árboles distintos para la misma cadena.

---
*Convención: `<x>` no terminal · `"x"` terminal · `'"'` la comilla doble como terminal · `{ }` cero o más · `[ ]` cero o uno · `|` alternativa · `<nl>` salto de línea*
