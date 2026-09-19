# Verificación regla por regla

**TocaScript · Grupo 8** · Las 15 reglas de `reglas.txt`, derivadas una a una con la gramática de `gramatica.md`.

Lo que se comprueba, para cada regla: que **cada palabra corresponda a un terminal o a un no terminal ya definido**, y que la gramática la **genere** — es decir, que exista un árbol de derivación desde `<regla>` cuyas hojas, leídas de izquierda a derecha, sean exactamente la regla. La derivación la produce un parser (`verificar.py`) que implementa las 33 producciones al pie de la letra: si el parser acepta la regla, la gramática la genera.

## Resultado

| | |
|---|---|
| Reglas en `reglas.txt` | 15 |
| Reglas que la gramática genera | **15 de 15** |

## Lo que la verificación destapó

La primera pasada **falló en 5 de las 15**: R1, R2, R8, R11 y R15. Todas usan `tempo` o `compas` como variable —`AL tempo > 140`, `AL compas = "3/4"`, `TOCAR tempo = tempo - 10`—, y la cabecera las tenía declaradas como **palabras clave**: `<cabecera> ::= "tempo" <numero> …`. Una palabra no puede ser terminal y variable a la vez: el lexer tiene que decidir, y con `"tempo"` como palabra clave, `<variable>` no podía derivarlo.

Siguiendo la instrucción —*si una regla no está cubierta, se ajusta la gramática, no la regla*— se cambió la cabecera a una lista de ajustes de variable:

```
 2  <cabecera> ::= <ajuste> <nl> <ajuste> <nl> <ajuste> <nl>
 3  <ajuste>   ::= <variable> <valor>
```

Con eso `tempo`, `compas` y `tonalidad` son lo que siempre fueron en el diseño: **variables** que la cabecera fija y las reglas consultan. Segunda pasada: 15 de 15.

## Las 15 reglas, una a una

Para cada regla: los tokens que produce el lexer con la categoría de cada uno, y el árbol de derivación.

### R1

```
AL tempo > 140 TOCAR dinamica = "ff"
```

| Token | Terminal o no terminal |
|---|---|
| `AL` | terminal `"AL"` |
| `tempo` | `<identificador>` (26) → `<letra>` … (30) |
| `>` | terminal `">"` · `<operador>` (19) |
| `140` | `<numero>` (28) → `<digito>` … (32) |
| `TOCAR` | terminal `"TOCAR"` |
| `dinamica` | `<identificador>` (26) → `<letra>` … (30) |
| `=` | terminal `"="` (comparación en `<condicion>`, asignación en `<accion>`) |
| `"ff"` | `<texto>` (29) → `'"'` … `'"'` |
| `↵` | terminal `"↵"` · `<nl>` (33) |

Árbol de derivación — 44 nodos no terminales, 25 hojas terminales:

```
<regla> (14)
  "AL"
  <expresion> (15)
    <termino> (16)
      <factor> (17)
        <condicion> (18)
          <operando> (20)
            <sumando> (21)
              <primario> (22)
                <variable> (25)
                  <identificador> (26)  → "t" "e" "m" "p" "o"
          <operador> (19)
            ">"
          <operando> (20)
            <sumando> (21)
              <primario> (22)
                <valor> (27)
                  <numero> (28)  → "1" "4" "0"
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
              <texto> (29)  → '"' "f" "f" '"'
  <nl> (33)  → "↵"
```

### R2

```
AL compas = "3/4" TOCAR acentuar_primer_tiempo
```

| Token | Terminal o no terminal |
|---|---|
| `AL` | terminal `"AL"` |
| `compas` | `<identificador>` (26) → `<letra>` … (30) |
| `=` | terminal `"="` (comparación en `<condicion>`, asignación en `<accion>`) |
| `"3/4"` | `<texto>` (29) → `'"'` … `'"'` |
| `TOCAR` | terminal `"TOCAR"` |
| `acentuar_primer_tiempo` | `<identificador>` (26) → `<letra>` … (30) |
| `↵` | terminal `"↵"` · `<nl>` (33) |

