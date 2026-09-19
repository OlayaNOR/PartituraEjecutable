# Producción 8 · `<nota>`

**La música** · Gramática BNF de TocaScript · Grupo 8

## La producción

La producción `<nota>` y, debajo, todas las que abre hasta llegar a los átomos —terminales entre comillas—. Todo en un mismo sitio, como en el tablero.

```
 8  <nota> ::= <nombre_nota> [ "#" | "b" ] <octava>

 9  <nombre_nota> ::= "do" | "re" | "mi" | "fa" | "sol" | "la" | "si"
10  <octava> ::= <digito>
30  <digito> ::= "0" | "1" | "2" | "..." | "9"
```

## Cómo se lee

Un nombre de nota, una alteración opcional —sostenido o bemol— y la octava, obligatoria.

## Qué usa y quién la usa

| | |
|---|---|
| **Terminales que aparecen** (entre comillas) | `"#"` · `"b"` |
| **No terminales que aparecen** (se abren en otra producción) | `<nombre_nota>` · `<octava>` |
| **Producciones que usan `<nota>`** | `<evento>` |

## Ejemplo válido

```
do4
fa#4
mib3
```

## Derivación del ejemplo hasta los átomos

Cada flecha aplica una producción; entre paréntesis, cuál. Al final solo quedan terminales entre comillas.

```
<nota>
→ <nombre_nota> "#" <octava>   (8, con la alteración opcional)
→ "fa" "#" <octava>   (9 nombre_nota)
→ "fa" "#" <digito>  →  "fa" "#" "4"   (10 octava · 30 digito)

Resultado:  fa#4
```

## Ejemplo inválido

```
do
fa4#
```

**Por qué no deriva:** `do` sin octava no deriva. `fa4#` tiene la alteración después de la octava; el orden es nombre, alteración, octava.

## Nota de diseño

Las notas se escriben pegadas: `do4` es un solo token para el lexer.

---
*Convención: `<x>` no terminal · `"x"` terminal · `'"'` la comilla doble como terminal · `{ }` cero o más · `[ ]` cero o uno · `|` alternativa · `<nl>` salto de línea*
