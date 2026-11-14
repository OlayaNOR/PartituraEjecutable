# main.py · lee un programa de TocaScript, lo pasa por el lexer y el parser e imprime el árbol
# Uso: python main.py programa.txt
#      python main.py --tokens programa.txt   (recorre los tokens con el Parser, como el 7 de noviembre)
#      python main.py --tabla programa.txt    (la tabla de tokens de la tarea 15)

import sys
from arbol import mostrar_arbol
from lexer import tokenizar
from parser import Parser
from tokens import ErrorDeLenguaje


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


def main():
    args = sys.argv[1:]
    modo = "arbol"
    for opcion in ("--tokens", "--tabla"):
        if opcion in args:
            args.remove(opcion)
            modo = opcion[2:]
    if len(args) != 1:
        print("Uso: python main.py [--tokens | --tabla] <archivo>")
        sys.exit(2)
    ruta = args[0]
    try:
        with open(ruta, encoding="utf-8") as archivo:
            codigo = archivo.read()
    except FileNotFoundError:
        print(f"No se encontró el archivo '{ruta}'")
        sys.exit(1)
    try:
        tokens = tokenizar(codigo)
        if modo == "tabla":
            mostrar_tabla(tokens)
        elif modo == "tokens":
            recorrer(tokens)
        else:
            programa = Parser(tokens).programa()
            mostrar_arbol(programa)
    except ErrorDeLenguaje as e:          # atrapa el léxico y el sintáctico: los dos heredan de ErrorDeLenguaje
        print(e)                                            # el mensaje completo
        print(f"linea = {e.linea}, columna = {e.columna}")  # la posición, leída por separado
        sys.exit(1)


if __name__ == "__main__":
    main()
