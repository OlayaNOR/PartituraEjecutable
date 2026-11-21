# pruebas_final.py · todo lo que debe funcionar en la entrega final, con la salida esperada calculada a mano
# Uso (desde la raíz del repositorio): python pruebas/pruebas_final.py

import os
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")   # para que los ✔ salgan también al redirigir la salida en Windows

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

from interprete import Interprete
from lexer import tokenizar
from parser import Parser
from tokens import ErrorDeLenguaje

aciertos = 0
total = 0


def revisar(nombre, entrada, esperado, real):
    global aciertos, total
    coincide = real == esperado
    aciertos += coincide
    total += 1
    print(nombre)
    print("   entrada :", entrada.replace("\n", " ⏎ ") if isinstance(entrada, str) else entrada)
    print("   esperado:", esperado)
    print("   real    :", real)
    print("   ", "✔ coincide" if coincide else "✘ NO coincide")
    print()


def correr(codigo):
    """Ejecuta el programa y devuelve lo que mostró, y el mensaje del error al final si hubo uno."""
    salida = []
    try:
        Interprete(salida.append).ejecutar_programa(Parser(tokenizar(codigo)).programa())
    except ErrorDeLenguaje as e:
        salida.append(str(e))
    return salida


def caso(nombre, codigo, esperado):
    revisar(nombre, codigo, esperado, correr(codigo))


# ===== 1 · El programa se ejecuta: salida, entorno, cuentas y tipos =====
caso("Ejecuta · variables y cuentas (precios)",
     'precio 12000\ncantidad 3\ntotal precio * cantidad\nmostrar total\npromedio total / 4.0\n'
     'mostrar promedio\nmensaje "Fin del calculo"\nmostrar mensaje',
     ["36000", "9000.0", "Fin del calculo"])
caso("Ejecuta · la multiplicación antes que la suma", "a 3\ntotal a + 5 * 2\nmostrar total", ["13"])
caso("Tipos · entero / entero es división entera", "mostrar 7 / 2", ["3"])
caso("Tipos · con un decimal la división es decimal", "mostrar 7 / 2.0", ["3.5"])
caso("Tipos · la división entera se corta hacia cero", "mostrar -7 / 2", ["-3"])
caso("Tipos · texto + texto une", 'mostrar "ho" + "la"', ["hola"])
caso("Tipos · texto + número une (decisión de TocaScript)", 'mostrar "tempo " + 120', ["tempo 120"])
caso("Tipos · texto * número es error en el *",
     'mostrar 7 / 2\nmostrar 7 / 2.0\nmostrar "ho" + "la"\nmostrar "hola" * 2',
     ["3", "3.5", "hola", "Error semántico en línea 4, columna 16: no se puede usar '*' con textos"])
caso("Tipos · un decimal acepta un entero y lo guarda como decimal", "p 2.5\np = 3\nmostrar p", ["3.0"])

# ===== 2 · Errores semánticos =====
caso("Semántico · variable no declarada", "mostrar edad",
     ["Error semántico en línea 1, columna 9: la variable 'edad' no ha sido declarada"])
caso("Semántico · declarada dos veces", "x 1\nx 2",
     ["Error semántico en línea 2, columna 1: la variable 'x' ya fue declarada en la línea 1"])
caso("Semántico · un texto en una variable entera", 'n 5\nn = "hola"',
     ["Error semántico en línea 2, columna 1: no se puede guardar un texto en la variable 'n' de tipo entero"])
caso("Semántico · un booleano no cabe en una variable entera", "n 1\nn = true",
     ["Error semántico en línea 2, columna 1: no se puede guardar un booleano en la variable 'n' de tipo entero"])
caso("Semántico · asignar a una variable no declarada", "volumen = 80",
     ["Error semántico en línea 1, columna 1: la variable 'volumen' no ha sido declarada"])
caso("Semántico · división por cero", "d 10 / 0",
     ["Error semántico en línea 1, columna 6: división por cero"])