Árbol de derivación — 48 nodos no terminales, 37 hojas terminales:

```
<regla> (14)
  "AL"
  <expresion> (15)
    <termino> (16)
      <factor> (17)
        <condicion> (18)
          <operando> (20)
            <sumando> (21)
              <primario> (22)
                <variable> (25)
                  <identificador> (26)  → "c" "o" "m" "p" "a" "s"
          <operador> (19)
            "="
          <operando> (20)
            <sumando> (21)
              <primario> (22)
                <valor> (27)
                  <texto> (29)  → '"' "3" "/" "4" '"'
  "TOCAR"
  <acciones> (23)
    <accion> (24)
      <identificador> (26)  → "a" "c" "e" "n" "t" "u" "a" "r" "_" "p" "r" "i" "m" "e" "r" "_" "t" "i" "e" "m" "p" "o"
  <nl> (33)  → "↵"
```

### R3

```
AL es_coda TOCAR dinamica = "pp"
```

| Token | Terminal o no terminal |
|---|---|
| `AL` | terminal `"AL"` |
| `es_coda` | `<identificador>` (26) → `<letra>` … (30) |
| `TOCAR` | terminal `"TOCAR"` |
| `dinamica` | `<identificador>` (26) → `<letra>` … (30) |
| `=` | terminal `"="` (comparación en `<condicion>`, asignación en `<accion>`) |
| `"pp"` | `<texto>` (29) → `'"'` … `'"'` |
| `↵` | terminal `"↵"` · `<nl>` (33) |

Árbol de derivación — 32 nodos no terminales, 23 hojas terminales:

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

### R4

```
AL es_intro TOCAR dinamica = "p"
```

| Token | Terminal o no terminal |
|---|---|
| `AL` | terminal `"AL"` |
| `es_intro` | `<identificador>` (26) → `<letra>` … (30) |
| `TOCAR` | terminal `"TOCAR"` |
| `dinamica` | `<identificador>` (26) → `<letra>` … (30) |
| `=` | terminal `"="` (comparación en `<condicion>`, asignación en `<accion>`) |
| `"p"` | `<texto>` (29) → `'"'` … `'"'` |
| `↵` | terminal `"↵"` · `<nl>` (33) |

Árbol de derivación — 32 nodos no terminales, 23 hojas terminales:

```
<regla> (14)
  "AL"
  <expresion> (15)
    <termino> (16)
      <factor> (17)
        <variable> (25)
          <identificador> (26)  → "e" "s" "_" "i" "n" "t" "r" "o"
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
              <texto> (29)  → '"' "p" '"'
  <nl> (33)  → "↵"
```

### R5

```
AL num_voces > 3 TOCAR articulacion = "staccato"
```

| Token | Terminal o no terminal |
|---|---|
| `AL` | terminal `"AL"` |
| `num_voces` | `<identificador>` (26) → `<letra>` … (30) |
| `>` | terminal `">"` · `<operador>` (19) |
| `3` | `<numero>` (28) → `<digito>` … (32) |
| `TOCAR` | terminal `"TOCAR"` |
| `articulacion` | `<identificador>` (26) → `<letra>` … (30) |
| `=` | terminal `"="` (comparación en `<condicion>`, asignación en `<accion>`) |
| `"staccato"` | `<texto>` (29) → `'"'` … `'"'` |
| `↵` | terminal `"↵"` · `<nl>` (33) |

Árbol de derivación — 55 nodos no terminales, 37 hojas terminales:

```
<regla> (14)
  "AL"
  <expresion> (15)
    <termino> (16)
      <factor> (17)
        <condicion> (18)
          <operando> (20)
            <sumando> (21)
              <primario> (22)
                <variable> (25)
                  <identificador> (26)  → "n" "u" "m" "_" "v" "o" "c" "e" "s"
          <operador> (19)
            ">"
          <operando> (20)
            <sumando> (21)
              <primario> (22)
                <valor> (27)
                  <numero> (28)  → "3"
  "TOCAR"
  <acciones> (23)
    <accion> (24)
      <variable> (25)
        <identificador> (26)  → "a" "r" "t" "i" "c" "u" "l" "a" "c" "i" "o" "n"
      "="
      <operando> (20)
        <sumando> (21)
          <primario> (22)
            <valor> (27)
              <texto> (29)  → '"' "s" "t" "a" "c" "c" "a" "t" "o" '"'
  <nl> (33)  → "↵"
```

