# -*- coding: utf-8 -*-
"""Parser de TocaScript: implementa las 33 producciones de gramatica.md, una función por producción,
por descenso recursivo. En <factor> hace retroceso, porque una condición y una variable sola empiezan igual.
Sirve para verificar —como pide el profesor— que la gramática GENERA cada regla de reglas.txt,
y para producir las derivaciones de las fichas. Una función por producción."""
import re

# número de cada producción: única fuente de verdad, compartida con el generador
NUM = {n: i + 1 for i, n in enumerate([
    "programa", "cabecera", "ajuste", "pieza", "motivo", "seccion", "tipo_seccion",
    "evento", "nota", "nombre_nota", "octava", "figura", "nombre_figura",
    "regla", "expresion", "termino", "factor", "condicion", "operador", "operando",
    "sumando", "primario", "acciones", "accion",
    "variable", "identificador", "valor", "numero", "texto",
    "letra", "mayuscula", "digito", "nl"])}

KW_REGLA = {"AL", "TOCAR", "Y", "O", "NO"}
KW_PIEZA = {"motivo", "seccion", "tipo", "pieza", "silencio"}
TIPOS = {"intro", "estrofa", "estribillo", "coda"}
FIGURAS = {"redonda", "blanca", "negra", "corchea", "semicorchea", "fusa"}
OPS = [">=", "<=", "<>", ">", "<", "=", "+", "-", "*", "/"]
REL = {">", "<", ">=", "<=", "=", "<>"}
SIMB = {"(", ")", "{", "}", "[", "]", ":", "."}
NOTA_RE = re.compile(r"(do|re|mi|fa|sol|la|si)(#|b)?(\d)(?![a-z0-9_])")


class Tok:
    def __init__(self, kind, text, pos): self.kind, self.text, self.pos = kind, text, pos
    def __repr__(self): return f"{self.kind}:{self.text!r}"


def tokenizar(src):
    """Fuera de llaves el salto de línea es el token <nl>; dentro cuenta como espacio.
    Los comentarios (# …) se descartan."""
    toks, i, n, prof = [], 0, len(src), 0
    while i < n:
        c = src[i]
        if c == "\n":
            if prof == 0 and toks and toks[-1].kind != "nl": toks.append(Tok("nl", "↵", i))
            i += 1; continue
        if c in " \t\r": i += 1; continue
        if c == "#" and (i == 0 or src[i - 1] in " \n\t"):
            while i < n and src[i] != "\n": i += 1
            continue
        if c == '"':
            j = src.index('"', i + 1); toks.append(Tok("texto", src[i:j + 1], i)); i = j + 1; continue
        m = NOTA_RE.match(src, i)
        if m and (i == 0 or not (src[i - 1].isalnum() or src[i - 1] == "_")):
            toks.append(Tok("nota", m.group(0), i)); i = m.end(); continue
        m = re.match(r"[0-9]+(\.[0-9]+)?", src[i:])
        if m: toks.append(Tok("numero", m.group(0), i)); i += m.end(); continue
        m = re.match(r"[A-Za-z_][A-Za-z0-9_]*", src[i:])
        if m:
            w = m.group(0)
            k = ("kw" if w in KW_REGLA or w in KW_PIEZA else "tipo" if w in TIPOS else
                 "figura" if w in FIGURAS else "bool" if w in ("true", "false") else "ident")
            toks.append(Tok(k, w, i)); i += m.end(); continue
        for op in OPS:
            if src.startswith(op, i): toks.append(Tok("op", op, i)); i += len(op); break
        else:
            if c in SIMB:
                prof += (c == "{") - (c == "}")
                toks.append(Tok("simb", c, i)); i += 1
            else:
                raise SyntaxError(f"carácter no reconocido {c!r} en posición {i}")
    if toks and toks[-1].kind != "nl": toks.append(Tok("nl", "↵", n))
    return toks


class N:
    """Nodo del árbol de derivación. nombre = "<x>" (no terminal) o un terminal entre comillas."""
    def __init__(self, nombre, hijos=None):
        self.nombre, self.hijos = nombre, hijos or []
        self.num = NUM.get(nombre[1:-1]) if nombre.startswith("<") else None
    def hoja(self): return not self.nombre.startswith("<")


def T(t): return N("'\"'" if t == '"' else f'"{t}"')


