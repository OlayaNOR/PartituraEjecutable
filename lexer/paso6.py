# paso6.py · Tareas 4 + 5 + 6: tipos, asignación, fin de instrucción y comentarios
# Cambio nuevo respecto a paso5.py: el bloque del comentario (# hasta el final de la línea).

LETRAS = "abcdefghijklmnopqrstuvwxyz"
MAYUS = LETRAS.upper()
DIGITOS = "0123456789"

TIPOS = {"motivo", "acorde", "seccion", "tipo", "pieza", "voz", "simultaneo"}
LOGICOS = {"Y", "O", "NO"}
RESERVADAS = {
    "AL", "TOCAR", "mostrar",
    "tocar", "repetir", "finales", "vez", "con", "silencio", "sin", "reglas", "exportar",
    "transportado", "invertido", "retrogradado", "semitonos", "velocidad",
    "en", "crescendo", "hasta", "durante",
    "intro", "estrofa", "estribillo", "coda",
    "redonda", "blanca", "negra", "corchea", "semicorchea", "fusa",
    "do", "re", "mi", "fa", "sol", "la", "si",
}

SIMBOLOS_LARGOS = [">=", "<=", "<>"]   # 2+ caracteres: se revisan PRIMERO
SIMBOLOS_1 = {"=", "<", ">"}           # 1 caracter (el "=" de asignación va aquí)


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

        elif c == "\n":                   # <nl> es un terminal
            tokens.append(("NL", "\\n", linea, columna))
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

            if palabra in ("true", "false"):
                tokens.append(("BOOLEANO", palabra, linea, columna))
            elif palabra in TIPOS:
                tokens.append(("TIPO", palabra, linea, columna))
            elif palabra in LOGICOS:
                tokens.append(("OPERADOR", palabra, linea, columna))
            elif palabra in RESERVADAS:
                tokens.append(("RESERVADA", palabra, linea, columna))
            elif any(ch in MAYUS for ch in palabra):
                # <identificador> solo admite minúsculas, dígitos y "_"
                raise SyntaxError(f"Identificador inválido '{palabra}': solo admite minúsculas")
            else:
                tokens.append(("IDENTIFICADOR", palabra, linea, columna))

        elif c in DIGITOS:                # <numero>: dígitos [ "." dígitos ]
            inicio = i
            while i < len(texto) and texto[i] in DIGITOS:
                i += 1
            if i < len(texto) and texto[i] == ".":
                i += 1
                if i >= len(texto) or texto[i] not in DIGITOS:
                    raise SyntaxError("Número mal formado: falta un dígito después del '.'")
                while i < len(texto) and texto[i] in DIGITOS:
                    i += 1
            tokens.append(("NUMERO", texto[inicio:i], linea, columna))

        elif c == '"':                    # <texto>
            i += 1
            inicio = i
            while i < len(texto) and texto[i] != '"':
                if texto[i] not in LETRAS + MAYUS + DIGITOS + " /":
                    raise SyntaxError(f"Carácter inesperado '{texto[i]}' dentro del texto")
                i += 1
            if i >= len(texto):
                raise SyntaxError("Texto sin cerrar: falta la comilla doble")
            tokens.append(("TEXTO", texto[inicio:i], linea, columna))
            i += 1                        # salta la comilla de cierre

        elif any(texto.startswith(s, i) for s in SIMBOLOS_LARGOS):
            for s in SIMBOLOS_LARGOS:
                if texto.startswith(s, i):
                    tokens.append(("SIMBOLO", s, linea, columna))
                    i += len(s)           # avanza tantas posiciones como mida el símbolo
                    break

        elif c in SIMBOLOS_1:
            tokens.append(("SIMBOLO", c, linea, columna))
            i += 1

        else:
            raise SyntaxError(f"Carácter inesperado '{c}'")

    return tokens


if __name__ == "__main__":
    pruebas = ['tempo 100  # velocidad de la pieza',
               'tempo 100  # velocidad\ncompas "4/4"',
               '# solo un comentario\ntempo 100',
               'motivo tema = 5\n# linea de comentario\nvolumen 80']
    for texto in pruebas:
        print(repr(texto))
        try:
            for token in tokenizar(texto):
                print("  ", token)
        except SyntaxError as e:
            print("   ERROR:", e)
