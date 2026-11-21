# interprete.py · recorre el árbol y ejecuta el programa: guarda variables, hace las cuentas y muestra resultados
#
# Tipos de TocaScript. Una variable no se declara con tipo: lo toma de su primer valor y ya no lo cambia.
#   entero   (int)    120         decimal  (float)  0.75
#   texto    (str)    "4/4"       booleano (bool)   true / false

from arbol import (Asignacion, Booleano, Cadena, Comparacion, Declaracion, Logica, Mientras, Mostrar,
                   Negacion, Negativo, Numero, OperacionBinaria, Repetir, Si, Variable)
from tokens import ErrorSemantico

LIMITE_VUELTAS = 100_000

# qué tipos de Python acepta cada tipo de TocaScript. Se usa type() y no isinstance(), porque en Python
# True cuenta como entero y un booleano no debe caber en una variable entera.
ACEPTA = {"entero": (int,), "decimal": (int, float), "texto": (str,), "booleano": (bool,)}
ARTICULO = {"entero": "un entero", "decimal": "un decimal", "texto": "un texto", "booleano": "un booleano"}


def tipo_de(valor):
    if type(valor) is bool:
        return "booleano"
    if type(valor) is int:
        return "entero"
    if type(valor) is float:
        return "decimal"
    return "texto"


def es_numero(valor):
    return type(valor) in (int, float)


def como_texto(valor):
    """Cómo se ve un valor al mostrarlo o al unirlo con un texto."""
    if type(valor) is bool:
        return "true" if valor else "false"
    return str(valor)


class Entorno:
    """Las variables de un bloque. Si un nombre no está aquí, se busca en el entorno de afuera (padre)."""

    def __init__(self, padre=None):
        self.variables = {}
        self.padre = padre

    def buscar(self, nombre):
        entorno = self
        while entorno is not None:
            if nombre in entorno.variables:
                return entorno.variables[nombre]
            entorno = entorno.padre
        return None

    def definir(self, nombre, tipo, valor, linea):
        self.variables[nombre] = {"tipo": tipo, "valor": valor, "linea": linea}