caso("Semántico · lo de antes del error ya se mostró", "a 5\nmostrar a\nmostrar b",
     ["5", "Error semántico en línea 3, columna 9: la variable 'b' no ha sido declarada"])

# ===== 3 · Decidir y repetir =====
revisar("Lexer · '<=' sale como un solo COMPARADOR", "n <= 5",
        ["IDENTIFICADOR('n') en 1:1", "COMPARADOR('<=') en 1:3", "NUMERO('5') en 1:6", "EOF('') en 1:7"],
        [str(t) for t in tokenizar("n <= 5")])
revisar("Lexer · el '=' sale como SIMBOLO", "a = b",
        ["IDENTIFICADOR('a') en 1:1", "SIMBOLO('=') en 1:3", "IDENTIFICADOR('b') en 1:5", "EOF('') en 1:6"],
        [str(t) for t in tokenizar("a = b")])
caso("Condicional · con SINO", 'AL 2 > 1 TOCAR { mostrar "si" } SINO { mostrar "no" }', ["si"])
caso("Condicional · sin SINO, el programa sigue", 'AL 1 > 2 TOCAR { mostrar "si" }\nmostrar "fin"', ["fin"])
caso("Condicional · SINO en la línea siguiente a la llave",
     'nota 2\nAL nota >= 3 TOCAR {\n    mostrar "aprobado"\n}\nSINO {\n    mostrar "reprobado"\n}', ["reprobado"])
caso("Condicional · '=' compara dentro de la condición", 'compas "4/4"\nAL compas = "4/4" TOCAR { mostrar "normal" }',
     ["normal"])
caso("Ciclo · repetir mientras", "n 1\nrepetir mientras n <= 3 {\n    mostrar n\n    n = n + 1\n}", ["1", "2", "3"])
caso("Ciclo · un bloque dentro de otro",
     "n 1\nrepetir mientras n <= 4 {\n    AL n > 2 TOCAR { mostrar n }\n    n = n + 1\n}", ["3", "4"])
caso("Bloque · sin cerrar", "AL 1 < 2 TOCAR { mostrar 1",
     ["Error sintáctico en línea 1, columna 27: falta '}' para cerrar el bloque abierto en la línea 1"])
salida = correr("n 1\nrepetir mientras n <= 3 {\n    mostrar n\n}")
revisar("Ciclo · infinito: muchos 1 y después el error en 'repetir'", "n 1 ⏎ repetir mientras n <= 3 { mostrar n }",
        (100000, "Error semántico en línea 2, columna 1: el ciclo superó 100000 vueltas; "
                 "¿falta actualizar la variable de la condición?"),
        (salida.count("1"), salida[-1]))
caso("Programa completo · suma del 1 al 5 y decisión",
     open(os.path.join(RAIZ, "programa.txt"), encoding="utf-8").read(), ["15", "grande"])

# ===== 4 · Requerimientos obligatorios =====
caso("Obligatorio 1 · alcance: lo declarado en el bloque no existe afuera",
     "AL 1 < 2 TOCAR {\n    x 5\n}\nmostrar x",
     ["Error semántico en línea 4, columna 9: la variable 'x' no ha sido declarada"])
caso("Obligatorio 1 · alcance: una asignación dentro del bloque cambia la variable de afuera",
     "n 1\nAL true TOCAR { n = 2 }\nmostrar n", ["2"])
caso("Obligatorio 1 · alcance: cada vuelta abre un bloque nuevo", "repetir 2 {\n    x 1\n    mostrar x\n}", ["1", "1"])
caso("Obligatorio 2 · lógicos: Y en rango", 'n 7\nAL n >= 1 Y n <= 10 TOCAR {\n    mostrar "en rango"\n}',
     ["en rango"])
