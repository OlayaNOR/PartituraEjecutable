# paso13.py · Tarea 13: clase Token
# Cambio nuevo respecto a paso12.py: cada token es un objeto Token (tipo, texto, linea, columna) en vez de una tupla.

from dataclasses import dataclass, astuple

@dataclass
class Token:
    tipo: str
    texto: str
    linea: int
    columna: int

    def __str__(self):                    # NUMERO('5') en 1:9
        return f"{self.tipo}('{self.texto}') en {self.linea}:{self.columna}"


LETRAS = "abcdefghijklmnopqrstuvwxyz"
MAYUS = LETRAS.upper()
DIGITOS = "0123456789"

TIPOS = {"motivo", "acorde", "seccion", "tipo", "pieza", "voz", "simultaneo"}
LOGICOS = {"Y", "O", "NO"}
BOOLEANOS = {"true", "false"}
CONTROL = {"AL", "TOCAR",                # la regla: AL <condición> TOCAR <acciones>
           "repetir", "finales", "vez"}  # la repetición: repetir 4 { … } finales { vez 1 … }
RESERVADAS = {
    "mostrar",
    "tocar", "con", "silencio", "sin", "reglas", "exportar",
    "transportado", "invertido", "retrogradado", "semitonos", "velocidad",
    "en", "crescendo", "hasta", "durante",
    "intro", "estrofa", "estribillo", "coda",
    "redonda", "blanca", "negra", "corchea", "semicorchea", "fusa",
    "do", "re", "mi", "fa", "sol", "la", "si",
}

OPERADORES_LARGOS = [">=", "<=", "<>"]  # 2 caracteres: se revisan PRIMERO (si no, ">=" saldría como ">" y "=")
SIMBOLOS_1 = {"=",                       # 1 caracter (el "=" de asignación va aquí)
              "(", ")", "{", "}", "[", "]", ":", ",", "."}   # delimitadores
OPERADORES = {"+", "-", "*", "/",       # operadores aritméticos de un carácter
              "<", ">"}                 # relacionales de un carácter


def tokenizar(texto):
    tokens = []
    i = 0
    linea = 1
    inicio_linea = 0                      # posicion donde empieza la linea actual
    while i < len(texto):
        c = texto[i]
        columna = i - inicio_linea + 1    # columna donde empieza el token

        if c == " ":                      # el lexer descarta espacios
            i += 1

        elif c == "#" and (i == 0 or texto[i - 1] in " \n"):   # comentario (en fa#4 el # es sostenido)
            while i < len(texto) and texto[i] != "\n":
                i += 1                    # se lee y no se guarda; el \n queda para contar la linea

        elif texto.startswith("/*", i):   # comentario de bloque
            linea_comentario = linea      # se guarda: linea cambia si el comentario cruza saltos
            i += 2
            while i < len(texto) and not texto.startswith("*/", i):
                if texto[i] == "\n":      # el salto dentro del comentario cuenta la línea, sin token NL
                    linea += 1
                    inicio_linea = i + 1
                i += 1
            if i >= len(texto):           # el error se reporta donde EMPEZÓ el comentario
                raise SyntaxError(f"Línea {linea_comentario}, columna {columna}: comentario sin cerrar")
            i += 2                        # salta el */

        elif c == "\n":                   # <nl> es un terminal
            tokens.append(Token("NL", "\\n", linea, columna))
            i += 1
            linea += 1                    # la columna vuelve a 1
            inicio_linea = i

        elif c in LETRAS or c in MAYUS:   # palabra: tipo, reservada, booleano o identificador
            inicio = i
            while i < len(texto) and (texto[i] in LETRAS or texto[i] in MAYUS
                                      or texto[i] in DIGITOS
                                      or texto[i] == "_"):
                i += 1
            palabra = texto[inicio:i]     # la palabra se lee COMPLETA antes de comparar

            if palabra in BOOLEANOS:
                tokens.append(Token("BOOLEANO", palabra, linea, columna))
            elif palabra in TIPOS:
                tokens.append(Token("TIPO", palabra, linea, columna))
            elif palabra in LOGICOS:
                tokens.append(Token("OPERADOR", palabra, linea, columna))
            elif palabra in CONTROL:
                tokens.append(Token("RESERVADA", palabra, linea, columna))
            elif palabra in RESERVADAS:
                tokens.append(Token("RESERVADA", palabra, linea, columna))
            elif any(ch in MAYUS for ch in palabra):
                # <identificador> solo admite minúsculas, dígitos y "_"
                raise SyntaxError(f"Línea {linea}, columna {columna}: identificador inválido '{palabra}', solo admite minúsculas")
            else:
                tokens.append(Token("IDENTIFICADOR", palabra, linea, columna))

        elif c in DIGITOS:                # <numero>: dígitos [ "." dígitos ]
            inicio = i
            while i < len(texto) and texto[i] in DIGITOS:
                i += 1
            if i < len(texto) and texto[i] == ".":
                i += 1
                if i >= len(texto) or texto[i] not in DIGITOS:
                    raise SyntaxError(f"Línea {linea}, columna {columna}: número mal formado, falta un dígito después del '.'")
                while i < len(texto) and texto[i] in DIGITOS:
                    i += 1
                if i < len(texto) and texto[i] == ".":   # un decimal lleva un solo punto
                    raise SyntaxError(f"Línea {linea}, columna {columna}: número mal formado, tiene más de un punto")
            tokens.append(Token("NUMERO", texto[inicio:i], linea, columna))

        elif c == '"':                    # <texto>
            i += 1
            inicio = i
            while i < len(texto) and texto[i] != '"' and texto[i] != "\n":   # el texto no pasa de línea
                if texto[i] not in LETRAS + MAYUS + DIGITOS + " /":
                    raise SyntaxError(f"Línea {linea}, columna {i - inicio_linea + 1}: carácter inesperado '{texto[i]}' dentro del texto")
                i += 1
            if i >= len(texto) or texto[i] == "\n":
                raise SyntaxError(f"Línea {linea}, columna {columna}: texto sin cerrar, falta la comilla doble")
            tokens.append(Token("TEXTO", texto[inicio:i], linea, columna))
            i += 1                        # salta la comilla de cierre

        elif any(texto.startswith(s, i) for s in OPERADORES_LARGOS):
            for s in OPERADORES_LARGOS:
                if texto.startswith(s, i):
                    tokens.append(Token("OPERADOR", s, linea, columna))
                    i += len(s)           # avanza tantas posiciones como mida el operador
                    break

        elif c in SIMBOLOS_1:             # el "." llega aquí solo si no va dentro de un número
            tokens.append(Token("SIMBOLO", c, linea, columna))
            i += 1

        elif c in OPERADORES:
            tokens.append(Token("OPERADOR", c, linea, columna))
            i += 1

        else:
            raise SyntaxError(f"Línea {linea}, columna {columna}: carácter inesperado '{c}'")

    tokens.append(Token("EOF", "", linea, i - inicio_linea + 1))   # posición final; el texto vacío da 1, 1
    return tokens



if __name__ == "__main__":
    pruebas = ['volumen = 5',
               'tempo 120\ncompas "4/4"']
    for texto in pruebas:
        print(repr(texto))
        try:
            for token in tokenizar(texto):
                print("  ", token)        # print usa __str__
        except SyntaxError as e:
            print("   ERROR:", e)
    t = tokenizar("volumen = 5")[2]
    print("t.tipo =", t.tipo, "· t.columna =", t.columna, "· como tupla:", astuple(t))
