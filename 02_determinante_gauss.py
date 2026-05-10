#!/usr/bin/env python3
"""
=============================================================================
TAREA ÁLGEBRA LINEAL - PARTE 2
Cálculo de Determinante por eliminación de Gauss con PyLaTeX
Autor : Diego Alexander Cuervo Padilla  |  Código: 2150049
Curso : Tecnología en Analítica de Datos - UFPS
=============================================================================
Lee una matriz cuadrada, calcula su determinante por el método de Gauss
y genera un PDF LaTeX mostrando cada paso de la eliminación.

Uso:
  python 02_determinante_gauss.py
  (el programa pedirá la matriz por consola)

  O con matriz hardcodeada para prueba rápida:
  python 02_determinante_gauss.py --demo
"""

import argparse
from fractions import Fraction
from pylatex import Document, Section, Subsection, Math, NoEscape, Package


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
                    print(f"  ⚠ Se esperaban {n} valores, ingresó {len(fila)}. Intente de nuevo.")
                    continue
                M.append(fila)
                break
            except ValueError:
                print("  ⚠ Solo números (enteros o fracciones como 3/4). Intente de nuevo.")
    return M


def matriz_demo():
    """Matriz de demostración 3×3 con resultado conocido."""
    return [
        [Fraction(2),  Fraction(1),  Fraction(-1)],
        [Fraction(-3), Fraction(-1), Fraction(2)],
        [Fraction(-2), Fraction(1),  Fraction(2)],
    ]


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS LaTeX
# ─────────────────────────────────────────────────────────────────────────────

def frac_tex(f: Fraction) -> str:
    """Convierte una Fraction a notación LaTeX compacta."""
    if f.denominator == 1:
        return str(f.numerator)
    # Si es negativo, extraemos el signo
    if f < 0:
        return rf"-\frac{{{abs(f.numerator)}}}{{{f.denominator}}}"
    return rf"\frac{{{f.numerator}}}{{{f.denominator}}}"


def matriz_a_tex(M):
    """Convierte una lista de listas de Fraction a LaTeX bmatrix."""
    filas = []
    for fila in M:
        filas.append(" & ".join(frac_tex(v) for v in fila))
    return r"\begin{bmatrix}" + r" \\ ".join(filas) + r"\end{bmatrix}"


# ─────────────────────────────────────────────────────────────────────────────
# ALGORITMO: ELIMINACIÓN DE GAUSS CON REGISTRO DE PASOS
# ─────────────────────────────────────────────────────────────────────────────

def gauss_determinante(M_original):
    """
    Calcula el determinante de M por eliminación gaussiana con pivoteo parcial
    (máximo valor absoluto de la columna). Devuelve (det: Fraction, pasos: list[dict])
    donde cada dict tiene:
      - descripcion : str  descripción textual
      - matriz      : list[list[Fraction]]  estado de la matriz tras el paso
      - operacion   : str  símbolo de la operación (LaTeX)
      - factor_det  : Fraction  factor acumulado del determinante
    """
    n = len(M_original)
    M = [fila[:] for fila in M_original]   # copia profunda con Fraction
    pasos = []
    factor_det = Fraction(1)      # acumulador de signos por intercambios
    intercambios = 0              # solo para mostrar en los mensajes

    for col in range(n):
        # ── Pivoteo parcial: buscar el elemento con mayor valor absoluto en la columna col ──
        max_val = 0
        pivote_fila = None
        for f in range(col, n):
            abs_val = abs(M[f][col])
            if abs_val > max_val:
                max_val = abs_val
                pivote_fila = f

        if pivote_fila is None or max_val == 0:
            # Toda la columna tiene ceros → determinante = 0
            pasos.append({
                "descripcion": (
                    rf"Todos los elementos de la columna {col+1} bajo la fila {col+1} "
                    r"son cero $\Rightarrow \det(A) = 0$."
                ),
                "matriz": [fila[:] for fila in M],
                "operacion": "",
                "factor_det": Fraction(0),
            })
            return Fraction(0), pasos

        # ── Intercambio de filas si el pivote no está en la diagonal ──
        if pivote_fila != col:
            M[col], M[pivote_fila] = M[pivote_fila], M[col]
            factor_det *= Fraction(-1)
            intercambios += 1
            pasos.append({
                "descripcion": (
                    rf"Intercambiamos $F_{{{col+1}}}$ y $F_{{{pivote_fila+1}}}$ "
                    rf"para colocar el máximo de la columna como pivote. "
                    rf"El determinante cambia de signo."
                ),
                "matriz": [fila[:] for fila in M],
                "operacion": rf"F_{{{col+1}}} \leftrightarrow F_{{{pivote_fila+1}}}",
                "factor_det": factor_det,
            })

        pivote = M[col][col]

        # ── Eliminación de la columna bajo el pivote ──
        for fila in range(col + 1, n):
            if M[fila][col] == 0:
                continue
            factor = M[fila][col] / pivote
            operacion_tex = (
                rf"F_{{{fila+1}}} \leftarrow F_{{{fila+1}}} "
                rf"- {frac_tex(factor)} \cdot F_{{{col+1}}}"
            )
            for j in range(col, n):
                M[fila][j] -= factor * M[col][j]

            pasos.append({
                "descripcion": (
                    rf"Eliminamos el elemento en la posición $({fila+1},{col+1})$ "
                    rf"usando el pivote $p = {frac_tex(pivote)}$."
                ),
                "matriz": [fila_[:] for fila_ in M],
                "operacion": operacion_tex,
                "factor_det": factor_det,
            })

    # ── Cálculo final del determinante ──
    diag_product = Fraction(1)
    diag_terms = []
    for i in range(n):
        diag_product *= M[i][i]
        diag_terms.append(frac_tex(M[i][i]))

    det = factor_det * diag_product
    signo_tex = f"({frac_tex(factor_det)})" if factor_det < 0 else frac_tex(factor_det)
    pasos.append({
        "descripcion": (
            r"La matriz está en forma escalonada. El determinante es el "
            f"producto de los elementos diagonales multiplicado por el "
            f"factor de intercambios {signo_tex}."
        ),
        "matriz": [fila[:] for fila in M],
        "operacion": (
            r"\det(A) = "
            + frac_tex(factor_det)
            + r" \cdot \left("
            + r" \cdot ".join(diag_terms)
            + r"\right) = "
            + frac_tex(det)
        ),
        "factor_det": det,
    })

    return det, pasos


