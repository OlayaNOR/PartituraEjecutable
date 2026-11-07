# main.py · lee un archivo, lo pasa por el lexer y recorre los tokens con el Parser
# Uso: python main.py programa.txt
#      python main.py --tabla programa.txt   (la tabla de tokens de la tarea 15)

import sys
from lexer import tokenizar
from parser import Parser
from tokens import ErrorLexico


def mostrar_tabla(tokens):
    print(f"{'LINEA':<7}{'COL':<5}{'TIPO':<15}TEXTO")
    for t in tokens:
        # rstrip: el EOF no tiene texto y la fila no debe quedar con espacios al final
        print(f"{t.linea:<7}{t.columna:<5}{t.tipo:<15}{t.texto}".rstrip())


def recorrer(tokens):
    parser = Parser(tokens)
    while parser.actual().tipo != "EOF":
        print(parser.avanzar())           # Token.__str__: NUMERO('5') en 1:9
    print(parser.actual())                # el EOF también se imprime


if __name__ == "__main__":
    args = sys.argv[1:]
    tabla = "--tabla" in args
    if tabla:
        args.remove("--tabla")
    if len(args) != 1:
        print("Uso: python main.py [--tabla] <archivo>")
        sys.exit(2)
    ruta = args[0]
    try:
        texto = open(ruta, encoding="utf-8").read()
    except FileNotFoundError:
        print(f"No se encontró el archivo '{ruta}'")
        sys.exit(1)
    try:
        tokens = tokenizar(texto)
    except ErrorLexico as e:
        print(e)                                          # el mensaje completo
        print(f"linea = {e.linea}, columna = {e.columna}")  # la posición, leída por separado
        sys.exit(1)
    if tabla:
        mostrar_tabla(tokens)
    else:
        recorrer(tokens)
