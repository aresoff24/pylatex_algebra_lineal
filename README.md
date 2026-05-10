Álgebra Lineal con PyLaTeX
Proyecto académico de la asignatura Álgebra Lineal.
Tecnología en Analítica de Datos – Universidad Francisco de Paula Santander (UFPS)
Autor: Diego Alexander Cuervo Padilla | Código: 2150049
Docente: Karen Patricia Jaimes Vega

Descripción
Scripts en Python que utilizan PyLaTeX para generar documentos PDF con procedimientos de álgebra lineal documentados paso a paso. Se ofrecen dos modalidades:

Tres programas independientes, uno por cada tema.
Un programa unificado que integra las tres funcionalidades mediante subcomandos.


Archivos del repositorio
ArchivoDescripción01_matrices_aleatorias.pyGenera matrices de distintos tipos y produce un PDF explicativo02_determinante_gauss.pyCalcula el determinante por eliminación de Gauss con pasos detallados03_matriz_inversa.pyCalcula la inversa vía cofactores → adjunta → inversatarea_algebra_lineal.pyPrograma unificado con subcomandos matriz, determinante e inversaREADME.mdEste documento

Requisitos
bashpip install PyLaTeX
Además se necesita un compilador LaTeX instalado para generar el PDF:
SistemaOpción recomendadaWindowsMiKTeX o TeX LiveLinuxsudo apt install texlive-fullmacOSMacTeX

Si no se dispone de LaTeX local, cada script genera también un archivo .tex que puede compilarse en Overleaf.


Programas individuales
Parte 1 — Matrices aleatorias (01_matrices_aleatorias.py)
Tipos disponibles: fila, columna, cuadrada, rectangular, diagonal, triangular_sup, triangular_inf, identidad, nula, simetrica.
bashpython 01_matrices_aleatorias.py --tipo cuadrada --filas 3
python 01_matrices_aleatorias.py --tipo rectangular --filas 3 --columnas 5
python 01_matrices_aleatorias.py --tipo identidad --filas 4 --salida mi_identidad
Parte 2 — Determinante por Gauss (02_determinante_gauss.py)
bash# Modo interactivo (ingresa la matriz por consola)
python 02_determinante_gauss.py

# Modo demostración con matriz 3×3 de resultado conocido
python 02_determinante_gauss.py --demo

# Salida con nombre personalizado
python 02_determinante_gauss.py --demo --salida det_ejemplo
Ejemplo de entrada interactiva:
Ingrese el tamaño n (matriz n×n): 3
Fila 1: 2 1 -1
Fila 2: -3 -1 2
Fila 3: -2 1 2
Parte 3 — Matriz inversa (03_matriz_inversa.py)
bash# Modo interactivo
python 03_matriz_inversa.py

# Modo demostración
python 03_matriz_inversa.py --demo

# Salida con nombre personalizado
python 03_matriz_inversa.py --demo --salida inversa_ejemplo

Programa unificado (tarea_algebra_lineal.py)
Reúne las tres partes en un solo script controlado por subcomandos.
bash# Subcomando: matriz
python tarea_algebra_lineal.py matriz --tipo cuadrada --filas 3
python tarea_algebra_lineal.py matriz --tipo rectangular --filas 3 --columnas 5
python tarea_algebra_lineal.py matriz --tipo identidad --filas 4 --salida mi_identidad

# Subcomando: determinante
python tarea_algebra_lineal.py determinante
python tarea_algebra_lineal.py determinante --demo
python tarea_algebra_lineal.py determinante --demo --salida det_ejemplo

# Subcomando: inversa
python tarea_algebra_lineal.py inversa
python tarea_algebra_lineal.py inversa --demo
python tarea_algebra_lineal.py inversa --demo --salida inversa_ejemplo

Contenido de cada PDF generado
Parte 1 — Matrices aleatorias

Definición del tipo de matriz solicitado
Matriz generada en notación LaTeX
Fragmento del código Python utilizado

Parte 2 — Determinante (Gauss)

Fundamento teórico de la eliminación de Gauss
Matriz original
Todos los pasos de eliminación (intercambios de fila y operaciones de reducción)
Resultado final en recuadro
Conclusión sobre invertibilidad

Parte 3 — Matriz inversa (cofactores)

Fundamento teórico del método de cofactores
Determinante calculado internamente por Gauss
Cada cofactor con su menor y signo correspondiente
Matriz de cofactores completa C
Matriz adjunta adj(A) = C^T
Matriz inversa A^{-1} = adj(A) / det(A)
Verificación: A · A^{-1} = I_n


Estructura del repositorio
tarea-matrices-pylatex/
├── 01_matrices_aleatorias.py
├── 02_determinante_gauss.py
├── 03_matriz_inversa.py
├── tarea_algebra_lineal.py
└── README.md

Notas técnicas

Los cálculos internos usan fractions.Fraction para aritmética exacta, sin errores de punto flotante.
PyLaTeX construye el .tex y llama a pdflatex automáticamente.
Los archivos .tex intermedios se conservan (clean_tex=False) para revisión o compilación manual.
Las matrices aceptan entradas fraccionarias, por ejemplo: 1/2 3/4 -1.


Licencia
Proyecto de uso académico. Puede copiarse, modificarse y distribuirse libremente con fines educativos.