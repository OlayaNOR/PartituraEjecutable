# tokens.py · Tareas 13 y 14: clases Token y ErrorLexico

from dataclasses import dataclass


@dataclass
class Token:
    tipo: str
    texto: str
    linea: int
    columna: int

    def __str__(self):                    # NUMERO('5') en 1:9
        return f"{self.tipo}('{self.texto}') en {self.linea}:{self.columna}"


class ErrorLexico(Exception):
    def __init__(self, mensaje, linea, columna):
        super().__init__(f"Error léxico en línea {linea}, columna {columna}: {mensaje}")
        self.mensaje = mensaje            # solo la causa, sin la posición
        self.linea = linea
        self.columna = columna
