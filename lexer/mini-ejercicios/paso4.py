def imprimir_digitos(texto):
    i = 0
    while i < len(texto):
        if texto[i].isdigit():
            print(texto[i])
        i += 1


print("a1b22c:")
imprimir_digitos("a1b22c")

print("sin digitos:")
imprimir_digitos("sin digitos")

print("termina en 7:")
imprimir_digitos("termina en 7")

print("vacio:")
imprimir_digitos("")
