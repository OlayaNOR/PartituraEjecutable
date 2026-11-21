# tokens.py · la clase Token y los errores de cada fase (léxico, sintáctico y semántico)

from dataclasses import dataclass


@dataclass
class Token:
    tipo: str
    texto: str
    linea: int
    columna: int

    def __str__(self):                    # NUMERO('5') en 1:9
        return f"{self.tipo}('{self.texto}') en {self.linea}:{self.columna}"


class ErrorDeLenguaje(Exception):
    """Lo que comparten todos los errores: mensaje, línea y columna. Cada fase solo cambia su nombre."""
    fase = "Error"

    def __init__(self, mensaje, linea, columna):
        self.mensaje = mensaje
        self.linea = linea
        self.columna = columna
        super().__init__(f"{self.fase} en línea {linea}, columna {columna}: {mensaje}")


class ErrorLexico(ErrorDeLenguaje):
    fase = "Error léxico"


class ErrorSintactico(ErrorDeLenguaje):
    fase = "Error sintáctico"


class ErrorSemantico(ErrorDeLenguaje):
    fase = "Error semántico"
