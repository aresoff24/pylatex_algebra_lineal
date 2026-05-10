#!/usr/bin/env python3
"""
Script unificado: Matrices aleatorias, Determinante (Gauss) e Inversa (Cofactores)
Autor: Diego Alexander Cuervo Padilla | Código: 2150049
Curso: Tecnología en Analítica de Datos – UFPS
"""
import argparse
import random
import sys
from fractions import Fraction
from pylatex import Document, Section, Subsection, Math, NoEscape, Package

# ─────────────────────────────────── PARTE 1 ───────────────────────────────────
def _rand(low=-9, high=9):
    v = 0
    while v == 0:
        v = random.randint(low, high)
    return v

def matriz_fila(n=4): return [[_rand() for _ in range(n)]]
def matriz_columna(m=4): return [[_rand()] for _ in range(m)]
def matriz_cuadrada(n=3): return [[_rand() for _ in range(n)] for _ in range(n)]
def matriz_rectangular(m=3, n=4): return [[_rand() for _ in range(n)] for _ in range(m)]
def matriz_diagonal(n=3):
    M = [[0]*n for _ in range(n)]
    for i in range(n): M[i][i] = _rand()
    return M
def matriz_triangular_superior(n=3):
    M = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i, n): M[i][j] = _rand()
    return M
def matriz_triangular_inferior(n=3):
    M = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(0, i+1): M[i][j] = _rand()
    return M
def matriz_identidad(n=3): return [[1 if i==j else 0 for j in range(n)] for i in range(n)]
def matriz_nula(m=3, n=3): return [[0]*n for _ in range(m)]
def matriz_simetrica(n=3):
    M = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            v = _rand()
            M[i][j] = M[j][i] = v
    return M

GENERADORES = {
    "fila": lambda r,c: matriz_fila(c),
    "columna": lambda r,c: matriz_columna(r),
    "cuadrada": lambda r,c: matriz_cuadrada(r),
    "rectangular": lambda r,c: matriz_rectangular(r,c),
    "diagonal": lambda r,c: matriz_diagonal(r),
    "triangular_sup": lambda r,c: matriz_triangular_superior(r),
    "triangular_inf": lambda r,c: matriz_triangular_inferior(r),
    "identidad": lambda r,c: matriz_identidad(r),
    "nula": lambda r,c: matriz_nula(r,c),
    "simetrica": lambda r,c: matriz_simetrica(r),
}
DESCRIPCIONES = {
    "fila": "Matriz fila: 1 × n con valores aleatorios.",
    "columna": "Matriz columna: m × 1 con valores aleatorios.",
    "cuadrada": "Matriz cuadrada: n × n con valores aleatorios.",
    "rectangular": "Matriz rectangular: m × n con m ≠ n.",
    "diagonal": "Matriz diagonal: ceros excepto en la diagonal.",
    "triangular_sup": "Triangular superior: ceros debajo de la diagonal.",
    "triangular_inf": "Triangular inferior: ceros encima de la diagonal.",
    "identidad": "Matriz identidad: unos en la diagonal.",
    "nula": "Matriz nula: todos sus elementos cero.",
    "simetrica": "Matriz simétrica: A = Aᵀ.",
}

def parte1(tipo, filas, columnas, salida):
    generador = GENERADORES[tipo]
    M = generador(filas, columnas)
    m, n = len(M), len(M[0])

    doc = Document(geometry_options={"margin": "2.5cm"})
    for pkg, opt in [("amsmath",None),("amssymb",None),("fontenc","T1"),
                     ("inputenc","utf8"),("babel","spanish")]:
        if opt: doc.packages.append(Package(pkg, options=opt))
        else: doc.packages.append(Package(pkg))

    doc.preamble.append(NoEscape(r"""
\title{\textbf{Generación de Matrices Aleatorias}\\[0.3em]
       \large Tipo: """ + tipo.replace("_", r"\_") + r"""}
\author{Diego Alexander Cuervo Padilla \\ Código: 2150049 \\
        Tecnología en Analítica de Datos --- UFPS}
\date{\today}
"""))
    doc.append(NoEscape(r"\maketitle\tableofcontents\newpage"))
    with doc.create(Section("Definición")):
        doc.append(NoEscape(DESCRIPCIONES[tipo]))
    with doc.create(Section("Matriz generada")):
        doc.append(NoEscape(rf"Tipo: \textbf{{{tipo.replace('_',' ')}}}; dimensión ${m}\times{n}$:"))
        doc.append(NoEscape(r"\[" + mat_tex_int(M) + r"\]"))
    with doc.create(Section("Código Python")):
        cod = snippet(tipo)
        doc.append(NoEscape(r"\begin{verbatim}" + cod + r"\end{verbatim}"))

    compilar(doc, salida)

