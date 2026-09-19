# Producción 5 · `<seccion>`

**Estructura del archivo** · Gramática BNF de TocaScript · Grupo 8

## La producción

La producción `<seccion>` y, debajo, todas las que abre hasta llegar a los átomos —terminales entre comillas—. Todo en un mismo sitio, como en el tablero.

```
 5  <seccion> ::= "seccion" <identificador> "tipo" <tipo_seccion>
                  "{" { <evento> | <identificador> } "}" <nl>

24  <identificador> ::= <letra> { <letra> | <digito> | "_" }
28  <letra> ::= "a" | "b" | "c" | "..." | "z"
30  <digito> ::= "0" | "1" | "2" | "..." | "9"
 6  <tipo_seccion> ::= "intro" | "estrofa" | "estribillo" | "coda"
 7  <evento> ::= <nota> ":" <figura> | "[" <nota> { <nota> } "]" ":" <figura> | "silencio" ":" <figura>
 8  <nota> ::= <nombre_nota> [ "#" | "b" ] <octava>
 9  <nombre_nota> ::= "do" | "re" | "mi" | "fa" | "sol" | "la" | "si"
10  <octava> ::= <digito>
11  <figura> ::= <nombre_figura> [ "." ]
12  <nombre_figura> ::= "redonda" | "blanca" | "negra" | "corchea" | "semicorchea" | "fusa"
31  <nl> ::= "↵"
```

## Cómo se lee

La palabra `seccion`, un nombre, la palabra `tipo`, el tipo de sección, y entre llaves eventos o nombres de motivos. Termina en salto de línea.

## Qué usa y quién la usa

| | |
|---|---|
| **Terminales que aparecen** (entre comillas) | `"seccion"` · `"tipo"` · `"{"` · `"}"` |
| **No terminales que aparecen** (se abren en otra producción) | `<identificador>` · `<tipo_seccion>` · `<evento>` · `<nl>` |
| **Producciones que usan `<seccion>`** | `<programa>` |

## Ejemplo válido

```
seccion cancion tipo estrofa { frase1 frase1 frase2 frase2 }
seccion cierre tipo coda { [do3 mi3 sol3 do4]:redonda }
```

## Derivación del ejemplo hasta los átomos

Cada flecha aplica una producción; entre paréntesis, cuál. Al final solo quedan terminales entre comillas.

```
<seccion>
→ "seccion" <identificador> "tipo" <tipo_seccion> "{" <identificador> <identificador> "}" <nl>   (5)
→ "seccion" "c" "a" "n" "c" "i" "o" "n" "tipo" <tipo_seccion> "{" … "}" <nl>   (24, 28)
→ "seccion" … "tipo" "estrofa" "{" … "}" <nl>   (6 tipo_seccion)
→ … "{" "f" "r" "a" "s" "e" "1"  "f" "r" "a" "s" "e" "2" "}" <nl>   (24, 28, 30)

Resultado:  seccion cancion tipo estrofa { frase1 frase2 } ↵
```

## Ejemplo inválido

```
seccion cancion { frase1 }
```

**Por qué no deriva:** Falta `"tipo" <tipo_seccion>`, que es obligatorio.

## Nota de diseño

El tipo es la bisagra entre las dos mitades del lenguaje: declarar `tipo estrofa` es lo que pone `es_estrofa` en `true` mientras suena la sección.

---
*Convención: `<x>` no terminal · `"x"` terminal · `'"'` la comilla doble como terminal · `{ }` cero o más · `[ ]` cero o uno · `|` alternativa · `<nl>` salto de línea*
