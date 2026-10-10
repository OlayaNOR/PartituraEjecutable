def clasificar(c):
    if c == " ":
        return "espacio"
    elif c == "\n":
        return "salto de linea"
    elif c == ";":
        return "punto y coma"
    elif c == '"':
        return "comilla"
    elif c.isdigit():
        return "digito"
    elif c.isalpha() and c.islower():
        return "letra minuscula"
    elif c.isalpha():
        return "letra mayuscula"
    elif c.isalnum():
        return "letra o digito"
    else:
        return "otra cosa"


for c in 'tempo 100':
    print(repr(c), "->", clasificar(c))

print()
for c in 'Si = 2;\n':
    print(repr(c), "->", clasificar(c))
