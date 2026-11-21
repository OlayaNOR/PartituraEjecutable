# arbol.py · los nodos del árbol que arma el parser y la función que lo imprime
# Los nodos guardan tokens (no solo textos) para poder dar línea y columna si algo falla al ejecutar.

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


# ----- expresiones con hijos -----
@dataclass
class OperacionBinaria:      # tempo * 2
    izq: object
    operador: Token
    der: object


@dataclass
class Negativo:              # -5, -(x + 2)
    operador: Token
    valor: object


@dataclass
class Comparacion:           # n <= 5, compas = "4/4"
    izq: object
    operador: Token
    der: object


@dataclass
class Logica:                # a Y b, a O b
    izq: object
    operador: Token
    der: object


@dataclass
class Negacion:              # NO a
    operador: Token
    valor: object


# ----- instrucciones -----
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
class Si:                    # AL condición TOCAR { … } SINO { … }
    palabra: Token
    condicion: object
    entonces: list
    sino: object             # lista de instrucciones, o None si no hay SINO


@dataclass
class Mientras:              # repetir mientras condición { … }
    palabra: Token
    condicion: object
    cuerpo: list


@dataclass
class Repetir:               # repetir 3 { … }  ·  repetir 3 con vuelta { … }
    palabra: Token
    veces: object
    contador: object         # token del nombre del contador, o None
    cuerpo: list


@dataclass
class Programa:              # la raíz: todas las instrucciones del archivo
    instrucciones: list


def mostrar_arbol(nodo, nivel=0):
    """Imprime el árbol con dos espacios de sangría por nivel: los hijos van debajo del padre."""
    s = "  " * nivel

    def bloque(titulo, instrucciones):
        print(f"{s}  {titulo}")
        for instruccion in instrucciones:
            mostrar_arbol(instruccion, nivel + 2)

    if isinstance(nodo, Programa):
        print(f"{s}Programa")
        for instruccion in nodo.instrucciones:
            mostrar_arbol(instruccion, nivel + 1)
    elif isinstance(nodo, Declaracion):
        print(f"{s}Declaracion {nodo.nombre.texto}")
        mostrar_arbol(nodo.valor, nivel + 1)
    elif isinstance(nodo, Asignacion):
        print(f"{s}Asignacion {nodo.nombre.texto}")
        mostrar_arbol(nodo.valor, nivel + 1)
    elif isinstance(nodo, Mostrar):
        print(f"{s}Mostrar")
        mostrar_arbol(nodo.valor, nivel + 1)
    elif isinstance(nodo, Si):
        print(f"{s}Si")
        mostrar_arbol(nodo.condicion, nivel + 1)
        bloque("Entonces", nodo.entonces)
        if nodo.sino is not None:
            bloque("Sino", nodo.sino)
    elif isinstance(nodo, Mientras):
        print(f"{s}Mientras")
        mostrar_arbol(nodo.condicion, nivel + 1)
        bloque("Cuerpo", nodo.cuerpo)
    elif isinstance(nodo, Repetir):
        contador = f" con {nodo.contador.texto}" if nodo.contador else ""
        print(f"{s}Repetir{contador}")
        mostrar_arbol(nodo.veces, nivel + 1)
        bloque("Cuerpo", nodo.cuerpo)
    elif isinstance(nodo, (OperacionBinaria, Comparacion, Logica)):
        print(f"{s}{type(nodo).__name__} {nodo.operador.texto}")
        mostrar_arbol(nodo.izq, nivel + 1)
        mostrar_arbol(nodo.der, nivel + 1)
    elif isinstance(nodo, (Negativo, Negacion)):
        print(f"{s}{type(nodo).__name__} {nodo.operador.texto}")
        mostrar_arbol(nodo.valor, nivel + 1)
    elif isinstance(nodo, Numero):
        print(f"{s}Numero {nodo.token.texto}")
    elif isinstance(nodo, Cadena):
        print(f'{s}Cadena "{nodo.token.texto}"')
    elif isinstance(nodo, Booleano):
        print(f"{s}Booleano {nodo.token.texto}")
    elif isinstance(nodo, Variable):
        print(f"{s}Variable {nodo.token.texto}")
