# paso4.py · Tarea 4: palabras reservadas (los tipos)
# Cambios respecto al lexer anterior: TIPOS, LOGICOS y RESERVADAS ampliada.

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

        else:
            raise SyntaxError(f"Carácter inesperado '{c}'")

    return tokens


if __name__ == "__main__":
    pruebas = ['motivo tema',
               'motivos',
               'domingo',
               'tempo 100\ncompas "4/4"',
               'tempo 100\numbral 0.7\nactivo true']
    for texto in pruebas:
        print(repr(texto))
        for token in tokenizar(texto):
            print("  ", token)
