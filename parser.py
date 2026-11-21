# parser.py · el parser de TocaScript: lee los tokens en el orden de la gramática y arma el árbol
#
# Gramática final (EBNF). ::= "está formado por" · | "o" · * "cero o más veces" · ? "cero o una vez" ·
# entre comillas, un token exacto; en mayúsculas, un tipo de token. El fin de instrucción es el salto de línea (NL).
#
#   programa    ::= ( instruccion | NL )* EOF
#   instruccion ::= declaracion | asignacion | salida | condicional | ciclo | repeticion
#   declaracion ::= IDENTIFICADOR condicion fin
#   asignacion  ::= IDENTIFICADOR '=' condicion fin
#   salida      ::= 'mostrar' condicion fin
#   condicional ::= 'AL' condicion 'TOCAR' bloque ( 'SINO' bloque )? fin
#   ciclo       ::= 'repetir' 'mientras' condicion bloque fin
#   repeticion  ::= 'repetir' expresion ( 'con' IDENTIFICADOR )? bloque fin
#   bloque      ::= '{' ( instruccion | NL )* '}'
#   fin         ::= NL | EOF                      (antes de un '}' la instrucción también puede terminar)
#   condicion   ::= conjuncion ( 'O' conjuncion )*
#   conjuncion  ::= negacion ( 'Y' negacion )*
#   negacion    ::= 'NO' negacion | comparacion
#   comparacion ::= expresion ( ( COMPARADOR | '=' ) expresion )?
#   expresion   ::= termino ( ( '+' | '-' ) termino )*
#   termino     ::= factor ( ( '*' | '/' ) factor )*
#   factor      ::= '-' factor | NUMERO | TEXTO | BOOLEANO | IDENTIFICADOR | '(' condicion ')'
#
# declaracion y asignacion empiezan con IDENTIFICADOR: si el token siguiente es '=', es asignación.
# Dentro de una condición, '=' compara (tempo = 120); como instrucción, asigna (tempo = 120).