# ─────────────────────────────────────────────────────────────────────────────
# GENERACIÓN DEL DOCUMENTO PyLaTeX
# ─────────────────────────────────────────────────────────────────────────────

def generar_documento(M_original, det, pasos, nombre_salida="determinante_gauss"):
    n = len(M_original)
    doc = Document(geometry_options={"margin": "2.5cm"})
    doc.packages.append(Package("amsmath"))
    doc.packages.append(Package("amssymb"))
    doc.packages.append(Package("fontenc", options="T1"))
    doc.packages.append(Package("inputenc", options="utf8"))
    doc.packages.append(Package("babel", options="spanish"))

    doc.preamble.append(NoEscape(r"""
\title{\textbf{Cálculo de Determinante}\\[0.3em]
       \large Método de Eliminación de Gauss}
\author{Diego Alexander Cuervo Padilla \\ Código: 2150049 \\
        Tecnología en Analítica de Datos --- UFPS}
\date{\today}
"""))
    doc.append(NoEscape(r"\maketitle\tableofcontents\newpage"))

    # ── Sección 1: Fundamento teórico ──
    with doc.create(Section("Fundamento teórico")):
        doc.append(NoEscape(r"""
El método de eliminación de Gauss transforma la matriz $A$ en una matriz
triangular superior $U$ mediante operaciones elementales de fila. Dado que:
\begin{itemize}
  \item Intercambiar dos filas cambia el signo del determinante.
  \item Sumar un múltiplo de una fila a otra \textbf{no} altera el determinante.
\end{itemize}
El determinante de $A$ es:
\[
  \det(A) = (-1)^{s} \cdot u_{11} \cdot u_{22} \cdots u_{nn}
\]
donde $s$ es el número de intercambios realizados y $u_{ii}$ son los
elementos de la diagonal de $U$.
"""))

    # ── Sección 2: Matriz original ──
    with doc.create(Section("Matriz original")):
        doc.append(NoEscape(
            rf"Se analiza la siguiente matriz cuadrada de orden ${n}$:\n"
        ))
        doc.append(NoEscape(r"\[ A = " + matriz_a_tex(M_original) + r" \]"))

    # ── Sección 3: Procedimiento paso a paso ──
    with doc.create(Section("Procedimiento de eliminación de Gauss")):
        for k, paso in enumerate(pasos, start=1):
            with doc.create(Subsection(f"Paso {k}")):
                doc.append(NoEscape(paso["descripcion"]))
                if paso["operacion"]:
                    doc.append(NoEscape(r"\[ " + paso["operacion"] + r" \]"))
                doc.append(NoEscape(
                    r"\[ M^{(" + str(k) + r")} = "
                    + matriz_a_tex(paso["matriz"])
                    + r" \]"
                ))

    # ── Sección 4: Resultado ──
    with doc.create(Section("Resultado")):
        doc.append(NoEscape(
            r"\[ \boxed{\det(A) = " + frac_tex(det) + r"} \]"
        ))
        if det == 0:
            doc.append(NoEscape(
                r"\textbf{Conclusión:} La matriz es singular (no invertible)."
            ))
        else:
            doc.append(NoEscape(
                r"\textbf{Conclusión:} La matriz es no singular (invertible)."
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
        description="Calcula determinante por Gauss y genera PDF LaTeX."
    )
    parser.add_argument("--demo", action="store_true",
                        help="Usar matriz de demostración 3×3")
    parser.add_argument("--salida", default="determinante_gauss",
                        help="Nombre base del PDF de salida")
    args = parser.parse_args()

    if args.demo:
        M = matriz_demo()
        print("Usando matriz de demostración:")
        for fila in M:
            print("  ", [str(v) for v in fila])
    else:
        M = leer_matriz()

    det, pasos = gauss_determinante(M)
    print(f"\nDeterminante calculado: {det}")
    generar_documento(M, det, pasos, args.salida)