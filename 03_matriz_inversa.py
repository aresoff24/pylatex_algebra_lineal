#!/usr/bin/env python3
"""
=============================================================================
TAREA ÁLGEBRA LINEAL - PARTE 3
Cálculo de la Matriz Inversa (Cofactores → Adjunta → Inversa) con PyLaTeX
Autor : Diego Alexander Cuervo Padilla  |  Código: 2150049
Curso : Tecnología en Analítica de Datos - UFPS
=============================================================================
Uso:
  python 03_matriz_inversa.py
  python 03_matriz_inversa.py --demo
"""

import argparse
from fractions import Fraction
from pylatex import Document, Section, Subsection, NoEscape, Package


# ─────────────────────────────────────────────────────────────────────────────
# LECTURA DE MATRIZ DESDE CONSOLA
# ─────────────────────────────────────────────────────────────────────────────

def leer_matriz():
    """Lee una matriz n×n desde la consola usando Fraction para precisión exacta."""
    n = int(input("Ingrese el tamaño n (matriz n×n): "))
    print(f"Ingrese la matriz {n}×{n} fila por fila, separando valores con espacios:")
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
    """Matriz de demostración 3×3 con inversa no trivial."""
    # A = [[1,2,0],[0,1,0],[0,0,1]]
    # Su inversa es [[1,-2,0],[0,1,0],[0,0,1]]
    return [
        [Fraction(1), Fraction(2), Fraction(0)],
        [Fraction(0), Fraction(1), Fraction(0)],
        [Fraction(0), Fraction(0), Fraction(1)],
    ]


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS LaTeX
# ─────────────────────────────────────────────────────────────────────────────

def frac_tex(f: Fraction) -> str:
    """Convierte una Fraction a notación LaTeX compacta."""
    if f.denominator == 1:
        return str(f.numerator)
    if f < 0:
        return rf"-\frac{{{abs(f.numerator)}}}{{{f.denominator}}}"
    return rf"\frac{{{f.numerator}}}{{{f.denominator}}}"


def mat_tex(M):
    """Convierte una lista de listas de Fraction a LaTeX bmatrix."""
    filas = [" & ".join(frac_tex(v) for v in fila) for fila in M]
    return r"\begin{bmatrix}" + r" \\ ".join(filas) + r"\end{bmatrix}"


# ─────────────────────────────────────────────────────────────────────────────
# DETERMINANTE POR GAUSS (con pivoteo parcial)
# ─────────────────────────────────────────────────────────────────────────────

def determinante_gauss(M_orig):
    """
    Calcula el determinante de la matriz M (list of lists de Fraction)
    usando eliminación gaussiana con pivoteo parcial (máximo valor absoluto).
    Retorna un Fraction.
    """
    n = len(M_orig)
    M = [fila[:] for fila in M_orig]   # copia profunda
    signo = Fraction(1)

    for col in range(n):
        # Buscar el máximo valor absoluto en la columna actual (pivoteo parcial)
        max_val = Fraction(0)
        pivote_fila = None
        for f in range(col, n):
            abs_val = abs(M[f][col])
            if abs_val > max_val:
                max_val = abs_val
                pivote_fila = f

        if pivote_fila is None or max_val == 0:
            # Columna de ceros → determinante 0
            return Fraction(0)

        # Intercambiar si es necesario
        if pivote_fila != col:
            M[col], M[pivote_fila] = M[pivote_fila], M[col]
            signo *= Fraction(-1)

        pivote = M[col][col]

        # Eliminación hacia adelante
        for fila in range(col + 1, n):
            if M[fila][col] == 0:
                continue
            factor = M[fila][col] / pivote
            for j in range(col, n):
                M[fila][j] -= factor * M[col][j]

    # Producto de la diagonal, multiplicado por el signo
    prod = Fraction(1)
    for i in range(n):
        prod *= M[i][i]
    return signo * prod


# ─────────────────────────────────────────────────────────────────────────────
# MENOR Y COFACTOR
# ─────────────────────────────────────────────────────────────────────────────

def menor(M, fila_exc, col_exc):
    """Devuelve la submatriz (n-1)×(n-1) eliminando fila y columna dadas."""
    return [
        [M[i][j] for j in range(len(M[0])) if j != col_exc]
        for i in range(len(M)) if i != fila_exc
    ]


def cofactor(M, i, j):
    """Cofactor C_{ij} = (-1)^{i+j} * det(Menor_ij)."""
    signo = Fraction(1) if (i + j) % 2 == 0 else Fraction(-1)
    return signo * determinante_gauss(menor(M, i, j))


