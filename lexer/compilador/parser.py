# parser.py · Sesión 3: primer prototipo de la clase Parser
# Guarda la lista de tokens y la posición actual; por ahora solo sabe ver el token actual y avanzar.


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens              # la lista que devuelve el lexer, siempre termina en EOF
        self.pos = 0                      # en qué token va este parser

    def actual(self):
        """Devuelve el token actual sin moverse."""
        return self.tokens[self.pos]

    def avanzar(self):
        """Devuelve el token actual y pasa al siguiente. En EOF se queda quieto."""
        token = self.actual()
        if token.tipo != "EOF":
            self.pos += 1
        return token
