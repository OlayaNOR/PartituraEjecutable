# pruebas.py · Tarea 7: los 6 casos del parcial 2
# La salida esperada de cada caso se calculó a mano ANTES de ejecutar (prueba de escritorio).
# El programa corre el lexer, muestra la salida real y marca si coincide con la esperada.

from paso6_3 import tokenizar

casos = [
    # ----- 3 casos válidos -----
    ("Válido 1 · simple",
     'tempo 120',
     [("IDENTIFICADOR", "tempo", 1, 1), ("NUMERO", "120", 1, 7)]),

    ("Válido 2 · sin espacios, con operadores",
     'volumen=tempo+5*2',
     [("IDENTIFICADOR", "volumen", 1, 1), ("SIMBOLO", "=", 1, 8), ("IDENTIFICADOR", "tempo", 1, 9),
      ("OPERADOR", "+", 1, 14), ("NUMERO", "5", 1, 15), ("OPERADOR", "*", 1, 16), ("NUMERO", "2", 1, 17)]),

    ("Válido 3 · dos líneas, comentario, decimal y cadena",
     'umbral 0.75  # sensibilidad\ncompas "4/4"',
     [("IDENTIFICADOR", "umbral", 1, 1), ("NUMERO", "0.75", 1, 8), ("NL", "\\n", 1, 28),
      ("IDENTIFICADOR", "compas", 2, 1), ("TEXTO", "4/4", 2, 8)]),

    # ----- 3 casos inválidos -----
    ("Inválido 1 · carácter que no existe",
     'tempo 100 @',
     "Línea 1, columna 11: carácter inesperado '@'"),

    ("Inválido 2 · declaración al estilo Java",
     'int tempo = 100;',
     "Línea 1, columna 16: carácter inesperado ';'"),

    ("Inválido 3 · error en la segunda línea (cadena sin cerrar)",
     'tempo 100\ntonalidad "Do mayor',
     "Línea 2, columna 11: texto sin cerrar, falta la comilla doble"),
]

aciertos = 0
for nombre, entrada, esperado in casos:
    try:
        real = tokenizar(entrada)
    except SyntaxError as e:
        real = str(e)
    coincide = real == esperado
    aciertos += coincide
    print(nombre)
    print("   entrada :", repr(entrada))
    print("   esperado:", esperado)
    print("   real    :", real)
    print("   ", "✔ coincide" if coincide else "✘ NO coincide: revisar si se equivocó el cálculo o el lexer")
    print()

print(f"{aciertos} de {len(casos)} casos coinciden")
