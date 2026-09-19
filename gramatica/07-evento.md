# Producción 7 · `<evento>`

**La música** · Gramática BNF de TocaScript · Grupo 8

## La producción

La producción `<evento>` y, debajo, todas las que abre hasta llegar a los átomos —terminales entre comillas—. Todo en un mismo sitio, como en el tablero.

```
 7  <evento> ::= <nota> ":" <figura> | "[" <nota> { <nota> } "]" ":" <figura> | "silencio" ":" <figura>

 8  <nota> ::= <nombre_nota> [ "#" | "b" ] <octava>
 9  <nombre_nota> ::= "do" | "re" | "mi" | "fa" | "sol" | "la" | "si"
10  <octava> ::= <digito>
30  <digito> ::= "0" | "1" | "2" | "..." | "9"
11  <figura> ::= <nombre_figura> [ "." ]
12  <nombre_figura> ::= "redonda" | "blanca" | "negra" | "corchea" | "semicorchea" | "fusa"
```

## Cómo se lee

Una nota con su figura; o varias notas entre corchetes —un acorde— con su figura; o la palabra `silencio` con su figura.

## Qué usa y quién la usa

| | |
|---|---|
| **Terminales que aparecen** (entre comillas) | `":"` · `"["` · `"]"` · `":"` · `"silencio"` · `":"` |
| **No terminales que aparecen** (se abren en otra producción) | `<nota>` · `<figura>` |
| **Producciones que usan `<evento>`** | `<motivo>` · `<seccion>` |

## Ejemplo válido

```
do4:negra
[do3 mi3 sol3 do4]:redonda
silencio:redonda
```

## Derivación del ejemplo hasta los átomos

Cada flecha aplica una producción; entre paréntesis, cuál. Al final solo quedan terminales entre comillas.

```
<evento>
→ <nota> ":" <figura>   (7, 1.ª alternativa)
→ <nombre_nota> <octava> ":" <figura>   (8 nota, sin alteración)
→ "do" <octava> ":" <figura>   (9 nombre_nota)
→ "do" <digito> ":" <figura>   (10 octava)
→ "do" "4" ":" <figura>   (30 digito)
→ "do" "4" ":" <nombre_figura>   (11 figura, sin puntillo)
→ "do" "4" ":" "negra"   (12 nombre_figura)

Resultado:  do4:negra
```

## Ejemplo inválido

```
do4
[do3 mi3]
```

**Por qué no deriva:** A los dos les falta `":" <figura>`. La figura es obligatoria: en música todo dura algo, incluso el silencio.

## Nota de diseño

Los corchetes van entre comillas porque son símbolos del lenguaje, no el «opcional» de la notación.

---
*Convención: `<x>` no terminal · `"x"` terminal · `'"'` la comilla doble como terminal · `{ }` cero o más · `[ ]` cero o uno · `|` alternativa · `<nl>` salto de línea*
