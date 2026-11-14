# pruebas_14nov.py · el parser: árbol de cada instrucción y errores sintácticos con línea y columna
# Uso: python pruebas_14nov.py

import contextlib
import io
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")   # para que los ✔ salgan también al redirigir la salida en Windows

AQUI = os.path.dirname(os.path.abspath(__file__))
COMPILADOR = os.path.join(AQUI, "compilador")
sys.path.insert(0, COMPILADOR)

from arbol import mostrar_arbol
from lexer import tokenizar
from parser import Parser
from tokens import ErrorDeLenguaje, ErrorLexico, ErrorSintactico

aciertos = 0
total = 0


def revisar(nombre, entrada, esperado, real):
    global aciertos, total
    coincide = real == esperado
    aciertos += coincide
    total += 1
    print(nombre)
    print("   entrada :", repr(entrada))
    print("   esperado:")
    print("      " + str(esperado).replace("\n", "\n      "))
    print("   real    :")
    print("      " + str(real).replace("\n", "\n      "))
    print("   ", "✔ coincide" if coincide else "✘ NO coincide")
    print()


def arbol_de(codigo):
    """Lo que imprime mostrar_arbol, o el mensaje del error si el código no es válido."""
    salida = io.StringIO()
    try:
        programa = Parser(tokenizar(codigo)).programa()
        with contextlib.redirect_stdout(salida):
            mostrar_arbol(programa)
        return salida.getvalue().rstrip("\n")
    except ErrorDeLenguaje as e:
        return str(e)


# ----- 1 · el árbol de cada instrucción -----
casos_arbol = [
    ("declaración con un número", "tempo 120",
     "Programa\n  Declaracion tempo\n    Numero 120"),
    ("declaración con decimal, texto y booleano", 'umbral 0.75\ncompas "4/4"\nes_intro true',
     'Programa\n  Declaracion umbral\n    Numero 0.75\n  Declaracion compas\n    Cadena "4/4"\n'
     "  Declaracion es_intro\n    Booleano true"),
    ("la resta se agrupa a la izquierda: (10 - 3) - 2", "r 10 - 3 - 2",
     "Programa\n  Declaracion r\n    OperacionBinaria -\n      OperacionBinaria -\n"
     "        Numero 10\n        Numero 3\n      Numero 2"),
    ("la multiplicación queda debajo de la suma", "total a + 5 * 2",
     "Programa\n  Declaracion total\n    OperacionBinaria +\n      Variable a\n"
     "      OperacionBinaria *\n        Numero 5\n        Numero 2"),
    ("el paréntesis baja la resta y no crea nodo", "volumen = (tempo - 20) / 4",
     "Programa\n  Asignacion volumen\n    OperacionBinaria /\n      OperacionBinaria -\n"
     "        Variable tempo\n        Numero 20\n      Numero 4"),
    ("asignación: el '=' decide que no es declaración", "volumen = 80",
     "Programa\n  Asignacion volumen\n    Numero 80"),
    ("salida con mostrar", "mostrar tempo - 20",
     "Programa\n  Mostrar\n    OperacionBinaria -\n      Variable tempo\n      Numero 20"),
    ("líneas vacías y comentarios no crean instrucciones", "# cabecera\n\ntempo 120\n\n/* nada */\n",
     "Programa\n  Declaracion tempo\n    Numero 120"),
]
for nombre, codigo, esperado in casos_arbol:
    revisar("Árbol · " + nombre, codigo, esperado, arbol_de(codigo))


# ----- 2 · errores sintácticos con línea y columna (calculados a mano) -----
casos_error = [
    ("sobra un valor: la instrucción debía terminar", "x 5 3",
     "Error sintáctico en línea 1, columna 5: se esperaba el fin de la línea y llegó '3'"),
    ("dos operadores seguidos", "y 4 + * 2",
     "Error sintáctico en línea 1, columna 7: se esperaba un número, una variable o '(' y llegó '*'"),
    ("paréntesis sin cerrar al final del archivo", "z (1 + 2",
     "Error sintáctico en línea 1, columna 9: se esperaba ')' y llegó el fin del archivo"),
    ("paréntesis sin cerrar al final de la línea", "z (1 + 2\ntempo 120",
     "Error sintáctico en línea 1, columna 9: se esperaba ')' y llegó el fin de la línea"),
    ("asignación sin valor", "x =",
     "Error sintáctico en línea 1, columna 4: se esperaba un número, una variable o '(' y llegó el fin del archivo"),
    ("error en la línea 2", "tempo 120\nvolumen = tempo *\n",
     "Error sintáctico en línea 2, columna 18: se esperaba un número, una variable o '(' y llegó el fin de la línea"),
    ("una instrucción no empieza con un número", "120 tempo",
     "Error sintáctico en línea 1, columna 1: se esperaba el inicio de una instrucción y llegó '120'"),
    ("mostrar sin nada que mostrar", "mostrar",
     "Error sintáctico en línea 1, columna 8: se esperaba un número, una variable o '(' y llegó el fin del archivo"),
]
for nombre, codigo, esperado in casos_error:
    revisar("Error sintáctico · " + nombre, codigo, esperado, arbol_de(codigo))


# ----- 3 · los errores heredan de ErrorDeLenguaje -----
try:
    Parser(tokenizar("x 5 3")).programa()
    real = "no lanzó error"
except ErrorDeLenguaje as e:
    real = (type(e).__name__, e.linea, e.columna)
revisar("Herencia · el error sintáctico se atrapa como ErrorDeLenguaje", "x 5 3", ("ErrorSintactico", 1, 5), real)

try:
    tokenizar("tempo 120 @")
    real = "no lanzó error"
except ErrorDeLenguaje as e:
    real = (type(e).__name__, str(e))
revisar("Herencia · el léxico también, con el mismo formato", "tempo 120 @",
        ("ErrorLexico", "Error léxico en línea 1, columna 11: carácter '@' no reconocido"), real)

revisar("Herencia · las dos clases son hijas de ErrorDeLenguaje", "issubclass",
        (True, True), (issubclass(ErrorLexico, ErrorDeLenguaje), issubclass(ErrorSintactico, ErrorDeLenguaje)))


# ----- 4 · main.py imprime el árbol o el error -----
def correr_main(archivo):
    r = subprocess.run([sys.executable, "main.py", archivo], cwd=COMPILADOR, capture_output=True,
                       encoding="utf-8", env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    return r.returncode, r.stdout, "Traceback" in r.stderr

revisar("main.py · programa.txt imprime el árbol",
        "python main.py programa.txt",
        (0, "Programa\n  Declaracion tempo\n    Numero 120\n  Asignacion volumen\n    Numero 5\n", False),
        correr_main("programa.txt"))

revisar("main.py · sintactico.txt da el error y la posición por separado",
        "python main.py sintactico.txt",
        (1, "Error sintáctico en línea 2, columna 18: se esperaba un número, una variable o '(' y llegó el fin de la línea\n"
            "linea = 2, columna = 18\n", False),
        correr_main("sintactico.txt"))

revisar("main.py · el error léxico se atrapa con el mismo except",
        "python main.py programa_invalido.txt",
        (1, "Error léxico en línea 1, columna 11: carácter '@' no reconocido\nlinea = 1, columna = 11\n", False),
        correr_main("programa_invalido.txt"))

print(f"{aciertos} de {total} casos coinciden")