# ─────────────────────────────────────────────────────────────────────────────
# PASOS COMPLETOS DE LA INVERSA
# ─────────────────────────────────────────────────────────────────────────────

def pasos_inversa(M):
    """
    Calcula todos los pasos intermedios y devuelve un diccionario con:
      det, C, adj, inv, pasos_cof
    """
    n = len(M)
    det = determinante_gauss(M)

    pasos_cof = []
    C = []
    for i in range(n):
        fila_c = []
        for j in range(n):
            min_ij = menor(M, i, j)
            det_min = determinante_gauss(min_ij)
            signo = Fraction(1) if (i + j) % 2 == 0 else Fraction(-1)
            cof_ij = signo * det_min
            fila_c.append(cof_ij)
            pasos_cof.append({
                "i": i, "j": j,
                "menor": min_ij,
                "signo": signo,
                "det_menor": det_min,
                "cof": cof_ij,
            })
        C.append(fila_c)

    adj = [list(fila) for fila in zip(*C)]   # transpuesta (más claro que transponer)

    if det == 0:
        inv = None
    else:
        inv = [[v / det for v in fila] for fila in adj]

    return {
        "det": det,
        "C": C,
        "adj": adj,
        "inv": inv,
        "pasos_cof": pasos_cof,
        "n": n
    }


# ─────────────────────────────────────────────────────────────────────────────
# GENERACIÓN DEL DOCUMENTO PyLaTeX
# ─────────────────────────────────────────────────────────────────────────────