class Parser:
    def __init__(self, toks): self.t, self.i = toks, 0
    def peek(self): return self.t[self.i] if self.i < len(self.t) else Tok("eof", "", -1)
    def eat(self, kind=None, text=None):
        tk = self.peek()
        if (kind and tk.kind != kind) or (text is not None and tk.text != text):
            raise SyntaxError(f"esperaba {text or kind}, encontré {tk.text!r} en {tk.pos}")
        self.i += 1; return tk
    def fin(self):
        while self.peek().kind == "nl": self.eat()
        if self.peek().kind != "eof": raise SyntaxError(f"sobra {self.peek().text!r} en {self.peek().pos}")

    # ── átomos ──
    def nl(self): self.eat("nl"); return N("<nl>", [T("↵")])
    def letra(self, ch): return N("<letra>", [T(ch)])
    def mayuscula(self, ch): return N("<mayuscula>", [T(ch)])
    def digito(self, ch): return N("<digito>", [T(ch)])

    # ── nombres y valores ──
    def identificador(self, w):
        if not re.fullmatch(r"[a-z][a-z0-9_]*", w): raise SyntaxError(f"identificador inválido {w!r}")
        return N("<identificador>", [self.letra(c) if c.isalpha() else self.digito(c) if c.isdigit() else T("_") for c in w])
    def variable(self, w): return N("<variable>", [self.identificador(w)])
    def numero(self, w):
        ent, _, dec = w.partition(".")
        h = [self.digito(c) for c in ent]
        if dec: h += [T(".")] + [self.digito(c) for c in dec]
        return N("<numero>", h)
    def texto(self, w):
        h = [T('"')]
        for ch in w[1:-1]:
            if ch.isascii() and ch.islower(): h.append(self.letra(ch))
            elif ch.isascii() and ch.isupper(): h.append(self.mayuscula(ch))
            elif ch.isdigit(): h.append(self.digito(ch))
            elif ch in " /": h.append(T(ch))
            else: raise SyntaxError(f"carácter {ch!r} no permitido dentro de <texto>")
        return N("<texto>", h + [T('"')])
    def valor(self):
        tk = self.peek()
        if tk.kind == "numero": self.eat(); return N("<valor>", [self.numero(tk.text)])
        if tk.kind == "bool": self.eat(); return N("<valor>", [T(tk.text)])
        if tk.kind == "texto": self.eat(); return N("<valor>", [self.texto(tk.text)])
        raise SyntaxError(f"esperaba <valor>, encontré {tk.text!r} en {tk.pos}")

    # ── la regla ──
    def primario(self):
        tk = self.peek()
        if tk.kind == "simb" and tk.text == "(":
            self.eat(); o = self.operando(); self.eat("simb", ")")
            return N("<primario>", [T("("), o, T(")")])
        if tk.kind == "ident": self.eat(); return N("<primario>", [self.variable(tk.text)])
        return N("<primario>", [self.valor()])
    def sumando(self):
        h = [self.primario()]
        while self.peek().kind == "op" and self.peek().text in ("*", "/"):
            h += [T(self.eat("op").text), self.primario()]
        return N("<sumando>", h)
    def operando(self):
        h = [self.sumando()]
        while self.peek().kind == "op" and self.peek().text in ("+", "-"):
            h += [T(self.eat("op").text), self.sumando()]
        return N("<operando>", h)
    def operador(self):
        tk = self.eat("op")
        if tk.text not in REL: raise SyntaxError(f"operador relacional inválido {tk.text!r}")
        return N("<operador>", [T(tk.text)])
    def condicion(self):
        a = self.operando(); op = self.operador(); b = self.operando()
        return N("<condicion>", [a, op, b])
    def factor(self):
        tk = self.peek()
        if tk.kind == "kw" and tk.text == "NO":
            self.eat(); return N("<factor>", [T("NO"), self.factor()])
        # <condicion>, <variable> y "(" <expresion> ")" pueden empezar por el mismo token:
        # se intenta primero la condición y, si no cuadra, se retrocede (la gramática no es LL(1)).
        save = self.i
        try:
            a = self.operando()
            if self.peek().kind == "op" and self.peek().text in REL:
                op = self.operador(); b = self.operando()
                return N("<factor>", [N("<condicion>", [a, op, b])])
        except SyntaxError:
            pass
        self.i = save
        if tk.kind == "simb" and tk.text == "(":
            self.eat(); e = self.expresion(); self.eat("simb", ")")
            return N("<factor>", [T("("), e, T(")")])
        return N("<factor>", [self.variable(self.eat("ident").text)])
    def termino(self):
        h = [self.factor()]
        while self.peek().kind == "kw" and self.peek().text == "Y":
            self.eat(); h += [T("Y"), self.factor()]
        return N("<termino>", h)
    def expresion(self):
        h = [self.termino()]
        while self.peek().kind == "kw" and self.peek().text == "O":
            self.eat(); h += [T("O"), self.termino()]
        return N("<expresion>", h)
    def accion(self):
        tk = self.eat("ident")
        if self.peek().kind == "op" and self.peek().text == "=":
            self.eat(); return N("<accion>", [self.variable(tk.text), T("="), self.operando()])
        return N("<accion>", [self.identificador(tk.text)])
    def acciones(self):
        h = [self.accion()]
        while self.peek().kind == "kw" and self.peek().text == "Y":
            self.eat(); h += [T("Y"), self.accion()]
        return N("<acciones>", h)
    def regla(self):
        self.eat("kw", "AL"); e = self.expresion(); self.eat("kw", "TOCAR"); a = self.acciones()
        return N("<regla>", [T("AL"), e, T("TOCAR"), a, self.nl()])

    # ── la música ──
    def nombre_nota(self, w): return N("<nombre_nota>", [T(w)])
    def octava(self, ch): return N("<octava>", [self.digito(ch)])
    def nota(self, w=None):
        w = w or self.eat("nota").text
        m = NOTA_RE.fullmatch(w)
        h = [self.nombre_nota(m.group(1))]
        if m.group(2): h.append(T(m.group(2)))
        return N("<nota>", h + [self.octava(m.group(3))])
    def nombre_figura(self, w): return N("<nombre_figura>", [T(w)])
    def figura(self):
        h = [self.nombre_figura(self.eat("figura").text)]
        if self.peek().kind == "simb" and self.peek().text == ".": self.eat(); h.append(T("."))
        return N("<figura>", h)
    def evento(self):
        tk = self.peek()
        if tk.kind == "nota":
            self.eat(); self.eat("simb", ":"); return N("<evento>", [self.nota(tk.text), T(":"), self.figura()])
        if tk.kind == "simb" and tk.text == "[":
            self.eat(); h = [T("[")]
            while self.peek().kind == "nota": h.append(self.nota())
            self.eat("simb", "]"); self.eat("simb", ":")
            return N("<evento>", h + [T("]"), T(":"), self.figura()])
        if tk.kind == "kw" and tk.text == "silencio":
            self.eat(); self.eat("simb", ":"); return N("<evento>", [T("silencio"), T(":"), self.figura()])
        raise SyntaxError(f"esperaba <evento>, encontré {tk.text!r} en {tk.pos}")

    # ── estructura ──
    def tipo_seccion(self): return N("<tipo_seccion>", [T(self.eat("tipo").text)])
    def seccion(self):
        self.eat("kw", "seccion"); nom = self.identificador(self.eat("ident").text)
        self.eat("kw", "tipo"); ts = self.tipo_seccion(); self.eat("simb", "{")
        h = [T("seccion"), nom, T("tipo"), ts, T("{")]
        while not (self.peek().kind == "simb" and self.peek().text == "}"):
            h.append(self.identificador(self.eat().text) if self.peek().kind == "ident" else self.evento())
        self.eat("simb", "}")
        return N("<seccion>", h + [T("}"), self.nl()])
    def motivo(self):
        self.eat("kw", "motivo"); nom = self.identificador(self.eat("ident").text); self.eat("simb", "{")
        h = [T("motivo"), nom, T("{")]
        while not (self.peek().kind == "simb" and self.peek().text == "}"): h.append(self.evento())
        self.eat("simb", "}")
        return N("<motivo>", h + [T("}"), self.nl()])
    def pieza(self):
        self.eat("kw", "pieza"); tx = self.texto(self.eat("texto").text); self.eat("simb", "{")
        h = [T("pieza"), tx, T("{")]
        while self.peek().kind == "ident": h.append(self.identificador(self.eat().text))
        self.eat("simb", "}")
        return N("<pieza>", h + [T("}"), self.nl()])
    def ajuste(self):
        return N("<ajuste>", [self.variable(self.eat("ident").text), self.valor()])
    def cabecera(self):
        h = []
        for _ in range(3): h += [self.ajuste(), self.nl()]
        return N("<cabecera>", h)
    def programa(self):
        h = [self.cabecera()]
        while not (self.peek().kind == "kw" and self.peek().text == "pieza"):
            tk = self.peek()
            if tk.kind == "kw" and tk.text == "motivo": h.append(self.motivo())
            elif tk.kind == "kw" and tk.text == "seccion": h.append(self.seccion())
            elif tk.kind == "kw" and tk.text == "AL": h.append(self.regla())
            elif tk.kind == "nl": self.eat()
            else: raise SyntaxError(f"no esperaba {tk.text!r} en {tk.pos}")
        h.append(self.pieza())
        return N("<programa>", h)


