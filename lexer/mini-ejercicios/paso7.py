def digitos(texto):
    lista = []
    i = 0
    while i < len(texto):
        c = texto[i]
        if c.isdigit():
            lista.append(("DIGITO", c))
        elif not c.isalpha():
            raise SyntaxError(f"Caracter inesperado '{c}' en la posicion {i}")
        i += 1
    return lista


for texto in ("a1b", "a1@", "x9y8", "@"):
    try:
        print(texto, "->", digitos(texto))
    except SyntaxError as e:
        print(texto, "-> ERROR:", e)
