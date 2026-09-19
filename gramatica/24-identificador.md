# Producción 24 · `<identificador>`

**Nombres y valores** · Gramática BNF de TocaScript · Grupo 8

## La producción

La producción `<identificador>` y, debajo, todas las que abre hasta llegar a los átomos —terminales entre comillas—. Todo en un mismo sitio, como en el tablero.

```
24  <identificador> ::= <letra> { <letra> | <digito> | "_" }

28  <letra> ::= "a" | "b" | "c" | "..." | "z"
30  <digito> ::= "0" | "1" | "2" | "..." | "9"
```

## Cómo se lee

Una letra minúscula, seguida de cero o más letras, dígitos o guiones bajos.

## Qué usa y quién la usa

| | |
|---|---|
| **Terminales que aparecen** (entre comillas) | `"_"` |
| **No terminales que aparecen** (se abren en otra producción) | `<letra>` · `<digito>` |
| **Producciones que usan `<identificador>`** | `<pieza>` · `<motivo>` · `<seccion>` · `<accion>` · `<variable>` |

## Ejemplo válido

```
frase1
compas_actual
```

## Derivación del ejemplo hasta los átomos

Cada flecha aplica una producción; entre paréntesis, cuál. Al final solo quedan terminales entre comillas.

```
<identificador>
→ <letra> <letra> <letra> <letra> <letra> <letra> "_" <letra> <letra> <letra> <letra> <letra> <letra>   (24)
→ "c" "o" "m" "p" "a" "s" "_" "a" "c" "t" "u" "a" "l"   (28 letra)

Resultado:  compas_actual
```

## Ejemplo inválido

```
_frase
2voces
```

**Por qué no deriva:** No puede empezar por guion bajo ni por dígito: el primer símbolo es `<letra>`.

## Nota de diseño

Es la frontera entre las dos mitades del lenguaje: lo que empieza en minúscula es un nombre; las palabras en MAYÚSCULAS son las de las reglas.

---
*Convención: `<x>` no terminal · `"x"` terminal · `'"'` la comilla doble como terminal · `{ }` cero o más · `[ ]` cero o uno · `|` alternativa · `<nl>` salto de línea*