def derivar(nombre, texto):
    """Deriva `texto` empezando en <nombre>. Devuelve el árbol o lanza SyntaxError."""
    t = texto.strip()
    if nombre == "nl":
        if t != "↵": raise SyntaxError("no es un salto de línea")
        return N("<nl>", [T("↵")])
    if nombre in ("letra", "mayuscula", "digito"):
        ok = {"letra": r"[a-z]", "mayuscula": r"[A-Z]", "digito": r"[0-9]"}[nombre]
        if not re.fullmatch(ok, t): raise SyntaxError(f"{t!r} no es <{nombre}>")
        return N(f"<{nombre}>", [T(t)])
    if nombre == "octava":
        if not re.fullmatch(r"[0-9]", t): raise SyntaxError(f"{t!r} no es un dígito")
        return N("<octava>", [N("<digito>", [T(t)])])
    if nombre == "nombre_nota":
        if t not in ("do", "re", "mi", "fa", "sol", "la", "si"): raise SyntaxError(f"{t!r} no es un nombre de nota")
        return N("<nombre_nota>", [T(t)])
    if nombre == "nombre_figura":
        if t not in FIGURAS: raise SyntaxError(f"{t!r} no es una figura")
        return N("<nombre_figura>", [T(t)])
    src = texto if texto.endswith(chr(10)) else texto + chr(10)
    p = Parser(tokenizar(src))
    if nombre in ("identificador", "variable", "numero", "texto", "nota"):
        tk = p.eat()
        arbol = getattr(p, nombre)(tk.text); p.fin(); return arbol
    if nombre == "tipo_seccion":
        if p.peek().text == "tipo": p.eat()
        arbol = p.tipo_seccion(); p.fin(); return arbol
    if nombre == "figura":
        if p.peek().kind == "simb" and p.peek().text == ":": p.eat()
        arbol = p.figura(); p.fin(); return arbol
    arbol = getattr(p, nombre)()
    p.fin()
    return arbol


