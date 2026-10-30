# pruebas_30oct.py · Sesión 1 del 30 de octubre: los "listo cuando" de las tareas 8 a 12
# La salida esperada de cada caso se calculó a mano ANTES de ejecutar (prueba de escritorio).
# Al final se repiten los 6 casos de pruebas.py: deben dar lo mismo, ahora con el EOF al final.

from paso12 import tokenizar

casos = [
    # ----- Tarea 8 · delimitadores -----
    ("T8 · paréntesis y operadores",
     '(tempo+5)*2',
     [("SIMBOLO", "(", 1, 1), ("IDENTIFICADOR", "tempo", 1, 2), ("OPERADOR", "+", 1, 7),
      ("NUMERO", "5", 1, 8), ("SIMBOLO", ")", 1, 9), ("OPERADOR", "*", 1, 10),
      ("NUMERO", "2", 1, 11), ("EOF", "", 1, 12)]),

    ("T8 · dos puntos y puntillo",
     'silencio:negra.',
     [("RESERVADA", "silencio", 1, 1), ("SIMBOLO", ":", 1, 9), ("RESERVADA", "negra", 1, 10),
      ("SIMBOLO", ".", 1, 15), ("EOF", "", 1, 16)]),

    ("T8 · punto entre nombres frente a punto decimal",
     'tema.parte 3.14',
     [("IDENTIFICADOR", "tema", 1, 1), ("SIMBOLO", ".", 1, 5), ("IDENTIFICADOR", "parte", 1, 6),
      ("NUMERO", "3.14", 1, 12), ("EOF", "", 1, 16)]),

    ("T8 · llaves, corchetes y coma",
     '{[a,b]}',
     [("SIMBOLO", "{", 1, 1), ("SIMBOLO", "[", 1, 2), ("IDENTIFICADOR", "a", 1, 3),
      ("SIMBOLO", ",", 1, 4), ("IDENTIFICADOR", "b", 1, 5), ("SIMBOLO", "]", 1, 6),
      ("SIMBOLO", "}", 1, 7), ("EOF", "", 1, 8)]),

    # ----- Tarea 9 · operadores de dos caracteres -----
    ("T9 · x >= 5 da 3 tokens",
     'x >= 5',
     [("IDENTIFICADOR", "x", 1, 1), ("OPERADOR", ">=", 1, 3), ("NUMERO", "5", 1, 6), ("EOF", "", 1, 7)]),

    ("T9 · x > = 5 da 4 tokens",
     'x > = 5',
     [("IDENTIFICADOR", "x", 1, 1), ("OPERADOR", ">", 1, 3), ("SIMBOLO", "=", 1, 5),
      ("NUMERO", "5", 1, 7), ("EOF", "", 1, 8)]),

    ("T9 · distinto y menor o igual sin espacios",
     'a<>b<=c',
     [("IDENTIFICADOR", "a", 1, 1), ("OPERADOR", "<>", 1, 2), ("IDENTIFICADOR", "b", 1, 4),
      ("OPERADOR", "<=", 1, 5), ("IDENTIFICADOR", "c", 1, 7), ("EOF", "", 1, 8)]),

    ("T9 · un ! solo es error léxico",
     'x ! 5',
     "Línea 1, columna 3: carácter inesperado '!'"),

    # ----- Tarea 10 · control y booleanos -----
    ("T10 · repetir es RESERVADA, repetirlo y repetir_x no",
     'repetir repetirlo repetir_x',
     [("RESERVADA", "repetir", 1, 1), ("IDENTIFICADOR", "repetirlo", 1, 9),
      ("IDENTIFICADOR", "repetir_x", 1, 19), ("EOF", "", 1, 28)]),

    ("T10 · la regla AL ... TOCAR con booleano",
     'AL activo = true TOCAR mostrar tempo',
     [("RESERVADA", "AL", 1, 1), ("IDENTIFICADOR", "activo", 1, 4), ("SIMBOLO", "=", 1, 11),
      ("BOOLEANO", "true", 1, 13), ("RESERVADA", "TOCAR", 1, 18), ("RESERVADA", "mostrar", 1, 24),
      ("IDENTIFICADOR", "tempo", 1, 32), ("EOF", "", 1, 37)]),

    ("T10 · falso es BOOLEANO, falsete es IDENTIFICADOR",
     'false falsete',
     [("BOOLEANO", "false", 1, 1), ("IDENTIFICADOR", "falsete", 1, 7), ("EOF", "", 1, 14)]),

    # ----- Tarea 11 · comentarios de bloque -----
    ("T11 · comentario de 3 líneas entre dos ajustes",
     'tempo 120 /* uno\ndos\ntres */\nvolumen 80',
     [("IDENTIFICADOR", "tempo", 1, 1), ("NUMERO", "120", 1, 7), ("NL", "\\n", 3, 8),
      ("IDENTIFICADOR", "volumen", 4, 1), ("NUMERO", "80", 4, 9), ("EOF", "", 4, 11)]),

    ("T11 · comentario sin cerrar",
     'tempo 120 /* sin cerrar',
     "Línea 1, columna 11: comentario sin cerrar"),

    ("T11 · sin cerrar que empieza en la línea 2",
     'tempo 120\n/* uno\ndos',
     "Línea 2, columna 1: comentario sin cerrar"),

    # ----- Tarea 12 · fin de archivo -----
    ("T12 · volumen = 5 da 3 tokens más EOF",
     'volumen = 5',
     [("IDENTIFICADOR", "volumen", 1, 1), ("SIMBOLO", "=", 1, 9), ("NUMERO", "5", 1, 11),
      ("EOF", "", 1, 12)]),

    ("T12 · el texto vacío da solo EOF",
     '',
     [("EOF", "", 1, 1)]),

    ("T12 · terminando en salto, EOF en la línea siguiente",
     'tempo 120\n',
     [("IDENTIFICADOR", "tempo", 1, 1), ("NUMERO", "120", 1, 7), ("NL", "\\n", 1, 10), ("EOF", "", 2, 1)]),

    # ----- Los 6 casos de pruebas.py (tarea 7), ahora con EOF -----
    ("T7 · Válido 1 · simple",
     'tempo 120',
     [("IDENTIFICADOR", "tempo", 1, 1), ("NUMERO", "120", 1, 7), ("EOF", "", 1, 10)]),

    ("T7 · Válido 2 · sin espacios, con operadores",
     'volumen=tempo+5*2',
     [("IDENTIFICADOR", "volumen", 1, 1), ("SIMBOLO", "=", 1, 8), ("IDENTIFICADOR", "tempo", 1, 9),
      ("OPERADOR", "+", 1, 14), ("NUMERO", "5", 1, 15), ("OPERADOR", "*", 1, 16), ("NUMERO", "2", 1, 17),
      ("EOF", "", 1, 18)]),

    ("T7 · Válido 3 · dos líneas, comentario, decimal y cadena",
     'umbral 0.75  # sensibilidad\ncompas "4/4"',
     [("IDENTIFICADOR", "umbral", 1, 1), ("NUMERO", "0.75", 1, 8), ("NL", "\\n", 1, 28),
      ("IDENTIFICADOR", "compas", 2, 1), ("TEXTO", "4/4", 2, 8), ("EOF", "", 2, 13)]),

    ("T7 · Inválido 1 · carácter que no existe",
     'tempo 100 @',
     "Línea 1, columna 11: carácter inesperado '@'"),

    ("T7 · Inválido 2 · declaración al estilo Java",
     'int tempo = 100;',
     "Línea 1, columna 16: carácter inesperado ';'"),

    ("T7 · Inválido 3 · error en la segunda línea (cadena sin cerrar)",
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