def snippet(tipo):
    snip = {
        "fila": "def matriz_fila(n=4):\n    return [[random.randint(-9,9) for _ in range(n)]]",
        "columna": "def matriz_columna(m=4):\n    return [[random.randint(-9,9)] for _ in range(m)]",
        "cuadrada": "def matriz_cuadrada(n=3):\n    return [[random.randint(-9,9) for _ in range(n)] for _ in range(n)]",
        "rectangular": "def matriz_rectangular(m=3,n=4):\n    return [[random.randint(-9,9) for _ in range(n)] for _ in range(m)]",
        "diagonal": "def matriz_diagonal(n=3):\n    M = [[0]*n for _ in range(n)]\n    for i in range(n): M[i][i]=random.randint(-9,9)\n    return M",
        "triangular_sup": "def matriz_triangular_superior(n=3):\n    M=[[0]*n for _ in range(n)]\n    for i in range(n):\n        for j in range(i,n): M[i][j]=random.randint(-9,9)\n    return M",
        "triangular_inf": "def matriz_triangular_inferior(n=3):\n    M=[[0]*n for _ in range(n)]\n    for i in range(n):\n        for j in range(0,i+1): M[i][j]=random.randint(-9,9)\n    return M",
        "identidad": "def matriz_identidad(n=3):\n    M=[[0]*n for _ in range(n)]\n    for i in range(n): M[i][i]=1\n    return M",
        "nula": "def matriz_nula(m=3,n=3):\n    return [[0]*n for _ in range(m)]",
        "simetrica": "def matriz_simetrica(n=3):\n    M=[[0]*n for _ in range(n)]\n    for i in range(n):\n        for j in range(i,n):\n            v=random.randint(-9,9)\n            M[i][j]=M[j][i]=v\n    return M",
    }
    return snip.get(tipo, "# ver código fuente")

# ─────────────────────────── HELPERS COMUNES ───────────────────────────────────
def a_fraction(M):
    return [[Fraction(x) for x in fila] for fila in M]

def frac_tex(f: Fraction) -> str:
    if f.denominator == 1:
        return str(f.numerator)
    if f < 0:
        return rf"-\frac{{{abs(f.numerator)}}}{{{f.denominator}}}"
    return rf"\frac{{{f.numerator}}}{{{f.denominator}}}"

def mat_tex(M):
    filas = [" & ".join(frac_tex(v) for v in fila) for fila in M]
    return r"\begin{bmatrix}" + r" \\ ".join(filas) + r"\end{bmatrix}"

def mat_tex_int(M):
    filas = [" & ".join(str(v) for v in fila) for fila in M]
    return r"\begin{bmatrix}" + r" \\ ".join(filas) + r"\end{bmatrix}"

def compilar(doc, nombre):
    doc.generate_tex(nombre)
    try:
        doc.generate_pdf(nombre, clean_tex=False, compiler="pdflatex")
        print(f"[OK] PDF generado: {nombre}.pdf")
    except Exception as e:
        print(f"[!] No se pudo compilar PDF: {e}")
        print(f"    Archivo .tex disponible: {nombre}.tex")

# ──────────────────────────── PARTE 2: DETERMINANTE ───────────────────────────
def leer_matriz():
    n = int(input("Tamaño n (matriz n×n): "))
    print(f"Ingrese la matriz {n}×{n} fila por fila (valores separados por espacio):")
    M = []
    for i in range(n):
        while True:
            try:
                fila = list(map(Fraction, input(f"  Fila {i+1}: ").split()))
                if len(fila) != n:
                    print(f"  ⚠ Se esperaban {n} valores. Intente de nuevo.")
                    continue
                M.append(fila)
                break
            except ValueError:
                print("  ⚠ Solo números (enteros o fracciones como 3/4). Intente de nuevo.")
    return M

def matriz_demo():
    return [[Fraction(2), Fraction(1), Fraction(-1)],
            [Fraction(-3), Fraction(-1), Fraction(2)],
            [Fraction(-2), Fraction(1), Fraction(2)]]

