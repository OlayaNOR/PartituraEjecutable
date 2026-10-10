LETRAS = "abcdefghijklmnopqrstuvwxyz"
MAYUS = LETRAS.upper()
DIGITOS = "0123456789"
RESERVADAS = {"AL", "TOCAR", "mostrar"}


def tokenizar_declaracion(texto):
    tokens = []
    i = 0
    while i < len(texto):
        c = texto[i]

        if c == " ":                      # el lexer descarta espacios
            i += 1

        elif c == "\n":                   # <nl> es un terminal
            tokens.append(("NL", "\\n"))
            i += 1

        elif c in LETRAS or c in MAYUS:   # palabra: reservada, booleano o identificador
            inicio = i
            while i < len(texto) and (texto[i] in LETRAS or texto[i] in MAYUS
                                      or texto[i] in DIGITOS
                                      or texto[i] == "_"):
                i += 1
            palabra = texto[inicio:i]

            if palabra in ("true", "false"):
                tokens.append(("BOOLEANO", palabra))
            elif palabra in RESERVADAS:
                tokens.append(("RESERVADA", palabra))
            elif any(ch in MAYUS for ch in palabra):
                # <identificador> solo admite minúsculas, dígitos y "_"
                raise SyntaxError(f"Identificador inválido '{palabra}': solo admite minúsculas")
            else:
                tokens.append(("IDENTIFICADOR", palabra))

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
            tokens.append(("NUMERO", texto[inicio:i]))

        elif c == '"':                    # <texto>
            i += 1
            inicio = i
            while i < len(texto) and texto[i] != '"':
                if texto[i] not in LETRAS + MAYUS + DIGITOS + " /":
                    raise SyntaxError(f"Carácter inesperado '{texto[i]}' dentro del texto")
                i += 1
            if i >= len(texto):
                raise SyntaxError("Texto sin cerrar: falta la comilla doble")
            tokens.append(("TEXTO", texto[inicio:i]))
            i += 1                        # salta la comilla de cierre

        else:
            raise SyntaxError(f"Carácter inesperado '{c}'")

    return tokens


pruebas = [
    'tempo 100',
    'compas "4/4"',
    'tonalidad "Do mayor"',
    'umbral 0.7',
    'activo true',
    'tempo 100\ncompas "4/4"',
    'AL tempo TOCAR mostrar tempo',
    'tempo = 100',
    'Tempo 100',
    'tempo 0.',
    'tonalidad "Do mayor',
    'titulo "¡Hola!"',
]

for texto in pruebas:
    try:
        print(repr(texto), "->", tokenizar_declaracion(texto))
    except SyntaxError as e:
        print(repr(texto), "-> ERROR:", e)