### R6

```
AL es_estribillo Y intensidad > 0.7 TOCAR activar_percusion
```

| Token | Terminal o no terminal |
|---|---|
| `AL` | terminal `"AL"` |
| `es_estribillo` | `<identificador>` (26) → `<letra>` … (30) |
| `Y` | terminal `"Y"` |
| `intensidad` | `<identificador>` (26) → `<letra>` … (30) |
| `>` | terminal `">"` · `<operador>` (19) |
| `0.7` | `<numero>` (28) → `<digito>` … (32) |
| `TOCAR` | terminal `"TOCAR"` |
| `activar_percusion` | `<identificador>` (26) → `<letra>` … (30) |
| `↵` | terminal `"↵"` · `<nl>` (33) |

Árbol de derivación — 63 nodos no terminales, 48 hojas terminales:

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

### R7

```
AL compas_actual > 24 O es_coda TOCAR aplicar_crescendo
```

| Token | Terminal o no terminal |
|---|---|
| `AL` | terminal `"AL"` |
| `compas_actual` | `<identificador>` (26) → `<letra>` … (30) |
| `>` | terminal `">"` · `<operador>` (19) |
| `24` | `<numero>` (28) → `<digito>` … (32) |
| `O` | terminal `"O"` |
| `es_coda` | `<identificador>` (26) → `<letra>` … (30) |
| `TOCAR` | terminal `"TOCAR"` |
| `aplicar_crescendo` | `<identificador>` (26) → `<letra>` … (30) |
| `↵` | terminal `"↵"` · `<nl>` (33) |

Árbol de derivación — 60 nodos no terminales, 44 hojas terminales:

```
<regla> (14)
  "AL"
  <expresion> (15)
    <termino> (16)
      <factor> (17)
        <condicion> (18)
          <operando> (20)
            <sumando> (21)
              <primario> (22)
                <variable> (25)
                  <identificador> (26)  → "c" "o" "m" "p" "a" "s" "_" "a" "c" "t" "u" "a" "l"
          <operador> (19)
            ">"
          <operando> (20)
            <sumando> (21)
              <primario> (22)
                <valor> (27)
                  <numero> (28)  → "2" "4"
    "O"
    <termino> (16)
      <factor> (17)
        <variable> (25)
          <identificador> (26)  → "e" "s" "_" "c" "o" "d" "a"
  "TOCAR"
  <acciones> (23)
    <accion> (24)
      <identificador> (26)  → "a" "p" "l" "i" "c" "a" "r" "_" "c" "r" "e" "s" "c" "e" "n" "d" "o"
  <nl> (33)  → "↵"
```

### R8

```
AL tempo < 80 Y NO hay_repeticion TOCAR articulacion = "legato"
```

| Token | Terminal o no terminal |
|---|---|
| `AL` | terminal `"AL"` |
| `tempo` | `<identificador>` (26) → `<letra>` … (30) |
| `<` | terminal `"<"` · `<operador>` (19) |
| `80` | `<numero>` (28) → `<digito>` … (32) |
| `Y` | terminal `"Y"` |
| `NO` | terminal `"NO"` |
| `hay_repeticion` | `<identificador>` (26) → `<letra>` … (30) |
| `TOCAR` | terminal `"TOCAR"` |
| `articulacion` | `<identificador>` (26) → `<letra>` … (30) |
| `=` | terminal `"="` (comparación en `<condicion>`, asignación en `<accion>`) |
| `"legato"` | `<texto>` (29) → `'"'` … `'"'` |
| `↵` | terminal `"↵"` · `<nl>` (33) |

Árbol de derivación — 68 nodos no terminales, 48 hojas terminales:

