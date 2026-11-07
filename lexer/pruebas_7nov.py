# pruebas_7nov.py · prototipo con clases: Token, ErrorLexico y Parser en compilador/
# Uso: python pruebas_7nov.py

import ast
import os
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")   # para que los ✔ salgan también al redirigir la salida en Windows

AQUI = os.path.dirname(os.path.abspath(__file__))
COMPILADOR = os.path.join(AQUI, "compilador")
sys.path.insert(0, COMPILADOR)

from lexer import tokenizar
from parser import Parser
from tokens import Token, ErrorLexico

aciertos = 0
total = 0


def revisar(nombre, entrada, esperado, real):
    global aciertos, total
    coincide = real == esperado
    aciertos += coincide
    total += 1
    print(nombre)
    print("   entrada :", repr(entrada))
    print("   esperado:", esperado)
    print("   real    :", real)
    print("   ", "✔ coincide" if coincide else "✘ NO coincide")
    print()


# ----- 1 · las pruebas anteriores, leyendo t.tipo, t.texto, t.linea y t.columna -----
arbol = ast.parse(open(os.path.join(AQUI, "pruebas_30oct.py"), encoding="utf-8").read())
casos_30oct = next(ast.literal_eval(n.value) for n in arbol.body
                   if isinstance(n, ast.Assign) and n.targets[0].id == "casos")

for nombre, entrada, esperado in casos_30oct:
    if isinstance(esperado, list):
        real = [(t.tipo, t.texto, t.linea, t.columna) for t in tokenizar(entrada)]
    else:
        # los casos de error se comparan por posición: la línea y la columna salen del ErrorLexico
        linea, columna = map(int, re.match(r"Línea (\d+), columna (\d+)", esperado).groups())
        esperado = (linea, columna)
        try:
            tokenizar(entrada)
            real = "no lanzó error"
        except ErrorLexico as e:
            real = (e.linea, e.columna)
    revisar("Token · " + nombre, entrada, esperado, real)


# ----- 2 · la clase Token -----
t = tokenizar("volumen = 5")[2]
revisar("Token · es un objeto Token con sus cuatro atributos",
        "volumen = 5",
        (True, "NUMERO", "5", 1, 11),
        (isinstance(t, Token), t.tipo, t.texto, t.linea, t.columna))

revisar("Token · se imprime legible",
        "volumen = 5",
        "NUMERO('5') en 1:11",
        str(t))


# ----- 3 · la clase ErrorLexico -----
try:
    tokenizar("tempo 120 @")
    real = "no lanzó error"
except ErrorLexico as e:
    real = (str(e), e.linea, e.columna)
revisar("ErrorLexico · mensaje completo y posición por separado",
        "tempo 120 @",
        ("Error léxico en línea 1, columna 11: carácter '@' no reconocido", 1, 11),
        real)


# ----- 4 · la clase Parser -----
p = Parser(tokenizar("tempo 120"))
revisar("Parser · actual() no se mueve",
        "tempo 120",
        ("tempo", "tempo", 0),
        (p.actual().texto, p.actual().texto, p.pos))

primero = p.avanzar()
revisar("Parser · avanzar() devuelve el token actual y pasa al siguiente",
        "tempo 120",
        ("tempo", "120", 1),
        (primero.texto, p.actual().texto, p.pos))

p.avanzar()
p.avanzar()
p.avanzar()
revisar("Parser · en EOF avanzar() se queda quieto",
        "tempo 120",
        ("EOF", 2),
        (p.actual().tipo, p.pos))

a = Parser(tokenizar("tempo 120"))
b = Parser(tokenizar("volumen = 5"))
a.avanzar()
revisar("Parser · dos objetos Parser llevan cada uno su posición",
        "a con 'tempo 120', b con 'volumen = 5', solo avanza a",
        (1, "120", 0, "volumen"),
        (a.pos, a.actual().texto, b.pos, b.actual().texto))


# ----- 5 · main.py recorre los tokens con el Parser -----
def correr_main(archivo):
    r = subprocess.run([sys.executable, "main.py", archivo], cwd=COMPILADOR, capture_output=True,
                       encoding="utf-8", env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    return r.returncode, r.stdout, "Traceback" in r.stderr

revisar("main.py · archivo válido, recorre hasta EOF",
        "python main.py programa.txt",
        (0, "IDENTIFICADOR('tempo') en 1:1\n"
            "NUMERO('120') en 1:7\n"
            "NL('\\n') en 1:10\n"
            "IDENTIFICADOR('volumen') en 2:1\n"
            "SIMBOLO('=') en 2:9\n"
            "NUMERO('5') en 2:11\n"
            "NL('\\n') en 2:12\n"
            "EOF('') en 3:1\n", False),
        correr_main("programa.txt"))

revisar("main.py · archivo inválido, mensaje y posición sin traza de Python",
        "python main.py programa_invalido.txt",
        (1, "Error léxico en línea 1, columna 11: carácter '@' no reconocido\n"
            "linea = 1, columna = 11\n", False),
        correr_main("programa_invalido.txt"))

archivos = sorted(f for f in os.listdir(COMPILADOR) if f.endswith(".py"))
revisar("Organización · los cuatro archivos",
        "compilador/",
        ["lexer.py", "main.py", "parser.py", "tokens.py"],
        archivos)

print(f"{aciertos} de {total} casos coinciden")