def generar_documento(M_orig, resultado, nombre_salida="matriz_inversa"):
    n = resultado["n"]
    det = resultado["det"]
    C = resultado["C"]
    adj = resultado["adj"]
    inv = resultado["inv"]
    pasos_cof = resultado["pasos_cof"]

    doc = Document(geometry_options={"margin": "2.5cm"})
    # Paquetes necesarios
    for pkg, opt in [
        ("amsmath", None), ("amssymb", None),
        ("fontenc", "T1"), ("inputenc", "utf8"),
        ("babel", "spanish"), ("xcolor", None), ("booktabs", None),
    ]:
        if opt:
            doc.packages.append(Package(pkg, options=opt))
        else:
            doc.packages.append(Package(pkg))

    doc.preamble.append(NoEscape(r"""
\title{\textbf{Cálculo de la Matriz Inversa}\\[0.3em]
       \large Cofactores $\rightarrow$ Adjunta $\rightarrow$ Inversa}
\author{Diego Alexander Cuervo Padilla \\ Código: 2150049 \\
        Tecnología en Analítica de Datos --- UFPS}
\date{\today}
"""))
    doc.append(NoEscape(r"\maketitle\tableofcontents\newpage"))

    # Sección 1: Teoría
    with doc.create(Section("Fundamento teórico")):
        doc.append(NoEscape(r"""
Dada una matriz cuadrada $A$ de orden $n$, su \textbf{inversa} $A^{-1}$ existe
si y solo si $\det(A) \neq 0$. El procedimiento clásico es:
\begin{enumerate}
  \item Calcular $\det(A)$.
  \item Calcular la \textbf{matriz de cofactores} $C$, donde
        $C_{ij} = (-1)^{i+j} M_{ij}$ y $M_{ij}$ es el determinante
        del menor obtenido al eliminar la fila $i$ y la columna $j$.
  \item Obtener la \textbf{matriz adjunta}: $\text{adj}(A) = C^{T}$.
  \item Calcular la inversa:
        $A^{-1} = \dfrac{1}{\det(A)} \, \text{adj}(A)$.
\end{enumerate}
Se puede verificar el resultado comprobando que $A \cdot A^{-1} = I_n$.
"""))

    # Sección 2: Matriz original
    with doc.create(Section("Matriz original")):
        doc.append(NoEscape(rf"Se analiza la siguiente matriz cuadrada de orden ${n}$:"))
        doc.append(NoEscape(r"\[ A = " + mat_tex(M_orig) + r" \]"))

    # Sección 3: Determinante
    with doc.create(Section("Paso 1 — Cálculo del determinante")):
        doc.append(NoEscape(r"Usando eliminación de Gauss con pivoteo parcial:"))
        doc.append(NoEscape(r"\[ \det(A) = " + frac_tex(det) + r" \]"))
        if det == 0:
            doc.append(NoEscape(r"\textbf{La matriz es singular: no tiene inversa.}"))
            # Generar PDF (o .tex) y salir
            doc.generate_tex(nombre_salida)
            try:
                doc.generate_pdf(nombre_salida, clean_tex=False, compiler="pdflatex")
                print(f"[OK] PDF generado: {nombre_salida}.pdf (matriz singular)")
            except Exception as e:
                print(f"No se pudo compilar el PDF: {e}")
                print(f"El archivo .tex está disponible: {nombre_salida}.tex")
            return

    # Sección 4: Cofactores (uno a uno)
    with doc.create(Section("Paso 2 — Matriz de cofactores")):
        doc.append(NoEscape(
            r"Calculamos $C_{ij} = (-1)^{i+j} \cdot \det(M_{ij})$ para cada posición:"
        ))
        for paso in pasos_cof:
            i, j = paso["i"], paso["j"]
            signo_str = "+" if paso["signo"] > 0 else "-"
            with doc.create(Subsection(f"Cofactor $C_{{{i+1}{j+1}}}$")):
                doc.append(NoEscape(
                    rf"Eliminamos la fila {i+1} y la columna {j+1}. "
                    rf"El signo es $(-1)^{{{i+1}+{j+1}}} = {signo_str}1$."
                ))
                # Mostrar el menor
                doc.append(NoEscape(
                    rf"\[ M_{{{i+1}{j+1}}} = " + mat_tex(paso["menor"])
                    + r" \]"
                ))
                doc.append(NoEscape(
                    rf"\[ \det(M_{{{i+1}{j+1}}}) = "
                    + frac_tex(paso["det_menor"])
                    + r" \]"
                ))
                doc.append(NoEscape(
                    rf"\[ C_{{{i+1}{j+1}}} = ({signo_str}1) \cdot "
                    + frac_tex(paso["det_menor"])
                    + r" = " + frac_tex(paso["cof"]) + r" \]"
                ))

        # Resumen: matriz C completa
        doc.append(NoEscape(r"La \textbf{matriz de cofactores} completa es:"))
        doc.append(NoEscape(r"\[ C = " + mat_tex(C) + r" \]"))

    # Sección 5: Adjunta
    with doc.create(Section("Paso 3 — Matriz adjunta")):
        doc.append(NoEscape(
            r"La adjunta es la transpuesta de la matriz de cofactores: "
            r"$\text{adj}(A) = C^{T}$."
        ))
        doc.append(NoEscape(r"\[ \text{adj}(A) = C^T = " + mat_tex(adj) + r" \]"))

    # Sección 6: Inversa
    with doc.create(Section("Paso 4 — Matriz inversa")):
        doc.append(NoEscape(r"Dividimos la adjunta entre el determinante:"))
        doc.append(NoEscape(
            r"\[ A^{-1} = \frac{1}{\det(A)} \cdot \text{adj}(A) "
            r"= \frac{1}{" + frac_tex(det) + r"} \cdot "
            + mat_tex(adj) + r" \]"
        ))
        doc.append(NoEscape(r"\[ \boxed{ A^{-1} = " + mat_tex(inv) + r" } \]"))

    # Sección 7: Verificación
    with doc.create(Section("Verificación: $A \\cdot A^{-1} = I_n$")):
        # Calcular A * A^{-1}
        prod = [[Fraction(0) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    prod[i][j] += M_orig[i][k] * Fraction(inv[k][j])
        doc.append(NoEscape(r"Comprobamos multiplicando $A \cdot A^{-1}$:"))
        doc.append(NoEscape(
            r"\[ A \cdot A^{-1} = " + mat_tex(M_orig) + r" \cdot "
            + mat_tex(inv) + r" = " + mat_tex(prod)
            + r" = I_{" + str(n) + r"} \quad \checkmark \]"
        ))

    # Generar archivos
    doc.generate_tex(nombre_salida)
    try:
        doc.generate_pdf(nombre_salida, clean_tex=False, compiler="pdflatex")
        print(f"[OK] PDF generado: {nombre_salida}.pdf")
    except Exception as e:
        print(f"No se pudo compilar el PDF: {e}")
        print(f"El archivo .tex está disponible: {nombre_salida}.tex")


# ─────────────────────────────────────────────────────────────────────────────
# PUNTO DE ENTRADA
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Calcula la inversa de una matriz y genera PDF LaTeX paso a paso."
    )
    parser.add_argument("--demo", action="store_true",
                        help="Usar matriz de demostración 3×3")
    parser.add_argument("--salida", default="matriz_inversa",
                        help="Nombre base del PDF de salida")
    args = parser.parse_args()

    if args.demo:
        M = matriz_demo()
        print("Usando matriz de demostración:")
        for fila in M:
            print("  ", [str(v) for v in fila])
    else:
        M = leer_matriz()

    resultado = pasos_inversa(M)
    generar_documento(M, resultado, args.salida)