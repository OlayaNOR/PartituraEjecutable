# Producción 3 · `<pieza>`

**Estructura del archivo** · Gramática BNF de TocaScript · Grupo 8

## La producción

La producción `<pieza>` y, debajo, todas las que abre hasta llegar a los átomos —terminales entre comillas—. Todo en un mismo sitio, como en el tablero.

```
 3  <pieza> ::= "pieza" <texto> "{" { <identificador> } "}" <nl>

27  <texto> ::= '"' { <letra> | <mayuscula> | <digito> | " " | "/" } '"'
28  <letra> ::= "a" | "b" | "c" | "..." | "z"
29  <mayuscula> ::= "A" | "B" | "C" | "..." | "Z"
30  <digito> ::= "0" | "1" | "2" | "..." | "9"
24  <identificador> ::= <letra> { <letra> | <digito> | "_" }
31  <nl> ::= "↵"
```

## Cómo se lee

La palabra `pieza`, un título entre comillas, y entre llaves la lista ordenada de nombres de sección. Termina en salto de línea.

## Qué usa y quién la usa

| | |
|---|---|
| **Terminales que aparecen** (entre comillas) | `"pieza"` · `"{"` · `"}"` |
| **No terminales que aparecen** (se abren en otra producción) | `<texto>` · `<identificador>` · `<nl>` |
| **Producciones que usan `<pieza>`** | `<programa>` |

## Ejemplo válido

```
pieza "Fray Santiago" { cancion cierre }
```

## Derivación del ejemplo hasta los átomos

Cada flecha aplica una producción; entre paréntesis, cuál. Al final solo quedan terminales entre comillas.

```
<pieza>
→ "pieza" <texto> "{" <identificador> <identificador> "}" <nl>   (3, dos identificadores)
→ "pieza" '"' <mayuscula> <letra> <letra> <letra> " " <mayuscula> <letra> … '"' "{" … "}" <nl>   (27 texto)
→ "pieza" '"' "F" "r" "a" "y" " " "S" "a" "n" "t" "i" "a" "g" "o" '"' "{" … "}" <nl>   (29, 28)
→ … "{" "c" "a" "n" "c" "i" "o" "n"  "c" "i" "e" "r" "r" "e" "}" <nl>   (24 identificador · 28 letra)

Resultado:  pieza "Fray Santiago" { cancion cierre } ↵
```

## Ejemplo inválido

```
pieza Fray Santiago { cancion cierre }
```

**Por qué no deriva:** El título tiene que ser un `<texto>`, con comillas. Sin ellas, `Fray` y `Santiago` serían identificadores — y además `Fray` empieza en mayúscula, que no es `<letra>`.

## Nota de diseño

Es el punto de entrada, el `main`. Que `cancion` y `cierre` existan como secciones lo comprueba el intérprete, no la gramática.

---
*Convención: `<x>` no terminal · `"x"` terminal · `'"'` la comilla doble como terminal · `{ }` cero o más · `[ ]` cero o uno · `|` alternativa · `<nl>` salto de línea*