from arbol import (Asignacion, Booleano, Cadena, Comparacion, Declaracion, Logica, Mientras, Mostrar,
                   Negacion, Negativo, Numero, OperacionBinaria, Programa, Repetir, Si, Variable)
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
        return self.tokens[self.pos]

    def siguiente(self):
        """El token que viene después del actual, sin moverse (el EOF si ya no hay más)."""
        return self.tokens[min(self.pos + 1, len(self.tokens) - 1)]

    def avanzar(self):
        """Devuelve el token actual y pasa al siguiente. En EOF se queda quieto."""
        token = self.actual()
        if token.tipo != "EOF":
            self.pos += 1
        return token

    def es(self, tipo, texto=None):
        t = self.actual()
        return t.tipo == tipo and (texto is None or t.texto == texto)

    def esperar(self, tipo, texto=None):
        """Si el token actual es el que pide la regla, avanza y lo devuelve; si no, ErrorSintactico."""
        t = self.actual()
        if t.tipo != tipo or (texto is not None and t.texto != texto):
            quiero = f"'{texto}'" if texto else f"un {tipo}"
            raise ErrorSintactico(f"se esperaba {quiero} y llegó {describir(t)}", t.linea, t.columna)
        return self.avanzar()

    # ----- programa e instrucciones -----
    # programa ::= ( instruccion | NL )* EOF
    def programa(self):
        instrucciones = []
        while not self.es("EOF"):
            if self.es("NL"):
                self.avanzar()
            else:
                instrucciones.append(self.instruccion())
        return Programa(instrucciones)

    # instruccion ::= declaracion | asignacion | salida | condicional | ciclo | repeticion
    def instruccion(self):
        t = self.actual()
        if self.es("RESERVADA", "mostrar"):
            return self.salida()
        if self.es("RESERVADA", "AL"):
            return self.condicional()
        if self.es("RESERVADA", "repetir"):
            siguiente = self.siguiente()
            if siguiente.tipo == "RESERVADA" and siguiente.texto == "mientras":
                return self.ciclo()
            return self.repeticion()
        if t.tipo == "IDENTIFICADOR":
            siguiente = self.siguiente()
            if siguiente.tipo == "SIMBOLO" and siguiente.texto == "=":
                return self.asignacion()
            return self.declaracion()
        raise ErrorSintactico(f"se esperaba el inicio de una instrucción y llegó {describir(t)}",
                              t.linea, t.columna)

    # declaracion ::= IDENTIFICADOR condicion fin
    def declaracion(self):
        nombre = self.esperar("IDENTIFICADOR")
        valor = self.condicion()
        self.fin()
        return Declaracion(nombre, valor)

    # asignacion ::= IDENTIFICADOR '=' condicion fin
    def asignacion(self):
        nombre = self.esperar("IDENTIFICADOR")
        self.esperar("SIMBOLO", "=")
        valor = self.condicion()
        self.fin()
        return Asignacion(nombre, valor)

    # salida ::= 'mostrar' condicion fin
    def salida(self):
        palabra = self.esperar("RESERVADA", "mostrar")
        valor = self.condicion()
        self.fin()
        return Mostrar(palabra, valor)

    # condicional ::= 'AL' condicion 'TOCAR' bloque ( 'SINO' bloque )? fin
    def condicional(self):
        palabra = self.esperar("RESERVADA", "AL")
        condicion = self.condicion()
        self.esperar("RESERVADA", "TOCAR")
        entonces = self.bloque()
        sino = None
        if self.viene_sino():                     # el SINO es opcional: se pregunta, no se espera
            self.esperar("RESERVADA", "SINO")
            sino = self.bloque()
        self.fin()
        return Si(palabra, condicion, entonces, sino)

    def viene_sino(self):
        """¿Después de la llave viene SINO? Puede estar en la misma línea o en la siguiente."""
        p = self.pos
        while self.tokens[p].tipo == "NL":
            p += 1
        t = self.tokens[p]
        if t.tipo == "RESERVADA" and t.texto == "SINO":
            self.pos = p                          # se saltan los saltos de línea antes del SINO
            return True
        return False

    # ciclo ::= 'repetir' 'mientras' condicion bloque fin
    def ciclo(self):
        palabra = self.esperar("RESERVADA", "repetir")
        self.esperar("RESERVADA", "mientras")
        condicion = self.condicion()
        cuerpo = self.bloque()
        self.fin()
        return Mientras(palabra, condicion, cuerpo)

    # repeticion ::= 'repetir' expresion ( 'con' IDENTIFICADOR )? bloque fin
    def repeticion(self):
        palabra = self.esperar("RESERVADA", "repetir")
        veces = self.expresion()
        contador = None
        if self.es("RESERVADA", "con"):
            self.avanzar()
            contador = self.esperar("IDENTIFICADOR")
        cuerpo = self.bloque()
        self.fin()
        return Repetir(palabra, veces, contador, cuerpo)

    # bloque ::= '{' ( instruccion | NL )* '}'
    def bloque(self):
        llave = self.esperar("SIMBOLO", "{")
        instrucciones = []
        while not self.es("SIMBOLO", "}"):
            if self.es("EOF"):
                t = self.actual()
                raise ErrorSintactico(f"falta '}}' para cerrar el bloque abierto en la línea {llave.linea}",
                                      t.linea, t.columna)
            if self.es("NL"):
                self.avanzar()
            else:
                instrucciones.append(self.instruccion())
        self.avanzar()                            # '}'
        return instrucciones

    # fin ::= NL | EOF   (o el '}' que cierra el bloque, que no se consume aquí)
    def fin(self):
        if self.es("NL"):
            self.avanzar()
        elif not (self.es("EOF") or self.es("SIMBOLO", "}")):
            t = self.actual()
            raise ErrorSintactico(f"se esperaba el fin de la línea y llegó {describir(t)}", t.linea, t.columna)

    # ----- condiciones: O está por debajo de Y, Y por debajo de NO y NO por debajo de la comparación -----
    # condicion ::= conjuncion ( 'O' conjuncion )*
    def condicion(self):
        izq = self.conjuncion()
        while self.es("LOGICO", "O"):
            operador = self.avanzar()
            izq = Logica(izq, operador, self.conjuncion())
        return izq

    # conjuncion ::= negacion ( 'Y' negacion )*
    def conjuncion(self):
        izq = self.negacion()
        while self.es("LOGICO", "Y"):
            operador = self.avanzar()
            izq = Logica(izq, operador, self.negacion())
        return izq

    # negacion ::= 'NO' negacion | comparacion
    def negacion(self):
        if self.es("LOGICO", "NO"):
            operador = self.avanzar()
            return Negacion(operador, self.negacion())
        return self.comparacion()

    # comparacion ::= expresion ( ( COMPARADOR | '=' ) expresion )?
    def comparacion(self):
        izq = self.expresion()
        if self.es("COMPARADOR") or self.es("SIMBOLO", "="):
            operador = self.avanzar()
            return Comparacion(izq, operador, self.expresion())
        return izq

    # ----- aritmética -----
    # expresion ::= termino ( ( '+' | '-' ) termino )*
    def expresion(self):
        izq = self.termino()
        while self.es("OPERADOR", "+") or self.es("OPERADOR", "-"):
            operador = self.avanzar()
            izq = OperacionBinaria(izq, operador, self.termino())
        return izq

    # termino ::= factor ( ( '*' | '/' ) factor )*
    def termino(self):
        izq = self.factor()
        while self.es("OPERADOR", "*") or self.es("OPERADOR", "/"):
            operador = self.avanzar()
            izq = OperacionBinaria(izq, operador, self.factor())
        return izq

    # factor ::= '-' factor | NUMERO | TEXTO | BOOLEANO | IDENTIFICADOR | '(' condicion ')'
    def factor(self):
        t = self.actual()
        if self.es("OPERADOR", "-"):              # menos unario: -5, -(x + 2)
            operador = self.avanzar()
            return Negativo(operador, self.factor())
        if t.tipo == "NUMERO":
            return Numero(self.avanzar())
        if t.tipo == "TEXTO":
            return Cadena(self.avanzar())
        if t.tipo == "BOOLEANO":
            return Booleano(self.avanzar())
        if t.tipo == "IDENTIFICADOR":
            return Variable(self.avanzar())
        if self.es("SIMBOLO", "("):
            self.avanzar()
            dentro = self.condicion()
            self.esperar("SIMBOLO", ")")
            return dentro                         # el paréntesis no crea nodo: lo de adentro queda más abajo
        raise ErrorSintactico(f"se esperaba un número, una variable o '(' y llegó {describir(t)}",
                              t.linea, t.columna)
