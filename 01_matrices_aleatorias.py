#!/usr/bin/env python3
"""
=============================================================================
TAREA ÁLGEBRA LINEAL – PARTE 1
Generación de matrices aleatorias con PyLaTeX
Autor : Diego Alexander Cuervo Padilla  |  Código: 2150049
Curso : Tecnología en Analítica de Datos – UFPS
=============================================================================
Uso:
  python matriz_aleatoria.py --tipo cuadrada --filas 3
  python matriz_aleatoria.py --tipo rectangular --filas 3 --columnas 4
  python matriz_aleatoria.py --tipo identidad --filas 4
"""

import argparse
import random
from pylatex import Document, Section, Math, NoEscape, Package
from pylatex.utils import italic


 
def _rand(low=-9, high=9):
    """Entero aleatorio distinto de cero para mayor claridad."""
    v = 0
    while v == 0:
        v = random.randint(low, high)
    return v


def matriz_fila(n=4):
    """Matriz fila: 1 × n con valores aleatorios."""
    return [[_rand() for _ in range(n)]]


def matriz_columna(m=4):
    """Matriz columna: m × 1 con valores aleatorios."""
    return [[_rand()] for _ in range(m)]


def matriz_cuadrada(n=3):
    """Matriz cuadrada: n × n con valores aleatorios."""
    return [[_rand() for _ in range(n)] for _ in range(n)]


def matriz_rectangular(m=3, n=4):
    """Matriz rectangular: m × n con valores aleatorios."""
    return [[_rand() for _ in range(n)] for _ in range(m)]


def matriz_diagonal(n=3):
    """Matriz diagonal: solo la diagonal principal es aleatoria."""
    M = [[0] * n for _ in range(n)]
    for i in range(n):
        M[i][i] = _rand()
    return M


def matriz_triangular_superior(n=3):
    """Triangular superior: ceros debajo de la diagonal."""
    M = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            M[i][j] = _rand()
    return M


def matriz_triangular_inferior(n=3):
    """Triangular inferior: ceros encima de la diagonal."""
    M = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(0, i + 1):
            M[i][j] = _rand()
    return M


def matriz_identidad(n=3):
    """Matriz identidad: unos en la diagonal, ceros en el resto."""
    M = [[0] * n for _ in range(n)]
    for i in range(n):
        M[i][i] = 1
    return M


def matriz_nula(m=3, n=3):
    """Matriz nula: todos los elementos son cero."""
    return [[0] * n for _ in range(m)]


def matriz_simetrica(n=3):
    """Matriz simétrica: A[i][j] = A[j][i]."""
    M = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            v = _rand()
            M[i][j] = v
            M[j][i] = v
    return M


# Mapa tipo → función generadora
GENERADORES = {
    "fila":           lambda r, c: matriz_fila(c),
    "columna":        lambda r, c: matriz_columna(r),
    "cuadrada":       lambda r, c: matriz_cuadrada(r),
    "rectangular":    lambda r, c: matriz_rectangular(r, c),
    "diagonal":       lambda r, c: matriz_diagonal(r),
    "triangular_sup": lambda r, c: matriz_triangular_superior(r),
    "triangular_inf": lambda r, c: matriz_triangular_inferior(r),
    "identidad":      lambda r, c: matriz_identidad(r),
    "nula":           lambda r, c: matriz_nula(r, c),
    "simetrica":      lambda r, c: matriz_simetrica(r),
}

# Descripciones para el documento
DESCRIPCIONES = {
    "fila": r"Una \textbf{matriz fila} (o vector fila) tiene una sola fila y $n$ columnas: dimensión $1 \times n$.",
    "columna": r"Una \textbf{matriz columna} (o vector columna) tiene $m$ filas y una sola columna: dimensión $m \times 1$.",
    "cuadrada": r"Una \textbf{matriz cuadrada} tiene el mismo número de filas y columnas: dimensión $n \times n$.",
    "rectangular": r"Una \textbf{matriz rectangular} tiene $m$ filas y $n$ columnas con $m \neq n$.",
    "diagonal": r"Una \textbf{matriz diagonal} tiene ceros en todas las posiciones excepto en la diagonal principal.",
    "triangular_sup": r"Una \textbf{matriz triangular superior} tiene ceros en todas las posiciones debajo de la diagonal principal.",
    "triangular_inf": r"Una \textbf{matriz triangular inferior} tiene ceros en todas las posiciones por encima de la diagonal principal.",
    "identidad": r"La \textbf{matriz identidad} $I_n$ tiene unos en la diagonal principal y ceros en las demás posiciones.",
    "nula": r"La \textbf{matriz nula} tiene todos sus elementos iguales a cero.",
    "simetrica": r"Una \textbf{matriz simétrica} cumple $A = A^T$, es decir, $a_{ij} = a_{ji}$ para todo $i, j$.",
}


def lista_a_latex(M):
    """Convierte una lista de listas en código LaTeX bmatrix."""
    filas_tex = [" & ".join(str(v) for v in fila) for fila in M]
    contenido = r" \\ ".join(filas_tex)
    return r"\begin{bmatrix}" + contenido + r"\end{bmatrix}"


