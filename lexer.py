# lexer.py · convierte el texto de un programa TocaScript en una lista de tokens con línea y columna

from tokens import Token, ErrorLexico

LETRAS = "abcdefghijklmnopqrstuvwxyz"
MAYUS = LETRAS.upper()
DIGITOS = "0123456789"
# dentro de un texto entre comillas también valen tildes, eñe y signos de puntuación
EXTRA_TEXTO = "áéíóúüñÁÉÍÓÚÜÑ .,:;!?¿¡/-"

TIPOS = {"motivo", "acorde", "seccion", "tipo", "pieza", "voz", "simultaneo"}
LOGICOS = {"Y", "O", "NO"}
BOOLEANOS = {"true", "false"}
CONTROL = {"AL", "TOCAR", "SINO",        # condicional: AL <condición> TOCAR { … } SINO { … }
           "repetir", "mientras",        # ciclos: repetir mientras <condición> { … }  ·  repetir 3 { … }
           "finales", "vez"}
RESERVADAS = {
    "mostrar",
    "tocar", "con", "silencio", "sin", "reglas", "exportar",
    "transportado", "invertido", "retrogradado", "semitonos", "velocidad",
    "en", "crescendo", "hasta", "durante",
    "intro", "estrofa", "estribillo", "coda",
    "redonda", "blanca", "negra", "corchea", "semicorchea", "fusa",
    "do", "re", "mi", "fa", "sol", "la", "si",
}

COMPARADORES = [">=", "<=", "<>", "<", ">"]   # los de dos caracteres primero: si no, ">=" saldría como ">" y "="
SIMBOLOS = {"=", "(", ")", "{", "}", "[", "]", ":", ",", "."}   # el "=" asigna y, dentro de una condición, compara
OPERADORES = {"+", "-", "*", "/"}


def tokenizar(texto):
    tokens = []
    i = 0
    linea = 1
    inicio_linea = 0                      # posición donde empieza la línea actual
    while i < len(texto):
        c = texto[i]
        columna = i - inicio_linea + 1    # columna donde empieza el token

        if c == " " or c == "\t" or c == "\r":
            i += 1

        elif c == "#" and (i == 0 or texto[i - 1] in " \t\n"):   # comentario de línea (en fa#4 el # es sostenido)
            while i < len(texto) and texto[i] != "\n":
                i += 1

        elif texto.startswith("/*", i):   # comentario de bloque
            linea_comentario = linea
            i += 2
            while i < len(texto) and not texto.startswith("*/", i):
                if texto[i] == "\n":      # el salto dentro del comentario cuenta la línea, sin token NL
                    linea += 1
                    inicio_linea = i + 1
                i += 1
            if i >= len(texto):           # el error se reporta donde empezó el comentario
                raise ErrorLexico("comentario sin cerrar", linea_comentario, columna)
            i += 2

        elif c == "\n":                   # el salto de línea es el fin de instrucción
            tokens.append(Token("NL", "\\n", linea, columna))
            i += 1
            linea += 1
            inicio_linea = i

        elif c in LETRAS or c in MAYUS:   # palabra: se lee completa antes de compararla
            inicio = i
            while i < len(texto) and (texto[i] in LETRAS or texto[i] in MAYUS
                                      or texto[i] in DIGITOS or texto[i] == "_"):
                i += 1
            palabra = texto[inicio:i]
            if palabra in BOOLEANOS:
                tokens.append(Token("BOOLEANO", palabra, linea, columna))
            elif palabra in TIPOS:
                tokens.append(Token("TIPO", palabra, linea, columna))
            elif palabra in LOGICOS:
                tokens.append(Token("LOGICO", palabra, linea, columna))
            elif palabra in CONTROL or palabra in RESERVADAS:
                tokens.append(Token("RESERVADA", palabra, linea, columna))
            elif any(ch in MAYUS for ch in palabra):
                raise ErrorLexico(f"identificador inválido '{palabra}', solo admite minúsculas", linea, columna)
            else:
                tokens.append(Token("IDENTIFICADOR", palabra, linea, columna))

        elif c in DIGITOS:                # número: dígitos [ "." dígitos ]
            inicio = i
            while i < len(texto) and texto[i] in DIGITOS:
                i += 1
            if i < len(texto) and texto[i] == ".":
                i += 1
                if i >= len(texto) or texto[i] not in DIGITOS:
                    raise ErrorLexico("número mal formado, falta un dígito después del '.'", linea, columna)
                while i < len(texto) and texto[i] in DIGITOS:
                    i += 1
                if i < len(texto) and texto[i] == ".":
                    raise ErrorLexico("número mal formado, tiene más de un punto", linea, columna)
            tokens.append(Token("NUMERO", texto[inicio:i], linea, columna))

        elif c == '"':                    # texto entre comillas, sin pasar de línea
            i += 1
            inicio = i
            while i < len(texto) and texto[i] != '"' and texto[i] != "\n":
                if texto[i] not in LETRAS + MAYUS + DIGITOS + EXTRA_TEXTO:
                    raise ErrorLexico(f"carácter '{texto[i]}' no reconocido dentro del texto",
                                      linea, i - inicio_linea + 1)
                i += 1
            if i >= len(texto) or texto[i] == "\n":
                raise ErrorLexico("texto sin cerrar, falta la comilla doble", linea, columna)
            tokens.append(Token("TEXTO", texto[inicio:i], linea, columna))
            i += 1

        elif any(texto.startswith(s, i) for s in COMPARADORES):
            simbolo = next(s for s in COMPARADORES if texto.startswith(s, i))
            tokens.append(Token("COMPARADOR", simbolo, linea, columna))
            i += len(simbolo)

        elif c in SIMBOLOS:
            tokens.append(Token("SIMBOLO", c, linea, columna))
            i += 1

        elif c in OPERADORES:
            tokens.append(Token("OPERADOR", c, linea, columna))
            i += 1

        else:
            raise ErrorLexico(f"carácter '{c}' no reconocido", linea, columna)

    tokens.append(Token("EOF", "", linea, i - inicio_linea + 1))
    return tokens