```
<regla> (14)
  "AL"
  <expresion> (15)
    <termino> (16)
      <factor> (17)
        <condicion> (18)
          <operando> (20)
            <sumando> (21)
              <primario> (22)
                <variable> (25)
                  <identificador> (26)  → "t" "e" "m" "p" "o"
          <operador> (19)
            "<"
          <operando> (20)
            <sumando> (21)
              <primario> (22)
                <valor> (27)
                  <numero> (28)  → "8" "0"
      "Y"
      <factor> (17)
        "NO"
        <factor> (17)
          <variable> (25)
            <identificador> (26)  → "h" "a" "y" "_" "r" "e" "p" "e" "t" "i" "c" "i" "o" "n"
  "TOCAR"
  <acciones> (23)
    <accion> (24)
      <variable> (25)
        <identificador> (26)  → "a" "r" "t" "i" "c" "u" "l" "a" "c" "i" "o" "n"
      "="
      <operando> (20)
        <sumando> (21)
          <primario> (22)
            <valor> (27)
              <texto> (29)  → '"' "l" "e" "g" "a" "t" "o" '"'
  <nl> (33)  → "↵"
```

### R9

```
AL es_estrofa O hay_repeticion TOCAR dinamica = "mp"
```

| Token | Terminal o no terminal |
|---|---|
| `AL` | terminal `"AL"` |
| `es_estrofa` | `<identificador>` (26) → `<letra>` … (30) |
| `O` | terminal `"O"` |
| `hay_repeticion` | `<identificador>` (26) → `<letra>` … (30) |
| `TOCAR` | terminal `"TOCAR"` |
| `dinamica` | `<identificador>` (26) → `<letra>` … (30) |
| `=` | terminal `"="` (comparación en `<condicion>`, asignación en `<accion>`) |
| `"mp"` | `<texto>` (29) → `'"'` … `'"'` |
| `↵` | terminal `"↵"` · `<nl>` (33) |

Árbol de derivación — 52 nodos no terminales, 41 hojas terminales:

```
<regla> (14)
  "AL"
  <expresion> (15)
    <termino> (16)
      <factor> (17)
        <variable> (25)
          <identificador> (26)  → "e" "s" "_" "e" "s" "t" "r" "o" "f" "a"
    "O"
    <termino> (16)
      <factor> (17)
        <variable> (25)
          <identificador> (26)  → "h" "a" "y" "_" "r" "e" "p" "e" "t" "i" "c" "i" "o" "n"
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
              <texto> (29)  → '"' "m" "p" '"'
  <nl> (33)  → "↵"
```

### R10

```
AL hay_repeticion Y repeticion_actual = 2 TOCAR subir_una_octava
```

| Token | Terminal o no terminal |
|---|---|
| `AL` | terminal `"AL"` |
| `hay_repeticion` | `<identificador>` (26) → `<letra>` … (30) |
| `Y` | terminal `"Y"` |
| `repeticion_actual` | `<identificador>` (26) → `<letra>` … (30) |
| `=` | terminal `"="` (comparación en `<condicion>`, asignación en `<accion>`) |
| `2` | `<numero>` (28) → `<digito>` … (32) |
| `TOCAR` | terminal `"TOCAR"` |
| `subir_una_octava` | `<identificador>` (26) → `<letra>` … (30) |
| `↵` | terminal `"↵"` · `<nl>` (33) |

Árbol de derivación — 67 nodos no terminales, 53 hojas terminales:

```
<regla> (14)
  "AL"
  <expresion> (15)
    <termino> (16)
      <factor> (17)
        <variable> (25)
          <identificador> (26)  → "h" "a" "y" "_" "r" "e" "p" "e" "t" "i" "c" "i" "o" "n"
      "Y"
      <factor> (17)
        <condicion> (18)
          <operando> (20)
            <sumando> (21)
              <primario> (22)
                <variable> (25)
                  <identificador> (26)  → "r" "e" "p" "e" "t" "i" "c" "i" "o" "n" "_" "a" "c" "t" "u" "a" "l"
          <operador> (19)
            "="
          <operando> (20)
            <sumando> (21)
              <primario> (22)
                <valor> (27)
                  <numero> (28)  → "2"
  "TOCAR"
  <acciones> (23)
    <accion> (24)
      <identificador> (26)  → "s" "u" "b" "i" "r" "_" "u" "n" "a" "_" "o" "c" "t" "a" "v" "a"
  <nl> (33)  → "↵"
```