def determinante_gauss(M_orig):
    n = len(M_orig)
    M = [fila[:] for fila in M_orig]
    signo = Fraction(1)
    pasos = []
    pasos.append({"desc": r"Matriz original $A = " + mat_tex(M_orig) + r"$", "matriz": [fila[:] for fila in M], "op": ""})
    for col in range(n):
        # pivoteo parcial
        max_val = Fraction(0)
        piv = None
        for f in range(col, n):
            if abs(M[f][col]) > max_val:
                max_val = abs(M[f][col])
                piv = f
        if piv is None or max_val == 0:
            pasos.append({"desc": "Columna de ceros → determinante 0.", "matriz": [f[:] for f in M], "op": ""})
            return Fraction(0), pasos
        if piv != col:
            M[col], M[piv] = M[piv], M[col]
            signo *= -1
            pasos.append({"desc": rf"Intercambio $F_{{{col+1}}} \leftrightarrow F_{{{piv+1}}}$ (signo ×-1).",
                          "matriz": [f[:] for f in M], "op": rf"F_{{{col+1}}}\leftrightarrow F_{{{piv+1}}}"})
        pivote = M[col][col]
        for fila in range(col+1, n):
            if M[fila][col] == 0: continue
            factor = M[fila][col] / pivote
            for j in range(col, n):
                M[fila][j] -= factor * M[col][j]
            pasos.append({"desc": rf"$F_{{{fila+1}}} \leftarrow F_{{{fila+1}}} - ({frac_tex(factor)})F_{{{col+1}}}$",
                          "matriz": [f[:] for f in M], "op": rf"F_{{{fila+1}}} \leftarrow F_{{{fila+1}}} - {frac_tex(factor)}F_{{{col+1}}}"})
    prod = Fraction(1)
    for i in range(n): prod *= M[i][i]
    det = signo * prod
    pasos.append({"desc": f"Determinante = {frac_tex(signo)}·({'·'.join(frac_tex(M[i][i]) for i in range(n))}) = {frac_tex(det)}",
                  "matriz": [f[:] for f in M], "op": ""})
    return det, pasos

def parte2(interactivo, demo, salida):
    if demo:
        M = matriz_demo()
        print("Usando matriz de demostración 3×3.")
    else:
        M = leer_matriz()
    det, pasos = determinante_gauss(M)
    print(f"Determinante = {det}")
    # Construir documento
    doc = Document(geometry_options={"margin": "2.5cm"})
    for pkg, opt in [("amsmath",None),("amssymb",None),("fontenc","T1"),
                     ("inputenc","utf8"),("babel","spanish")]:
        if opt: doc.packages.append(Package(pkg, options=opt))
        else: doc.packages.append(Package(pkg))
    doc.preamble.append(NoEscape(r"""
\title{\textbf{Cálculo del Determinante}\\[0.3em]\large Método de Gauss}
\author{Diego Alexander Cuervo Padilla \\ Código: 2150049 \\ UFPS}
\date{\today}
"""))
    doc.append(NoEscape(r"\maketitle\tableofcontents\newpage"))
    with doc.create(Section("Fundamento teórico")):
        doc.append(NoEscape(r"""El método de Gauss transforma $A$ en una matriz triangular superior $U$.
El determinante es $(-1)^s \prod u_{ii}$, donde $s$ son los intercambios."""))
    with doc.create(Section("Matriz original")):
        doc.append(NoEscape(r"\[ A = " + mat_tex(M) + r" \]"))
    with doc.create(Section("Procedimiento")):
        for i, paso in enumerate(pasos, 1):
            with doc.create(Subsection(f"Paso {i}")):
                doc.append(NoEscape(paso["desc"]))
                if paso["op"]:
                    doc.append(NoEscape(r"\[ " + paso["op"] + r" \]"))
                if i > 1 and paso["matriz"]:
                    doc.append(NoEscape(r"\[ " + mat_tex(paso["matriz"]) + r" \]"))
    with doc.create(Section("Resultado")):
        doc.append(NoEscape(r"\[ \boxed{\det(A) = " + frac_tex(det) + r"} \]"))
    compilar(doc, salida)

# ────────────────────────────── PARTE 3: INVERSA ──────────────────────────────
def menor(M, i, j):
    return [[M[r][c] for c in range(len(M)) if c != j] for r in range(len(M)) if r != i]

def cofactor_val(M, i, j):
    signo = Fraction(1) if (i+j)%2==0 else Fraction(-1)
    return signo * determinante_gauss(menor(M, i, j))[0]

def matriz_cofactores(M):
    n = len(M)
    return [[cofactor_val(M, i, j) for j in range(n)] for i in range(n)]

def transponer(M):
    return list(map(list, zip(*M)))

