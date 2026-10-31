# main.py · Tarea 15: lee un archivo y muestra la tabla de tokens
# Uso: python main.py ejemplo.txt

import sys
from lexer import tokenizar
from tokens import ErrorLexico


def mostrar_tabla(tokens):
    print(f"{'LINEA':<7}{'COL':<5}{'TIPO':<15}TEXTO")
    for t in tokens:
        # rstrip: el EOF no tiene texto y la fila no debe quedar con espacios al final
        print(f"{t.linea:<7}{t.columna:<5}{t.tipo:<15}{t.texto}".rstrip())


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python main.py <archivo>")
        sys.exit(2)
    ruta = sys.argv[1]
    try:
        texto = open(ruta, encoding="utf-8").read()
    except FileNotFoundError:
        print(f"No se encontró el archivo '{ruta}'")
        sys.exit(1)
    try:
        tokens = tokenizar(texto)
    except ErrorLexico as e:
        print(e)                          # solo el mensaje: Error léxico en línea L, columna C: ...
        sys.exit(1)
    mostrar_tabla(tokens)
