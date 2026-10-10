texto = "a1b22c"
lista = []
i = 0
while i < len(texto):
    if texto[i].isdigit():
        lista.append(("DIGITO", texto[i]))
    i += 1

print(lista)
print(len(lista))
print(lista[0])
print(lista[0][1])

texto = "sin digitos"
lista = []
i = 0
while i < len(texto):
    if texto[i].isdigit():
        lista.append(("DIGITO", texto[i]))
    i += 1
print(lista)
