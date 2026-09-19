# Producción 4 · `<motivo>`

**Estructura del archivo** · Gramática BNF de TocaScript · Grupo 8

## La producción

La producción `<motivo>` y, debajo, todas las que abre hasta llegar a los átomos —terminales entre comillas—. Todo en un mismo sitio, como en el tablero.

```
 4  <motivo> ::= "motivo" <identificador> "{" { <evento> } "}" <nl>

24  <identificador> ::= <letra> { <letra> | <digito> | "_" }
28  <letra> ::= "a" | "b" | "c" | "..." | "z"
30  <digito> ::= "0" | "1" | "2" | "..." | "9"
 7  <evento> ::= <nota> ":" <figura> | "[" <nota> { <nota> } "]" ":" <figura> | "silencio" ":" <figura>
 8  <nota> ::= <nombre_nota> [ "#" | "b" ] <octava>
 9  <nombre_nota> ::= "do" | "re" | "mi" | "fa" | "sol" | "la" | "si"
10  <octava> ::= <digito>
11  <figura> ::= <nombre_figura> [ "." ]
12  <nombre_figura> ::= "redonda" | "blanca" | "negra" | "corchea" | "semicorchea" | "fusa"
31  <nl> ::= "↵"
```

## Cómo se lee

La palabra `motivo`, un nombre, y entre llaves cero o más eventos. Termina en salto de línea.

## Qué usa y quién la usa

| | |
|---|---|
| **Terminales que aparecen** (entre comillas) | `"motivo"` · `"{"` · `"}"` |
| **No terminales que aparecen** (se abren en otra producción) | `<identificador>` · `<evento>` · `<nl>` |
| **Producciones que usan `<motivo>`** | `<programa>` |

## Ejemplo válido

```
motivo frase1 { do4:negra re4:negra mi4:negra do4:negra }
```

## Derivación del ejemplo hasta los átomos

Cada flecha aplica una producción; entre paréntesis, cuál. Al final solo quedan terminales entre comillas.

```
<motivo>
→ "motivo" <identificador> "{" <evento> <evento> "}" <nl>   (4, dos eventos)
→ "motivo" <letra> <letra> <letra> <letra> <letra> <digito> "{" … "}" <nl>   (24 identificador)
→ "motivo" "f" "r" "a" "s" "e" "1" "{" … "}" <nl>   (28 letra · 30 digito)
→ … "{" <nota> ":" <figura>  <nota> ":" <figura> "}" <nl>   (7 evento ×2)
→ … "{" "do" "4" ":" "negra"  "re" "4" ":" "negra" "}" <nl>   (8–12, como en <evento>)

Resultado:  motivo frase1 { do4:negra re4:negra } ↵
```

## Ejemplo inválido

```
motivo frase1 do4:negra re4:negra
```

**Por qué no deriva:** Faltan las llaves `"{"` y `"}"`.

## Nota de diseño

Dentro de las llaves los saltos de línea cuentan como espacio; el `<nl>` obligatorio es el que va tras la llave de cierre.

---
*Convención: `<x>` no terminal · `"x"` terminal · `'"'` la comilla doble como terminal · `{ }` cero o más · `[ ]` cero o uno · `|` alternativa · `<nl>` salto de línea*
