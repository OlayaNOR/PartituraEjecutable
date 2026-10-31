# pruebas_31oct.py · casos de las tareas 13 a 16 con la salida esperada calculada a mano

import ast
import os
import subprocess
import sys
from dataclasses import astuple

sys.stdout.reconfigure(encoding="utf-8")   # para que los ✔ salgan también al redirigir la salida en Windows

AQUI = os.path.dirname(os.path.abspath(__file__))
COMPILADOR = os.path.join(AQUI, "compilador")

import paso13
import paso14

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
    print("   ", "✔ coincide" if coincide else "✘ NO coincide: revisar si se equivocó el cálculo o el lexer")
    print()


# ----- Tarea 13 · clase Token -----
# Los casos se leen de pruebas_30oct.py sin ejecutarlo (ast), así no se repiten a mano.
arbol = ast.parse(open(os.path.join(AQUI, "pruebas_30oct.py"), encoding="utf-8").read())
casos_30oct = next(ast.literal_eval(n.value) for n in arbol.body
                   if isinstance(n, ast.Assign) and n.targets[0].id == "casos")

for nombre, entrada, esperado in casos_30oct:
    try:
        real = [astuple(t) for t in paso13.tokenizar(entrada)]   # Token -> tupla para comparar
    except SyntaxError as e:
        real = str(e)
    revisar("T13 · " + nombre, entrada, esperado, real)

revisar("T13 · __str__ legible",
        'volumen = 5',
        ["IDENTIFICADOR('volumen') en 1:1", "SIMBOLO('=') en 1:9", "NUMERO('5') en 1:11", "EOF('') en 1:12"],
        [str(t) for t in paso13.tokenizar('volumen = 5')])

t = paso13.tokenizar('tempo 120')[1]
revisar("T13 · los datos se leen con punto",
        'tempo 120',
        ("NUMERO", "120", 1, 7),
        (t.tipo, t.texto, t.linea, t.columna))


# ----- Tarea 14 · excepción propia -----
# (entrada, línea, columna, mensaje completo)
errores = [
    ("T14 · error en la línea 2",
     'tempo 120\nvolumen 2 @', 2, 11,
     "Error léxico en línea 2, columna 11: carácter '@' no reconocido"),
    ("T14 · un ! solo",
     'x ! 5', 1, 3,
     "Error léxico en línea 1, columna 3: carácter '!' no reconocido"),
    ("T14 · comentario de bloque sin cerrar",
     'tempo 120\n/* uno\ndos', 2, 1,
     "Error léxico en línea 2, columna 1: comentario sin cerrar"),
    ("T14 · decimal con dos puntos",
     'umbral 3.4.5', 1, 8,
     "Error léxico en línea 1, columna 8: número mal formado, tiene más de un punto"),
    ("T14 · texto sin cerrar",
     'tempo 100\ntonalidad "Do mayor', 2, 11,
     "Error léxico en línea 2, columna 11: texto sin cerrar, falta la comilla doble"),
    ("T14 · identificador con mayúscula",
     'Tempo 120', 1, 1,
     "Error léxico en línea 1, columna 1: identificador inválido 'Tempo', solo admite minúsculas"),
]
for nombre, entrada, linea, columna, mensaje in errores:
    try:
        paso14.tokenizar(entrada)
        real = "no lanzó error"
    except paso14.ErrorLexico as e:          # se atrapa con su propio nombre, no con Exception
        real = (e.linea, e.columna, str(e))
    revisar(nombre, entrada, (linea, columna, mensaje), real)

# Las entradas válidas de los 23 casos siguen dando los mismos tokens con paso14
validos = [(n, ent, esp) for n, ent, esp in casos_30oct if isinstance(esp, list)]
revisar("T14 · las entradas válidas no cambian",
        f"{len(validos)} casos válidos de pruebas_30oct.py",
        [esp for _, _, esp in validos],
        [[astuple(t) for t in paso14.tokenizar(ent)] for _, ent, _ in validos])


# ----- Tarea 15 · leer un archivo -----
def correr_main(archivo):
    r = subprocess.run([sys.executable, "main.py", archivo], cwd=COMPILADOR, capture_output=True,
                       encoding="utf-8", env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    return r.returncode, r.stdout, "Traceback" in r.stderr

revisar("T15 · archivo válido (programa.txt)",
        'python main.py programa.txt',
        (0, "LINEA  COL  TIPO           TEXTO\n"
            "1      1    IDENTIFICADOR  tempo\n"
            "1      7    NUMERO         120\n"
            "1      10   NL             \\n\n"
            "2      1    IDENTIFICADOR  volumen\n"
            "2      9    SIMBOLO        =\n"
            "2      11   NUMERO         5\n"
            "2      12   NL             \\n\n"
            "3      1    EOF\n", False),
        correr_main("programa.txt"))

revisar("T15 · archivo inválido (programa_invalido.txt), sin traza de Python",
        'python main.py programa_invalido.txt',
        (1, "Error léxico en línea 1, columna 11: carácter '@' no reconocido\n", False),
        correr_main("programa_invalido.txt"))


# ----- Tarea 16 · programa de ejemplo -----
sys.path.insert(0, COMPILADOR)               # el lexer.py de compilador/, no el de las tareas 1 a 3
import lexer as lexer_modular

revisar("T15 · un tabulador se descarta como un espacio (cuenta 1 columna)",
        '\\ttempo\\t120',
        [("IDENTIFICADOR", "tempo", 1, 2), ("NUMERO", "120", 1, 8), ("EOF", "", 1, 11)],
        [astuple(t) for t in lexer_modular.tokenizar('\ttempo\t120')])

ejemplo = open(os.path.join(COMPILADOR, "ejemplo.txt"), encoding="utf-8").read()
try:
    tokens = lexer_modular.tokenizar(ejemplo)
    error = None
except lexer_modular.ErrorLexico as e:
    tokens, error = [], str(e)
revisar("T16 · ejemplo.txt se tokeniza sin errores",
        f"ejemplo.txt ({ejemplo.count(chr(10))} líneas)", None, error)

revisar("T16 · las 3 primeras líneas calculadas a mano (la 1 es comentario: solo deja su NL)",
        "# programa de ejemplo\\ntempo 120\\numbral 0.75",
        [("NL", "\\n", 1, 22),
         ("IDENTIFICADOR", "tempo", 2, 1), ("NUMERO", "120", 2, 7), ("NL", "\\n", 2, 10),
         ("IDENTIFICADOR", "umbral", 3, 1), ("NUMERO", "0.75", 3, 8), ("NL", "\\n", 3, 12)],
        [astuple(t) for t in tokens if t.linea <= 3])

revisar("T16 · trae comentarios, decimales, cadenas, operadores, regla e impresión",
        "10 líneas o más, decimales, cadenas, operadores, comentario de bloque, regla e impresión",
        {"10 líneas o más": True, "decimal": True, "cadena": True, "operador": True,
         "comentario de bloque": True, "AL ... TOCAR": True, "mostrar": True},
        {"10 líneas o más": ejemplo.count("\n") >= 10,
         "decimal": any(t.tipo == "NUMERO" and "." in t.texto for t in tokens),
         "cadena": any(t.tipo == "TEXTO" for t in tokens),
         "operador": any(t.tipo == "OPERADOR" for t in tokens),
         "comentario de bloque": "/*" in ejemplo,
         "AL ... TOCAR": any(t.texto == "AL" for t in tokens) and any(t.texto == "TOCAR" for t in tokens),
         "mostrar": any(t.texto == "mostrar" for t in tokens)})

print(f"{aciertos} de {total} casos coinciden")
