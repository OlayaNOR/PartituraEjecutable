# arbol.py · los nodos del árbol que arma el parser y la función que lo imprime
# Los nodos guardan tokens (no solo textos) para poder dar línea y columna si algo falla después.

from dataclasses import dataclass

from tokens import Token


# ----- hojas: guardan un solo token -----
@dataclass
class Numero:                # 120, 0.75
    token: Token


@dataclass
class Cadena:                # "Do mayor"
    token: Token


@dataclass
class Booleano:              # true, false
    token: Token


@dataclass
class Variable:              # un nombre usado en una expresión: tempo
    token: Token


# ----- nodos con hijos -----
@dataclass
class OperacionBinaria:      # tempo * 2
    izq: object
    operador: Token
    der: object


@dataclass
class Declaracion:           # tempo 120
    nombre: Token
    valor: object


@dataclass
class Asignacion:            # volumen = tempo * 0.5 + 10
    nombre: Token
    valor: object


@dataclass
class Mostrar:               # mostrar tempo - 20
    palabra: Token
    valor: object


@dataclass
class Programa:              # la raíz: todas las instrucciones del archivo
    instrucciones: list


def mostrar_arbol(nodo, nivel=0):
    """Imprime el árbol con dos espacios de sangría por nivel: los hijos van debajo del padre."""
    sangria = "  " * nivel
    if isinstance(nodo, Programa):
        print(f"{sangria}Programa")
        for instruccion in nodo.instrucciones:
            mostrar_arbol(instruccion, nivel + 1)
    elif isinstance(nodo, Declaracion):
        print(f"{sangria}Declaracion {nodo.nombre.texto}")
        mostrar_arbol(nodo.valor, nivel + 1)
    elif isinstance(nodo, Asignacion):
        print(f"{sangria}Asignacion {nodo.nombre.texto}")
        mostrar_arbol(nodo.valor, nivel + 1)
    elif isinstance(nodo, Mostrar):
        print(f"{sangria}Mostrar")
        mostrar_arbol(nodo.valor, nivel + 1)
    elif isinstance(nodo, OperacionBinaria):
        print(f"{sangria}OperacionBinaria {nodo.operador.texto}")
        mostrar_arbol(nodo.izq, nivel + 1)
        mostrar_arbol(nodo.der, nivel + 1)
    elif isinstance(nodo, Numero):
        print(f"{sangria}Numero {nodo.token.texto}")
    elif isinstance(nodo, Cadena):
        print(f'{sangria}Cadena "{nodo.token.texto}"')
    elif isinstance(nodo, Booleano):
        print(f"{sangria}Booleano {nodo.token.texto}")
    elif isinstance(nodo, Variable):
        print(f"{sangria}Variable {nodo.token.texto}")