def parte3(interactivo, demo, salida):
    if demo:
        M = matriz_demo()
        print("Usando matriz de demostración 3×3.")
    else:
        M = leer_matriz()
    det, _ = determinante_gauss(M)
    if det == 0:
        print("La matriz es singular, no tiene inversa.")
        doc = Document(geometry_options={"margin":"2.5cm"})
        doc.append(NoEscape(r"\section*{Matriz singular} $\det(A)=0$"))
        compilar(doc, salida)
        return
    C = matriz_cofactores(M)
    adj = transponer(C)
    inv = [[v/det for v in fila] for fila in adj]
    # Pasos de cofactores
    pasos_cof = []
    n = len(M)
    for i in range(n):
        for j in range(n):
            min_ij = menor(M, i, j)
            signo = Fraction(1) if (i+j)%2==0 else Fraction(-1)
            det_min, _ = determinante_gauss(min_ij)
            cof = signo * det_min
            pasos_cof.append((i,j,min_ij,signo,det_min,cof))
    # Documento
    doc = Document(geometry_options={"margin":"2.5cm"})
    for pkg, opt in [("amsmath",None),("amssymb",None),("fontenc","T1"),
                     ("inputenc","utf8"),("babel","spanish")]:
        if opt: doc.packages.append(Package(pkg, options=opt))
        else: doc.packages.append(Package(pkg))
    doc.preamble.append(NoEscape(r"""
\title{\textbf{Cálculo de la Matriz Inversa}\\[0.3em]\large Cofactores, Adjunta e Inversa}
\author{Diego Alexander Cuervo Padilla \\ Código: 2150049 \\ UFPS}
\date{\today}
"""))
    doc.append(NoEscape(r"\maketitle\tableofcontents\newpage"))
    with doc.create(Section("Fundamento teórico")):
        doc.append(NoEscape(r"$A^{-1} = \frac{1}{\det(A)}\text{adj}(A)$."))
    with doc.create(Section("Matriz original")):
        doc.append(NoEscape(r"\[ A = " + mat_tex(M) + r" \]"))
    with doc.create(Section("Determinante")):
        doc.append(NoEscape(r"\[ \det(A) = " + frac_tex(det) + r" \]"))
    with doc.create(Section("Matriz de cofactores")):
        for (i,j,min_ij,signo,det_min,cof) in pasos_cof:
            doc.append(NoEscape(rf"$C_{{{i+1}{j+1}}} = ({'+' if signo>0 else '-'})\det(M_{{{i+1}{j+1}}}) = {frac_tex(cof)}$\\"))
        doc.append(NoEscape(r"\[ C = " + mat_tex(C) + r" \]"))
    with doc.create(Section("Matriz adjunta (transpuesta de cofactores)")):
        doc.append(NoEscape(r"\[ \text{adj}(A) = " + mat_tex(adj) + r" \]"))
    with doc.create(Section("Matriz inversa")):
        doc.append(NoEscape(r"\[ A^{-1} = \frac{1}{" + frac_tex(det) + r"} \cdot " + mat_tex(adj) + r" = " + mat_tex(inv) + r" \]"))
    # Verificación
    prod = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                prod[i][j] += M[i][k] * inv[k][j]
    with doc.create(Section("Verificación")):
        doc.append(NoEscape(r"\[ A \cdot A^{-1} = " + mat_tex(M) + r" \cdot " + mat_tex(inv) + r" = " + mat_tex(prod) + r" = I_n \quad \checkmark \]"))
    compilar(doc, salida)

# ─────────────────────────────── MAIN ────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script unificado de Álgebra Lineal con PyLaTeX")
    subparsers = parser.add_subparsers(dest="modo", required=True, help="Elija una parte")

    # Subcomando matriz
    p1 = subparsers.add_parser("matriz", help="Generar matriz aleatoria")
    p1.add_argument("--tipo", required=True, choices=list(GENERADORES.keys()))
    p1.add_argument("--filas", type=int, default=3)
    p1.add_argument("--columnas", type=int, default=4)
    p1.add_argument("--salida", default="matriz_output")

    # Subcomando determinante
    p2 = subparsers.add_parser("determinante", help="Determinante por Gauss")
    p2.add_argument("--demo", action="store_true", help="Usar matriz demo 3x3")
    p2.add_argument("--salida", default="determinante_gauss")
    # Si no se pone --demo, será interactivo (no hace falta argumento extra)

    # Subcomando inversa
    p3 = subparsers.add_parser("inversa", help="Inversa por cofactores")
    p3.add_argument("--demo", action="store_true", help="Usar matriz demo 3x3")
    p3.add_argument("--salida", default="matriz_inversa")

    args = parser.parse_args()

    if args.modo == "matriz":
        parte1(args.tipo, args.filas, args.columnas, args.salida)
    elif args.modo == "determinante":
        parte2(interactivo=not args.demo, demo=args.demo, salida=args.salida)
    elif args.modo == "inversa":
        parte3(interactivo=not args.demo, demo=args.demo, salida=args.salida)

