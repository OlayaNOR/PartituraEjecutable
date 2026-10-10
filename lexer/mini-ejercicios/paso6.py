def digitos(texto):
    lista = []
    i = 0
    while i < len(texto):
        if texto[i].isdigit():
            lista.append(("DIGITO", texto[i]))
        i += 1
    return lista


print(digitos("a1b22c"))
print(digitos("sin digitos"))
print(digitos("tempo 100"))

resultado = digitos("x9y8")
print(len(resultado), "digitos encontrados")