class Interprete:
    def __init__(self, salida=print):
        self.entorno = Entorno()          # el entorno global; cada bloque abre uno nuevo con este como padre
        self.salida = salida

    def ejecutar_programa(self, programa):
        for instruccion in programa.instrucciones:
            self.ejecutar(instruccion)

    # ----- instrucciones: cambian el entorno o muestran algo, no devuelven nada -----
    def ejecutar(self, nodo):
        if isinstance(nodo, Declaracion):
            nombre = nodo.nombre
            existente = self.entorno.variables.get(nombre.texto)     # solo en el bloque actual
            if existente is not None:
                raise ErrorSemantico(f"la variable '{nombre.texto}' ya fue declarada en la línea {existente['linea']}",
                                     nombre.linea, nombre.columna)
            valor = self.evaluar(nodo.valor)
            self.entorno.definir(nombre.texto, tipo_de(valor), valor, nombre.linea)

        elif isinstance(nodo, Asignacion):
            nombre = nodo.nombre
            variable = self.entorno.buscar(nombre.texto)
            if variable is None:
                raise ErrorSemantico(f"la variable '{nombre.texto}' no ha sido declarada", nombre.linea, nombre.columna)
            valor = self.evaluar(nodo.valor)
            if type(valor) not in ACEPTA[variable["tipo"]]:
                raise ErrorSemantico(f"no se puede guardar {ARTICULO[tipo_de(valor)]} en la variable "
                                     f"'{nombre.texto}' de tipo {variable['tipo']}", nombre.linea, nombre.columna)
            variable["valor"] = float(valor) if variable["tipo"] == "decimal" else valor

        elif isinstance(nodo, Mostrar):
            self.salida(como_texto(self.evaluar(nodo.valor)))

        elif isinstance(nodo, Si):
            if self.condicion(nodo.condicion, nodo.palabra):
                self.ejecutar_bloque(nodo.entonces)
            elif nodo.sino is not None:
                self.ejecutar_bloque(nodo.sino)

        elif isinstance(nodo, Mientras):
            vueltas = 0
            while self.condicion(nodo.condicion, nodo.palabra):
                vueltas += 1
                if vueltas > LIMITE_VUELTAS:
                    raise ErrorSemantico(f"el ciclo superó {LIMITE_VUELTAS} vueltas; "
                                         "¿falta actualizar la variable de la condición?",
                                         nodo.palabra.linea, nodo.palabra.columna)
                self.ejecutar_bloque(nodo.cuerpo)

        elif isinstance(nodo, Repetir):
            veces = self.evaluar(nodo.veces)
            if type(veces) is not int or veces < 0:
                raise ErrorSemantico("repetir necesita un número entero de veces, cero o más",
                                     nodo.palabra.linea, nodo.palabra.columna)
            if veces > LIMITE_VUELTAS:
                raise ErrorSemantico(f"el ciclo superó {LIMITE_VUELTAS} vueltas",
                                     nodo.palabra.linea, nodo.palabra.columna)
            for vuelta in range(1, veces + 1):
                contador = None
                if nodo.contador is not None:      # repetir 3 con vuelta { … }: vuelta vale 1, 2 y 3
                    contador = (nodo.contador.texto, vuelta, nodo.contador.linea)
                self.ejecutar_bloque(nodo.cuerpo, contador)

    def ejecutar_bloque(self, instrucciones, contador=None):
        """Un bloque tiene su propio entorno: lo que se declara adentro deja de existir al cerrar la llave."""
        anterior = self.entorno
        self.entorno = Entorno(padre=anterior)
        if contador is not None:
            nombre, valor, linea = contador
            self.entorno.definir(nombre, "entero", valor, linea)
        try:
            for instruccion in instrucciones:
                self.ejecutar(instruccion)
        finally:
            self.entorno = anterior

    def condicion(self, nodo, palabra):
        valor = self.evaluar(nodo)
        if type(valor) is not bool:
            raise ErrorSemantico(f"la condición de {palabra.texto} debe dar true o false",
                                 palabra.linea, palabra.columna)
        return valor

    # ----- expresiones: devuelven un valor -----
    def evaluar(self, nodo):
        if isinstance(nodo, Numero):
            texto = nodo.token.texto
            return float(texto) if "." in texto else int(texto)
        if isinstance(nodo, Cadena):
            return nodo.token.texto
        if isinstance(nodo, Booleano):
            return nodo.token.texto == "true"
        if isinstance(nodo, Variable):
            variable = self.entorno.buscar(nodo.token.texto)
            if variable is None:
                raise ErrorSemantico(f"la variable '{nodo.token.texto}' no ha sido declarada",
                                     nodo.token.linea, nodo.token.columna)
            return variable["valor"]
        if isinstance(nodo, OperacionBinaria):
            izq = self.evaluar(nodo.izq)               # primero los dos hijos: lo de abajo se calcula antes
            der = self.evaluar(nodo.der)
            return self.operar(izq, nodo.operador, der)
        if isinstance(nodo, Negativo):
            valor = self.evaluar(nodo.valor)
            if not es_numero(valor):
                raise ErrorSemantico("el menos solo se usa con números", nodo.operador.linea, nodo.operador.columna)
            return -valor
        if isinstance(nodo, Comparacion):
            return self.comparar(self.evaluar(nodo.izq), nodo.operador, self.evaluar(nodo.der))
        if isinstance(nodo, Logica):
            izq = self.booleano(self.evaluar(nodo.izq), nodo.operador)
            if nodo.operador.texto == "Y" and not izq:
                return False                           # con Y, si el primero es false ya no hace falta el segundo
            if nodo.operador.texto == "O" and izq:
                return True
            return self.booleano(self.evaluar(nodo.der), nodo.operador)
        if isinstance(nodo, Negacion):
            return not self.booleano(self.evaluar(nodo.valor), nodo.operador)
        raise TypeError(f"nodo desconocido: {type(nodo).__name__}")

    def booleano(self, valor, operador):
        if type(valor) is not bool:
            raise ErrorSemantico(f"'{operador.texto}' solo se usa con true o false", operador.linea, operador.columna)
        return valor

    def operar(self, izq, operador, der):
        """Las reglas de las operaciones entre tipos (están también en el README)."""
        op = operador.texto
        if type(izq) is bool or type(der) is bool:
            raise ErrorSemantico(f"no se puede usar '{op}' con booleanos", operador.linea, operador.columna)
        if isinstance(izq, str) or isinstance(der, str):
            if op == "+":                              # unir: texto + texto, texto + número o número + texto
                return como_texto(izq) + como_texto(der)
            raise ErrorSemantico(f"no se puede usar '{op}' con textos", operador.linea, operador.columna)
        if op == "+":
            return izq + der
        if op == "-":
            return izq - der
        if op == "*":
            return izq * der
        if der == 0:
            raise ErrorSemantico("división por cero", operador.linea, operador.columna)
        if type(izq) is int and type(der) is int:      # entero / entero = división entera, se corta hacia cero
            cociente = abs(izq) // abs(der)
            return cociente if (izq < 0) == (der < 0) else -cociente
        return izq / der

    def comparar(self, izq, operador, der):
        op = operador.texto
        if op in ("=", "<>"):
            mismo_tipo = (es_numero(izq) and es_numero(der)) or type(izq) is type(der)
            if not mismo_tipo:
                raise ErrorSemantico(f"no se puede comparar {ARTICULO[tipo_de(izq)]} con {ARTICULO[tipo_de(der)]}",
                                     operador.linea, operador.columna)
            return izq == der if op == "=" else izq != der
        if not (es_numero(izq) and es_numero(der)):
            raise ErrorSemantico(f"'{op}' solo compara números", operador.linea, operador.columna)
        if op == "<":
            return izq < der
        if op == ">":
            return izq > der
        if op == "<=":
            return izq <= der
        return izq >= der
