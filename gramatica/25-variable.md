# Producción 25 · `<variable>`

**Nombres y valores** · Gramática BNF de TocaScript · Grupo 8

## La producción

La producción `<variable>` y, debajo, todas las que abre hasta llegar a los átomos —terminales entre comillas—. Todo en un mismo sitio, como en el tablero.

```
25  <variable> ::= <identificador>

26  <identificador> ::= <letra> { <letra> | <digito> | "_" }
                        # y no puede coincidir con ninguna palabra reservada
30  <letra> ::= "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m"
              | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z"
32  <digito> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
```

## Cómo se lee

Una variable se escribe como un identificador.

## Qué usa y quién la usa

| | |
|---|---|
| **Terminales que aparecen** (entre comillas) | — |
| **No terminales que aparecen** (se abren en otra producción) | `<identificador>` |
| **Producciones que usan `<variable>`** | `<ajuste>` · `<factor>` · `<primario>` · `<accion>` |

## Ejemplo válido y su derivación

Cada ejemplo, y debajo el árbol que la gramática construye para él: cada nodo es una producción (con su número) y las hojas son terminales entre comillas. Derivación producida por el parser (`verificar.py`) que implementa estas 33 producciones; en `<identificador>`, `<numero>`, `<texto>` y `<nota>` se muestran directamente las hojas — cada carácter viene de `<letra>`, `<mayuscula>` o `<digito>`.

```
compas_actual
```

```
<variable> (25)
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

```
tiene_percusion
```

```
<variable> (25)
  <identificador> (26)
    <letra> (30)
      "t"
    <letra> (30)
      "i"
    <letra> (30)
      "e"
    <letra> (30)
      "n"
    <letra> (30)
      "e"
    "_"
    <letra> (30)
      "p"
    <letra> (30)
      "e"
    <letra> (30)
      "r"
    <letra> (30)
      "c"
    <letra> (30)
      "u"
    <letra> (30)
      "s"
    <letra> (30)
      "i"
    <letra> (30)
      "o"
    <letra> (30)
      "n"
```

```
tempo
```

```
<variable> (25)
  <identificador> (26)
    <letra> (30)
      "t"
    <letra> (30)
      "e"
    <letra> (30)
      "m"
    <letra> (30)
      "p"
    <letra> (30)
      "o"
```

## Ejemplo inválido

```
Tempo
```

**Por qué no deriva:** Empieza en mayúscula, y `<identificador>` empieza por `<letra>`, que solo tiene minúsculas.

## Nota de diseño

El conjunto de variables es cerrado: son las 20 de la tabla, entre ellas `tempo`, `compas` y `tonalidad`, que la cabecera fija y las reglas consultan. Sintácticamente cualquier identificador deriva; que exista lo comprueba el intérprete.

---
*Convención: `<x>` no terminal · `"x"` terminal · `'"'` la comilla doble como terminal · `{ }` cero o más · `[ ]` cero o uno · `|` alternativa · `<nl>` salto de línea*
