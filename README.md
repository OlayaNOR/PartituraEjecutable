# TocaScript

Un lenguaje para escribir música que además se ejecuta. Un programa en TocaScript se lee como el encabezado y las indicaciones de una partitura, y el intérprete lo corre.

**Integrantes del grupo 8 de Lenguajes Formales**

- Valeria Alarcón Munera
- Nicolás Olaya Rincón
- Andrew García Mosquera

## Cómo ejecutar

Hace falta Python 3.10 o superior. No usa librerías externas.

```
python main.py programa.txt
```

Otros modos para ver lo que hace cada fase:

```
python main.py --tokens programa.txt     muestra los tokens que entrega el lexer
python main.py --arbol programa.txt      muestra el árbol que arma el parser
```

Las pruebas de todo el proyecto se corren con `python pruebas/pruebas_final.py`. En la carpeta `programas` están los programas de muestra y tres archivos con un error de cada fase.

## Ficha del lenguaje

### Nombre

**TocaScript** viene de *tocar*. Una partitura no explica, indica cómo hay que tocar. Por eso el verbo central del lenguaje es `TOCAR` y de ahí sale el nombre. Las reglas dicen "al pasar esto, toca así", y se escriben `AL condición TOCAR`.

### Tabla de traducción desde Java

| Qué | Java | TocaScript |
|---|---|---|
| Tipos | `int edad = 20;` y `double nota = 4.5;` y `String s = "hola";` y `boolean b = true;` | no se escriben. El valor trae su tipo y la variable lo conserva: `edad 20` es entero, `nota 4.5` es decimal, `s "hola"` es texto y `b true` es booleano |
| Asignación | `edad = edad + 1;` | `edad = edad + 1` |
| Fin de instrucción | `;` | el salto de línea |
| Salida | `System.out.println(total);` | `mostrar total` |
| Condicional | `if (n > 2) { ... } else { ... }` | `AL n > 2 TOCAR { ... } SINO { ... }` |
| Ciclo | `while (n <= 5) { ... }` | `repetir mientras n <= 5 { ... }` |
| Ciclo con contador | `for (int i = 1; i <= 3; i = i + 1) { ... }` | `repetir 3 con i { ... }` |
| Igual y distinto | `==` y `!=` | `=` y `<>` |
| Lógicos | `&&` y `\|\|` y `!` | `Y` y `O` y `NO` |
| Comentario | `// una línea` y `/* bloque */` | `# una línea` y `/* bloque */` |

### Decisión de diseño

**Declarar una variable es escribir su nombre y su valor, sin tipo y sin signo igual.** En una partitura arriba se escribe `tempo 120` o `compas "4/4"`, y nadie aclara que 120 es un número. TocaScript hace lo mismo: `tempo 120` crea la variable y el valor decide su tipo. Desde ahí el tipo queda fijo, así que `tempo = "rapido"` es un error semántico. Así un programa empieza como empieza una partitura y el control de tipos no se pierde.

Otras dos decisiones que salen de la misma idea:

- El salto de línea termina la instrucción, como cada indicación de una partitura va en su renglón. No hay punto y coma.
- Un texto se puede unir con un número: `mostrar "tempo " + tempo` muestra `tempo 120`. En una partitura se escribe así la indicación de tempo.

## Gramática final en EBNF

`::=` se lee "está formado por", `|` se lee "o", `*` es cero o más veces y `?` es cero o una vez. Lo que va entre comillas es un token exacto y lo que va en mayúsculas es un tipo de token.

```
programa    ::= ( instruccion | NL )* EOF
instruccion ::= declaracion | asignacion | salida | condicional | ciclo | repeticion
declaracion ::= IDENTIFICADOR condicion fin
asignacion  ::= IDENTIFICADOR '=' condicion fin
salida      ::= 'mostrar' condicion fin
condicional ::= 'AL' condicion 'TOCAR' bloque ( 'SINO' bloque )? fin
ciclo       ::= 'repetir' 'mientras' condicion bloque fin
repeticion  ::= 'repetir' expresion ( 'con' IDENTIFICADOR )? bloque fin
bloque      ::= '{' ( instruccion | NL )* '}'
fin         ::= NL | EOF
condicion   ::= conjuncion ( 'O' conjuncion )*
conjuncion  ::= negacion ( 'Y' negacion )*
negacion    ::= 'NO' negacion | comparacion
comparacion ::= expresion ( ( COMPARADOR | '=' ) expresion )?
expresion   ::= termino ( ( '+' | '-' ) termino )*
termino     ::= factor ( ( '*' | '/' ) factor )*
factor      ::= '-' factor | NUMERO | TEXTO | BOOLEANO | IDENTIFICADOR | '(' condicion ')'
```

Notas de la gramática:

- `declaracion` y `asignacion` empiezan con un nombre. El parser mira el token siguiente y si es `=` es una asignación.
- El `=` asigna cuando es una instrucción y compara dentro de una condición. `AL compas = "4/4" TOCAR` pregunta si son iguales.
- Antes de la llave que cierra un bloque una instrucción también puede terminar, así que `AL n > 2 TOCAR { mostrar n }` cabe en una línea.
- `O` está por debajo de `Y`, `Y` por debajo de `NO` y `NO` por debajo de la comparación. Por eso `true O false Y false` da `true`.
- La recursión por la izquierda se evita con `*`, que en el parser es un `while`.
- COMPARADOR es `<`, `>`, `<=`, `>=` o `<>`. El lexer revisa primero los de dos caracteres.

## Reglas de operaciones entre tipos

| Operación | entero con entero | con al menos un decimal | texto con texto | texto con número | con un booleano |
|---|---|---|---|---|---|
| `+` | entero | decimal | une los textos | une, el número pasa a texto | error |
| `-` y `*` | entero | decimal | error | error | error |
| `/` | división entera, se corta hacia cero | decimal | error | error | error |
| `<` `>` `<=` `>=` | compara | compara | error | error | error |
| `=` y `<>` | compara | compara | compara | error | solo con otro booleano |
| `Y` `O` `NO` | error | error | error | error | operan |

Así `7 / 2` da `3`, `7 / 2.0` da `3.5`, `"ho" + "la"` da `hola`, `"tempo " + 120` da `tempo 120` y `"hola" * 2` da un error en la columna del `*`.

Qué guarda cada variable:

| Tipo de la variable | Acepta |
|---|---|
| entero | enteros |
| decimal | decimales y enteros, que se guardan como decimal |
| texto | textos |
| booleano | `true` y `false` |

Los errores semánticos que revisa el intérprete:

1. Usar o asignar una variable que no se ha declarado.
2. Declarar dos veces la misma variable en el mismo bloque.
3. Guardar un valor de un tipo que la variable no acepta.
4. Dividir por cero.
5. Una condición de `AL` o de `repetir mientras` que no da `true` o `false`.
6. Un ciclo que pasa de 100000 vueltas, para que el intérprete no se quede pegado.

## Requerimientos electivos

**1. Ciclo con contador.** Es el `repetir` de TocaScript, que ya existía en la gramática del lenguaje para repetir un motivo. `repetir 3 { ... }` repite el bloque tres veces y `repetir 3 con vuelta { ... }` además crea la variable `vuelta`, que vale 1, 2 y 3. El contador solo existe dentro del bloque. Si las veces no son un entero de cero en adelante, sale un error semántico.

```
repetir 3 con vuelta {
    mostrar vuelta * 10
}
```

Salida: `10`, `20` y `30`.

**2. Tipo booleano.** `true` y `false` se guardan en variables y sirven como condición. Una comparación da un booleano, así que se puede guardar. Una variable booleana no acepta otro tipo y una condición que no da booleano es un error.

```
listo 4 > 3
mostrar listo
AL listo TOCAR { mostrar "ok" }
```

Salida: `true` y `ok`.

## Estructura del repositorio

```
README.md          este documento
tokens.py          la clase Token y los errores de cada fase, que heredan de ErrorDeLenguaje
lexer.py           convierte el texto en tokens con línea y columna
arbol.py           los nodos del árbol y la función que lo imprime
parser.py          la gramática como métodos: arma el árbol o lanza ErrorSintactico
interprete.py      recorre el árbol, guarda las variables en entornos anidados y lanza ErrorSemantico
main.py            une las tres fases y señala el error en el código con un ^
programa.txt       un programa de ejemplo
programas/         los tres programas de muestra, otros ejemplos y un error de cada fase
pruebas/           las pruebas de todo el proyecto
```

El resto del repositorio es la historia del lenguaje a lo largo del semestre. El diseño original y las 15 reglas están en `DISENO.md`, la gramática del primer corte con sus 33 producciones en `gramatica.md`, y los pasos con los que se construyó el lexer en la carpeta `lexer`.

## Programas de muestra

**Tabla de multiplicar del 3** en `programas/tabla_del_3.txt`

```
n 1
repetir mientras n <= 5 {
    mostrar n * 3
    n = n + 1
}
```

Salida: `3`, `6`, `9`, `12` y `15`.

**Factorial de 5** en `programas/factorial.txt`

```
n 5
resultado 1
repetir mientras n > 1 {
    resultado = resultado * n
    n = n - 1
}
mostrar resultado
```

Salida: `120`.

**Promedio de tres notas** en `programas/promedio.txt`

```
promedio (3.0 + 4.0 + 5.0) / 3.0
mostrar promedio
AL promedio >= 3.0 TOCAR {
    mostrar "aprueba"
} SINO {
    mostrar "reprueba"
}
```

Salida: `4.0` y `aprueba`.

## Errores que señalan el código

Los tres tipos de error se atrapan igual en `main.py`. Además del mensaje se muestra la línea del programa con un `^` debajo de la columna.

```
> python main.py programas/errores/semantico.txt
Error semántico en línea 2, columna 15: división por cero
    mostrar tempo / (tempo - 120)
                  ^
linea = 2, columna = 15
```