caso("Obligatorio 2 · lógicos: Y va antes que O", "mostrar true O false Y false", ["true"])
caso("Obligatorio 2 · lógicos: NO va por encima de la comparación", "mostrar NO 1 > 2", ["true"])
caso("Obligatorio 2 · lógicos: con números es error", "mostrar 1 Y true",
     ["Error semántico en línea 1, columna 11: 'Y' solo se usa con true o false"])
caso("Obligatorio 3 · negativos", "x -5\ny -(x + 2)\nmostrar y", ["3"])
caso("Obligatorio 3 · menos y menos", "mostrar 2 - -3", ["5"])
caso("Obligatorio 3 · el menos con un texto es error", 'mostrar -"a"',
     ["Error semántico en línea 1, columna 9: el menos solo se usa con números"])

# ===== 5 · Requerimientos electivos =====
caso("Electivo ciclo con contador · repetir 3 con vuelta", "repetir 3 con vuelta {\n    mostrar vuelta * 10\n}",
     ["10", "20", "30"])
caso("Electivo ciclo con contador · repetir sin contador", 'repetir 2 {\n    mostrar "la"\n}', ["la", "la"])
caso("Electivo ciclo con contador · el contador no existe después",
     "repetir 1 con vuelta { mostrar vuelta }\nmostrar vuelta",
     ["1", "Error semántico en línea 2, columna 9: la variable 'vuelta' no ha sido declarada"])
caso("Electivo ciclo con contador · las veces deben ser un entero", "repetir 2.5 { mostrar 1 }",
     ["Error semántico en línea 1, columna 1: repetir necesita un número entero de veces, cero o más"])
caso("Electivo booleano · una comparación guardada en una variable", 'listo 4 > 3\nmostrar listo\nAL listo TOCAR { mostrar "ok" }',
     ["true", "ok"])
caso("Electivo booleano · un entero no cabe en una variable booleana", "listo true\nlisto = 5",
     ["Error semántico en línea 2, columna 1: no se puede guardar un entero en la variable 'listo' de tipo booleano"])
caso("Electivo booleano · la condición debe dar true o false", "AL 5 TOCAR { mostrar 1 }",
     ["Error semántico en línea 1, columna 1: la condición de AL debe dar true o false"])
caso("Electivo booleano · no se suma con booleanos", "mostrar true + 1",
     ["Error semántico en línea 1, columna 14: no se puede usar '+' con booleanos"])


# ===== 6 · main.py: los tres programas de muestra y los errores que señalan el código =====
def main_py(archivo):
    r = subprocess.run([sys.executable, "main.py", archivo], cwd=RAIZ, capture_output=True, encoding="utf-8",
                       env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    return r.stdout, "Traceback" in r.stderr

revisar("Muestra · tabla del 3", "python main.py programas/tabla_del_3.txt", ("3\n6\n9\n12\n15\n", False),
        main_py("programas/tabla_del_3.txt"))
revisar("Muestra · factorial de 5", "python main.py programas/factorial.txt", ("120\n", False),
        main_py("programas/factorial.txt"))
revisar("Muestra · promedio de tres notas", "python main.py programas/promedio.txt", ("4.0\naprueba\n", False),
        main_py("programas/promedio.txt"))
revisar("Obligatorio 4 · error léxico con la línea y el ^", "python main.py programas/errores/lexico.txt",
        ("Error léxico en línea 2, columna 14: carácter '@' no reconocido\n"
         '    compas "4/4" @\n'
         "                 ^\n"
         "linea = 2, columna = 14\n", False),
        main_py("programas/errores/lexico.txt"))
revisar("Obligatorio 4 · error semántico con la línea y el ^", "python main.py programas/errores/semantico.txt",
        ("Error semántico en línea 2, columna 15: división por cero\n"
         "    mostrar tempo / (tempo - 120)\n"
         "                  ^\n"
         "linea = 2, columna = 15\n", False),
        main_py("programas/errores/semantico.txt"))

print(f"{aciertos} de {total} casos coinciden")
