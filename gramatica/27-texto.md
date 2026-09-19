# Producción 27 · `<texto>`

**Nombres y valores** · Gramática BNF de TocaScript · Grupo 8

## La producción

La producción `<texto>` y, debajo, todas las que abre hasta llegar a los átomos —terminales entre comillas—. Todo en un mismo sitio, como en el tablero.

```
27  <texto> ::= '"' { <letra> | <mayuscula> | <digito> | " " | "/" } '"'

28  <letra> ::= "a" | "b" | "c" | "..." | "z"
29  <mayuscula> ::= "A" | "B" | "C" | "..." | "Z"
30  <digito> ::= "0" | "1" | "2" | "..." | "9"
```

## Cómo se lee

Una comilla doble, cero o más letras, mayúsculas, dígitos, espacios o barras, y otra comilla doble.

## Qué usa y quién la usa

| | |
|---|---|
| **Terminales que aparecen** (entre comillas) | `" "` · `"/"` · `'"'` |
| **No terminales que aparecen** (se abren en otra producción) | `<letra>` · `<mayuscula>` · `<digito>` |
| **Producciones que usan `<texto>`** | `<cabecera>` · `<pieza>` · `<valor>` |

## Ejemplo válido

```
"ff"
"4/4"
"Do mayor"
"Fray Santiago"
```

## Derivación del ejemplo hasta los átomos

Cada flecha aplica una producción; entre paréntesis, cuál. Al final solo quedan terminales entre comillas.

```
<texto>
→ '"' <digito> "/" <digito> '"'   (27: tres elementos de la repetición)
→ '"' "4" "/" "4" '"'   (30 digito)

Resultado:  "4/4"

Con mayúscula y espacio:
<texto>
→ '"' <mayuscula> <letra> " " <letra> <letra> <letra> <letra> <letra> '"'   (27)
→ '"' "D" "o" " " "m" "a" "y" "o" "r" '"'   (29 mayuscula · 28 letra)

Resultado:  "Do mayor"
```

## Ejemplo inválido

```
'ff'
"Do
mayor"
```

**Por qué no deriva:** Las comillas simples no delimitan texto. Y el salto de línea no está entre los caracteres permitidos.

## Nota de diseño

Aquí viven las comillas: la producción empieza y termina en `'"'`, así que todo `<texto>` las lleva a los dos lados. Las producciones que usan un texto —cabecera, pieza, valor— no las repiten: dicen `<texto>` y al derivar aparecen. La comilla doble como terminal se escribe `'"'`, entre comillas simples, porque las dobles ya marcan los demás terminales y `"""` sería ilegible. Se admiten `<mayuscula>`, el espacio y la barra porque los necesitan `"Do mayor"` y `"4/4"`.

---
*Convención: `<x>` no terminal · `"x"` terminal · `'"'` la comilla doble como terminal · `{ }` cero o más · `[ ]` cero o uno · `|` alternativa · `<nl>` salto de línea*