COMPACTOS = {"<identificador>", "<numero>", "<texto>", "<nota>", "<nl>"}

def arbol_txt(n, ind=0, compacto=True, max_prof=None):
    pad = "  " * ind
    if n.hoja(): return pad + n.nombre + "\n"
    tag = f"{n.nombre} ({n.num})"
    if max_prof is not None and ind >= max_prof and n.hijos:
        return pad + tag + "  → " + " ".join(h.nombre if h.hoja() else h.nombre for h in n.hijos) + "\n"
    if compacto and n.nombre in COMPACTOS:
        return pad + tag + "  → " + " ".join(hojas(n)) + "\n"
    return pad + tag + "\n" + "".join(arbol_txt(h, ind + 1, compacto, max_prof) for h in n.hijos)


def hojas(n):
    return [n.nombre] if n.hoja() else [x for h in n.hijos for x in hojas(h)]


def contar(n, acc=None):
    acc = acc if acc is not None else {"nt": 0, "t": 0}
    if n.hoja(): acc["t"] += 1
    else:
        acc["nt"] += 1
        for h in n.hijos: contar(h, acc)
    return acc


def categoria_token(tk):
    """Para la tabla de tokens: a qué terminal o no terminal corresponde cada token del lexer."""
    q = NUM
    if tk.kind == "nl": return f'terminal `"↵"` · `<nl>` ({q["nl"]})'
    if tk.kind in ("kw", "simb"): return f'terminal `"{tk.text}"`'
    if tk.kind == "op":
        if tk.text in (">", "<", ">=", "<=", "<>"): return f'terminal `"{tk.text}"` · `<operador>` ({q["operador"]})'
        if tk.text == "=": return 'terminal `"="` (comparación en `<condicion>`, asignación en `<accion>`)'
        if tk.text in ("+", "-"): return f'terminal `"{tk.text}"` · `<operando>` ({q["operando"]})'
        return f'terminal `"{tk.text}"` · `<sumando>` ({q["sumando"]})'
    if tk.kind == "ident": return f'`<identificador>` ({q["identificador"]}) → `<letra>` … ({q["letra"]})'
    if tk.kind == "numero": return f'`<numero>` ({q["numero"]}) → `<digito>` … ({q["digito"]})'
    if tk.kind == "texto": return f'`<texto>` ({q["texto"]}) → `\'"\'` … `\'"\'`'
    if tk.kind == "bool": return f'terminal `"{tk.text}"` · `<valor>` ({q["valor"]})'
    if tk.kind == "nota": return f'`<nota>` ({q["nota"]}) → `<nombre_nota>` `<octava>`'
    if tk.kind == "figura": return f'`<nombre_figura>` ({q["nombre_figura"]})'
    if tk.kind == "tipo": return f'`<tipo_seccion>` ({q["tipo_seccion"]})'
    return tk.kind
