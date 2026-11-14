# parser.py · el parser de TocaScript: lee los tokens en el orden de la gramática y arma el árbol
#
# Gramática (EBNF). ::= "está formado por" · | "o" · * "cero o más veces" · entre comillas, un token exacto;
# en mayúsculas, un tipo de token. En TocaScript el fin de instrucción es el salto de línea (NL), no el ';'.
#
#   programa    ::= ( instruccion | NL )* EOF
#   instruccion ::= declaracion | asignacion | salida
#   declaracion ::= IDENTIFICADOR expresion fin
#   asignacion  ::= IDENTIFICADOR '=' expresion fin
#   salida      ::= 'mostrar' expresion fin
#   fin         ::= NL | EOF
#   expresion   ::= termino ( ( '+' | '-' ) termino )*
#   termino     ::= factor ( ( '*' | '/' ) factor )*
#   factor      ::= NUMERO | TEXTO | BOOLEANO | IDENTIFICADOR | '(' expresion ')'
#
# declaracion y asignacion empiezan las dos con IDENTIFICADOR: se decide mirando el token siguiente.
# Si es '=', es una asignación (volumen = 80); si no, es una declaración (tempo 120).

from arbol import (Asignacion, Booleano, Cadena, Declaracion, Mostrar, Numero, OperacionBinaria,
                   Programa, Variable)
from tokens import ErrorSintactico


def describir(token):
    """Cómo se nombra en un mensaje de error el token que llegó."""
    if token.tipo == "EOF":
        return "el fin del archivo"
    if token.tipo == "NL":
        return "el fin de la línea"
    return f"'{token.texto}'"


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens              # la lista que devuelve el lexer, siempre termina en EOF
        self.pos = 0                      # en qué token va este parser

    # ----- moverse por los tokens -----
    def actual(self):
        """Devuelve el token actual sin moverse."""
        return self.tokens[self.pos]

    def siguiente(self):
        """Devuelve el token que viene después del actual, sin moverse (el EOF si ya no hay más)."""
        return self.tokens[min(self.pos + 1, len(self.tokens) - 1)]

    def avanzar(self):
        """Devuelve el token actual y pasa al siguiente. En EOF se queda quieto."""
        token = self.actual()
        if token.tipo != "EOF":
            self.pos += 1
        return token

    def esperar(self, tipo, texto=None):
        """Si el token actual es el que pide la regla, avanza y lo devuelve; si no, ErrorSintactico."""
        t = self.actual()
        if t.tipo != tipo or (texto is not None and t.texto != texto):
            quiero = f"'{texto}'" if texto else f"un {tipo}"
            raise ErrorSintactico(f"se esperaba {quiero} y llegó {describir(t)}", t.linea, t.columna)
        return self.avanzar()

    def es(self, tipo, texto):
        """¿El token actual es este tipo con este texto?"""
        t = self.actual()
        return t.tipo == tipo and t.texto == texto

    # ----- una regla, un método -----
    # programa ::= ( instruccion | NL )* EOF
    def programa(self):
        instrucciones = []
        while self.actual().tipo != "EOF":
            if self.actual().tipo == "NL":           # líneas vacías y de comentario
                self.avanzar()
            else:
                instrucciones.append(self.instruccion())
        return Programa(instrucciones)

    # instruccion ::= declaracion | asignacion | salida
    def instruccion(self):
        t = self.actual()
        if t.tipo == "RESERVADA" and t.texto == "mostrar":
            return self.salida()
        if t.tipo == "IDENTIFICADOR":
            siguiente = self.siguiente()
            if siguiente.tipo == "SIMBOLO" and siguiente.texto == "=":
                return self.asignacion()
            return self.declaracion()
        raise ErrorSintactico(f"se esperaba el inicio de una instrucción y llegó {describir(t)}",
                              t.linea, t.columna)

    # declaracion ::= IDENTIFICADOR expresion fin
    def declaracion(self):
        nombre = self.esperar("IDENTIFICADOR")      # IDENTIFICADOR
        valor = self.expresion()                    # expresion
        self.fin()                                  # fin
        return Declaracion(nombre, valor)

    # asignacion ::= IDENTIFICADOR '=' expresion fin
    def asignacion(self):
        nombre = self.esperar("IDENTIFICADOR")      # IDENTIFICADOR
        self.esperar("SIMBOLO", "=")                # '='
        valor = self.expresion()                    # expresion
        self.fin()                                  # fin
        return Asignacion(nombre, valor)

    # salida ::= 'mostrar' expresion fin
    def salida(self):
        palabra = self.esperar("RESERVADA", "mostrar")   # 'mostrar'
        valor = self.expresion()                         # expresion
        self.fin()                                       # fin
        return Mostrar(palabra, valor)

    # fin ::= NL | EOF
    def fin(self):
        t = self.actual()
        if t.tipo == "NL":
            self.avanzar()
        elif t.tipo != "EOF":                       # el EOF no se consume: lo necesita programa()
            raise ErrorSintactico(f"se esperaba el fin de la línea y llegó {describir(t)}",
                                  t.linea, t.columna)

    # expresion ::= termino ( ( '+' | '-' ) termino )*
    def expresion(self):
        izq = self.termino()                                    # termino
        while self.es("OPERADOR", "+") or self.es("OPERADOR", "-"):
            operador = self.avanzar()                           # '+' o '-'
            der = self.termino()                                # termino
            izq = OperacionBinaria(izq, operador, der)
        return izq

    # termino ::= factor ( ( '*' | '/' ) factor )*
    def termino(self):
        izq = self.factor()                                     # factor
        while self.es("OPERADOR", "*") or self.es("OPERADOR", "/"):
            operador = self.avanzar()                           # '*' o '/'
            der = self.factor()                                 # factor
            izq = OperacionBinaria(izq, operador, der)
        return izq

    # factor ::= NUMERO | TEXTO | BOOLEANO | IDENTIFICADOR | '(' expresion ')'
    def factor(self):
        t = self.actual()
        if t.tipo == "NUMERO":
            return Numero(self.avanzar())
        if t.tipo == "TEXTO":
            return Cadena(self.avanzar())
        if t.tipo == "BOOLEANO":
            return Booleano(self.avanzar())
        if t.tipo == "IDENTIFICADOR":
            return Variable(self.avanzar())
        if self.es("SIMBOLO", "("):
            self.avanzar()                          # '('
            dentro = self.expresion()               # expresion
            self.esperar("SIMBOLO", ")")            # ')'
            return dentro                           # el paréntesis no crea nodo: lo de adentro queda más abajo
        raise ErrorSintactico(f"se esperaba un número, una variable o '(' y llegó {describir(t)}",
                              t.linea, t.columna)
