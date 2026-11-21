# main.py · ejecuta un programa de TocaScript: lexer → parser → intérprete
# Uso: python main.py programa.txt
#      python main.py --arbol programa.txt    (muestra el árbol en vez de ejecutar)
#      python main.py --tokens programa.txt   (muestra los tokens)

import sys

from arbol import mostrar_arbol
from interprete import Interprete
from lexer import tokenizar
from parser import Parser
from tokens import ErrorDeLenguaje


def senalar(codigo, linea, columna):
    """La línea del programa donde está el error y un ^ debajo de la columna."""
    lineas = codigo.split("\n")
    texto = lineas[linea - 1] if 1 <= linea <= len(lineas) else ""
    texto = texto.replace("\t", " ").rstrip("\r")    # el tabulador cuenta una columna, como en el lexer
    return f"    {texto}\n    {' ' * (columna - 1)}^"


def main():
    args = sys.argv[1:]
    modo = "ejecutar"
    for opcion in ("--arbol", "--tokens"):
        if opcion in args:
            args.remove(opcion)
            modo = opcion[2:]
    if len(args) != 1:
        print("Uso: python main.py [--arbol | --tokens] <archivo>")
        sys.exit(2)
    try:
        with open(args[0], encoding="utf-8") as archivo:
            codigo = archivo.read()
    except FileNotFoundError:
        print(f"No se encontró el archivo '{args[0]}'")
        sys.exit(1)

    try:
        tokens = tokenizar(codigo)
        if modo == "tokens":
            for token in tokens:
                print(token)
            return
        programa = Parser(tokens).programa()
        if modo == "arbol":
            mostrar_arbol(programa)
        else:
            Interprete().ejecutar_programa(programa)
    except ErrorDeLenguaje as e:          # un solo except atrapa el error léxico, el sintáctico y el semántico
        sys.stdout.flush()
        print(e)
        print(senalar(codigo, e.linea, e.columna))
        print(f"linea = {e.linea}, columna = {e.columna}")
        sys.exit(1)


if __name__ == "__main__":
    main()