### R11

```
AL (es_coda O es_final) Y NO tiene_percusion TOCAR tempo = tempo - 10
```

| Token | Terminal o no terminal |
|---|---|
| `AL` | terminal `"AL"` |
| `(` | terminal `"("` |
| `es_coda` | `<identificador>` (26) → `<letra>` … (30) |
| `O` | terminal `"O"` |
| `es_final` | `<identificador>` (26) → `<letra>` … (30) |
| `)` | terminal `")"` |
| `Y` | terminal `"Y"` |
| `NO` | terminal `"NO"` |
| `tiene_percusion` | `<identificador>` (26) → `<letra>` … (30) |
| `TOCAR` | terminal `"TOCAR"` |
| `tempo` | `<identificador>` (26) → `<letra>` … (30) |
| `=` | terminal `"="` (comparación en `<condicion>`, asignación en `<accion>`) |
| `tempo` | `<identificador>` (26) → `<letra>` … (30) |
| `-` | terminal `"-"` · `<operando>` (20) |
| `10` | `<numero>` (28) → `<digito>` … (32) |
| `↵` | terminal `"↵"` · `<nl>` (33) |

Árbol de derivación — 70 nodos no terminales, 52 hojas terminales:

```
<regla> (14)
  "AL"
  <expresion> (15)
    <termino> (16)
      <factor> (17)
        "("
        <expresion> (15)
          <termino> (16)
            <factor> (17)
              <variable> (25)
                <identificador> (26)  → "e" "s" "_" "c" "o" "d" "a"
          "O"
          <termino> (16)
            <factor> (17)
              <variable> (25)
                <identificador> (26)  → "e" "s" "_" "f" "i" "n" "a" "l"
        ")"
      "Y"
      <factor> (17)
        "NO"
        <factor> (17)
          <variable> (25)
            <identificador> (26)  → "t" "i" "e" "n" "e" "_" "p" "e" "r" "c" "u" "s" "i" "o" "n"
  "TOCAR"
  <acciones> (23)
    <accion> (24)
      <variable> (25)
        <identificador> (26)  → "t" "e" "m" "p" "o"
      "="
      <operando> (20)
        <sumando> (21)
          <primario> (22)
            <variable> (25)
              <identificador> (26)  → "t" "e" "m" "p" "o"
        "-"
        <sumando> (21)
          <primario> (22)
            <valor> (27)
              <numero> (28)  → "1" "0"
  <nl> (33)  → "↵"
```

### R12

```
AL intensidad >= 0.9 Y es_estribillo TOCAR dinamica = "fff" Y duplicar_octava
```

| Token | Terminal o no terminal |
|---|---|
| `AL` | terminal `"AL"` |
| `intensidad` | `<identificador>` (26) → `<letra>` … (30) |
| `>=` | terminal `">="` · `<operador>` (19) |
| `0.9` | `<numero>` (28) → `<digito>` … (32) |
| `Y` | terminal `"Y"` |
| `es_estribillo` | `<identificador>` (26) → `<letra>` … (30) |
| `TOCAR` | terminal `"TOCAR"` |
| `dinamica` | `<identificador>` (26) → `<letra>` … (30) |
| `=` | terminal `"="` (comparación en `<condicion>`, asignación en `<accion>`) |
| `"fff"` | `<texto>` (29) → `'"'` … `'"'` |
| `Y` | terminal `"Y"` |
| `duplicar_octava` | `<identificador>` (26) → `<letra>` … (30) |
| `↵` | terminal `"↵"` · `<nl>` (33) |

Árbol de derivación — 80 nodos no terminales, 61 hojas terminales:

```
<regla> (14)
  "AL"
  <expresion> (15)
    <termino> (16)
      <factor> (17)
        <condicion> (18)
          <operando> (20)
            <sumando> (21)
              <primario> (22)
                <variable> (25)
                  <identificador> (26)  → "i" "n" "t" "e" "n" "s" "i" "d" "a" "d"
          <operador> (19)
            ">="
          <operando> (20)
            <sumando> (21)
              <primario> (22)
                <valor> (27)
                  <numero> (28)  → "0" "." "9"
      "Y"
      <factor> (17)
        <variable> (25)
          <identificador> (26)  → "e" "s" "_" "e" "s" "t" "r" "i" "b" "i" "l" "l" "o"
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
              <texto> (29)  → '"' "f" "f" "f" '"'
    "Y"
    <accion> (24)
      <identificador> (26)  → "d" "u" "p" "l" "i" "c" "a" "r" "_" "o" "c" "t" "a" "v" "a"
  <nl> (33)  → "↵"
```

### R13

```
AL nota_actual > 91 Y NO permitir_agudos TOCAR bajar_una_octava
```

| Token | Terminal o no terminal |
|---|---|
| `AL` | terminal `"AL"` |
| `nota_actual` | `<identificador>` (26) → `<letra>` … (30) |
| `>` | terminal `">"` · `<operador>` (19) |
| `91` | `<numero>` (28) → `<digito>` … (32) |
| `Y` | terminal `"Y"` |
| `NO` | terminal `"NO"` |
| `permitir_agudos` | `<identificador>` (26) → `<letra>` … (30) |
| `TOCAR` | terminal `"TOCAR"` |
| `bajar_una_octava` | `<identificador>` (26) → `<letra>` … (30) |
| `↵` | terminal `"↵"` · `<nl>` (33) |

Árbol de derivación — 64 nodos no terminales, 50 hojas terminales:

```
<regla> (14)
  "AL"
  <expresion> (15)
    <termino> (16)
      <factor> (17)
        <condicion> (18)
          <operando> (20)
            <sumando> (21)
              <primario> (22)
                <variable> (25)
                  <identificador> (26)  → "n" "o" "t" "a" "_" "a" "c" "t" "u" "a" "l"
          <operador> (19)
            ">"
          <operando> (20)
            <sumando> (21)
              <primario> (22)
                <valor> (27)
                  <numero> (28)  → "9" "1"
      "Y"
      <factor> (17)
        "NO"
        <factor> (17)
          <variable> (25)
            <identificador> (26)  → "p" "e" "r" "m" "i" "t" "i" "r" "_" "a" "g" "u" "d" "o" "s"
  "TOCAR"
  <acciones> (23)
    <accion> (24)
      <identificador> (26)  → "b" "a" "j" "a" "r" "_" "u" "n" "a" "_" "o" "c" "t" "a" "v" "a"
  <nl> (33)  → "↵"
```

### R14

```
AL num_voces >= 4 Y tiene_percusion TOCAR volumen = volumen - 15
```

| Token | Terminal o no terminal |
|---|---|
| `AL` | terminal `"AL"` |
| `num_voces` | `<identificador>` (26) → `<letra>` … (30) |
| `>=` | terminal `">="` · `<operador>` (19) |
| `4` | `<numero>` (28) → `<digito>` … (32) |
| `Y` | terminal `"Y"` |
| `tiene_percusion` | `<identificador>` (26) → `<letra>` … (30) |
| `TOCAR` | terminal `"TOCAR"` |
| `volumen` | `<identificador>` (26) → `<letra>` … (30) |
| `=` | terminal `"="` (comparación en `<condicion>`, asignación en `<accion>`) |
| `volumen` | `<identificador>` (26) → `<letra>` … (30) |
| `-` | terminal `"-"` · `<operando>` (20) |
| `15` | `<numero>` (28) → `<digito>` … (32) |
| `↵` | terminal `"↵"` · `<nl>` (33) |

Árbol de derivación — 72 nodos no terminales, 48 hojas terminales:

```
<regla> (14)
  "AL"
  <expresion> (15)
    <termino> (16)
      <factor> (17)
        <condicion> (18)
          <operando> (20)
            <sumando> (21)
              <primario> (22)
                <variable> (25)
                  <identificador> (26)  → "n" "u" "m" "_" "v" "o" "c" "e" "s"
          <operador> (19)
            ">="
          <operando> (20)
            <sumando> (21)
              <primario> (22)
                <valor> (27)
                  <numero> (28)  → "4"
      "Y"
      <factor> (17)
        <variable> (25)
          <identificador> (26)  → "t" "i" "e" "n" "e" "_" "p" "e" "r" "c" "u" "s" "i" "o" "n"
  "TOCAR"
  <acciones> (23)
    <accion> (24)
      <variable> (25)
        <identificador> (26)  → "v" "o" "l" "u" "m" "e" "n"
      "="
      <operando> (20)
        <sumando> (21)
          <primario> (22)
            <variable> (25)
              <identificador> (26)  → "v" "o" "l" "u" "m" "e" "n"
        "-"
        <sumando> (21)
          <primario> (22)
            <valor> (27)
              <numero> (28)  → "1" "5"
  <nl> (33)  → "↵"
```

### R15

```
AL compas_actual >= duracion_total - 2 Y es_final TOCAR tempo = tempo * 0.85
```

| Token | Terminal o no terminal |
|---|---|
| `AL` | terminal `"AL"` |
| `compas_actual` | `<identificador>` (26) → `<letra>` … (30) |
| `>=` | terminal `">="` · `<operador>` (19) |
| `duracion_total` | `<identificador>` (26) → `<letra>` … (30) |
| `-` | terminal `"-"` · `<operando>` (20) |
| `2` | `<numero>` (28) → `<digito>` … (32) |
| `Y` | terminal `"Y"` |
| `es_final` | `<identificador>` (26) → `<letra>` … (30) |
| `TOCAR` | terminal `"TOCAR"` |
| `tempo` | `<identificador>` (26) → `<letra>` … (30) |
| `=` | terminal `"="` (comparación en `<condicion>`, asignación en `<accion>`) |
| `tempo` | `<identificador>` (26) → `<letra>` … (30) |
| `*` | terminal `"*"` · `<sumando>` (21) |
| `0.85` | `<numero>` (28) → `<digito>` … (32) |
| `↵` | terminal `"↵"` · `<nl>` (33) |

Árbol de derivación — 82 nodos no terminales, 58 hojas terminales:

```
<regla> (14)
  "AL"
  <expresion> (15)
    <termino> (16)
      <factor> (17)
        <condicion> (18)
          <operando> (20)
            <sumando> (21)
              <primario> (22)
                <variable> (25)
                  <identificador> (26)  → "c" "o" "m" "p" "a" "s" "_" "a" "c" "t" "u" "a" "l"
          <operador> (19)
            ">="
          <operando> (20)
            <sumando> (21)
              <primario> (22)
                <variable> (25)
                  <identificador> (26)  → "d" "u" "r" "a" "c" "i" "o" "n" "_" "t" "o" "t" "a" "l"
            "-"
            <sumando> (21)
              <primario> (22)
                <valor> (27)
                  <numero> (28)  → "2"
      "Y"
      <factor> (17)
        <variable> (25)
          <identificador> (26)  → "e" "s" "_" "f" "i" "n" "a" "l"
  "TOCAR"
  <acciones> (23)
    <accion> (24)
      <variable> (25)
        <identificador> (26)  → "t" "e" "m" "p" "o"
      "="
      <operando> (20)
        <sumando> (21)
          <primario> (22)
            <variable> (25)
              <identificador> (26)  → "t" "e" "m" "p" "o"
          "*"
          <primario> (22)
            <valor> (27)
              <numero> (28)  → "0" "." "8" "5"
  <nl> (33)  → "↵"
```

## Cobertura

Las 15 reglas usan, entre todas, estas construcciones de la gramática: condición simple, variable booleana sola, `Y`, `O`, `NO`, paréntesis, los seis operadores relacionales, aritmética en el operando (`-`, `*`), asignación como acción, acción por identificador, y acciones múltiples con `Y`. Ninguna regla necesitó una construcción que la gramática no tuviera **después** del ajuste de la cabecera.