def generar_documento(tipo, filas, columnas, nombre_salida="matriz_output"):
    """Crea un documento LaTeX con la matriz aleatoria del tipo solicitado."""
    generador = GENERADORES[tipo]
    M = generador(filas, columnas)
    m, n = len(M), len(M[0])

    doc = Document(geometry_options={"margin": "2.5cm"})
    doc.packages.append(Package("amsmath"))
    doc.packages.append(Package("amssymb"))
    doc.packages.append(Package("fontenc", options="T1"))
    doc.packages.append(Package("inputenc", options="utf8"))
    doc.packages.append(Package("babel", options="spanish"))

    # Título y autor
    doc.preamble.append(NoEscape(r"""
\title{\textbf{Generación de Matrices Aleatorias}\\[0.3em]
       \large Tipo: """ + tipo.replace("_", r"\_") + r"""}
\author{Diego Alexander Cuervo Padilla \\ Código: 2150049 \\
        Tecnología en Analítica de Datos --- UFPS}
\date{\today}
"""))
    doc.append(NoEscape(r"\maketitle"))
    doc.append(NoEscape(r"\tableofcontents\newpage"))

    # Sección 1: Definición
    with doc.create(Section("Definición del tipo de matriz")):
        doc.append(NoEscape(DESCRIPCIONES[tipo]))

    # Sección 2: Matriz generada
    with doc.create(Section("Matriz generada aleatoriamente")):
        doc.append(NoEscape(
            rf"Se generó una matriz de tipo \textbf{{{tipo.replace('_', ' ')}}} "
            rf"de dimensión ${m} \times {n}$:"
        ))
        doc.append(NoEscape(r"\[" + lista_a_latex(M) + r"\]"))

    # Sección 3: Código Python de ejemplo
    with doc.create(Section("Código Python utilizado")):
        doc.append(NoEscape(r"""
El siguiente fragmento muestra la función que genera este tipo de matriz:

\begin{verbatim}
""" + _codigo_funcion(tipo) + r"""
\end{verbatim}
"""))

    # Generar .tex y .pdf
    doc.generate_tex(nombre_salida)
    try:
        doc.generate_pdf(nombre_salida, clean_tex=False, compiler="pdflatex")
        print(f"[OK] PDF generado: {nombre_salida}.pdf")
        print(f"     Archivo .tex: {nombre_salida}.tex")
    except Exception as e:
        print(f"No se pudo compilar el PDF: {e}")
        print(f"El archivo .tex está disponible: {nombre_salida}.tex")


def _codigo_funcion(tipo):
    """Devuelve un fragmento de código representativo de la matriz."""
    snippets = {
        "fila": "def matriz_fila(n=4):\n    return [[random.randint(-9,9) for _ in range(n)]]",
        "columna": "def matriz_columna(m=4):\n    return [[random.randint(-9,9)] for _ in range(m)]",
        "cuadrada": "def matriz_cuadrada(n=3):\n    return [[random.randint(-9,9) for _ in range(n)] for _ in range(n)]",
        "rectangular": "def matriz_rectangular(m=3, n=4):\n    return [[random.randint(-9,9) for _ in range(n)] for _ in range(m)]",
        "diagonal": "def matriz_diagonal(n=3):\n    M = [[0]*n for _ in range(n)]\n    for i in range(n): M[i][i] = random.randint(-9,9)\n    return M",
        "triangular_sup": "def matriz_triangular_superior(n=3):\n    M = [[0]*n for _ in range(n)]\n    for i in range(n):\n        for j in range(i, n): M[i][j] = random.randint(-9,9)\n    return M",
        "triangular_inf": "def matriz_triangular_inferior(n=3):\n    M = [[0]*n for _ in range(n)]\n    for i in range(n):\n        for j in range(0, i+1): M[i][j] = random.randint(-9,9)\n    return M",
        "identidad": "def matriz_identidad(n=3):\n    M = [[0]*n for _ in range(n)]\n    for i in range(n): M[i][i] = 1\n    return M",
        "nula": "def matriz_nula(m=3, n=3):\n    return [[0]*n for _ in range(m)]",
        "simetrica": "def matriz_simetrica(n=3):\n    M = [[0]*n for _ in range(n)]\n    for i in range(n):\n        for j in range(i, n):\n            v = random.randint(-9,9)\n            M[i][j] = M[j][i] = v\n    return M",
    }
    return snippets.get(tipo, "# consultar archivo fuente")


# ─────────────────────────────────────────────────────────────────────────────
# PUNTO DE ENTRADA
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Genera un PDF LaTeX con una matriz aleatoria del tipo dado."
    )
    parser.add_argument(
        "--tipo", required=True,
        choices=list(GENERADORES.keys()),
        help="Tipo de matriz a generar"
    )
    parser.add_argument("--filas", type=int, default=3, help="Número de filas (n si cuadrada)")
    parser.add_argument("--columnas", type=int, default=4, help="Número de columnas")
    parser.add_argument("--salida", default="matriz_output", help="Nombre base del PDF de salida")
    args = parser.parse_args()

    generar_documento(args.tipo, args.filas, args.columnas, args.salida)