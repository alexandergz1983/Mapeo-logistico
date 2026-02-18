import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # Import necesario para gráficas 3D en matplotlib

# ------------------------------------------------------------
# 1) MAPA LOGÍSTICO Y DIAGRAMA DE BIFURCACIONES
# ------------------------------------------------------------
def logistic_map(x, r):
    """Función del mapa logístico: x_{n+1} = r * x_n * (1 - x_n)."""
    return r * x * (1 - x)

def generar_bifurcacion(r_min=2.4, r_max=4.0, steps=800, discard=200, keep=100):
    """
    Genera puntos (r, x) para el diagrama de bifurcación del mapa logístico.
    - r_min, r_max: rango de r
    - steps: número de subdivisiones de r
    - discard: iteraciones que se descartan (transitorio)
    - keep: iteraciones que se guardan (estacionario)
    Retorna:
      - bif_r: array con los valores de r repetidos
      - bif_x: array con las órbitas x
    """
    r_values = np.linspace(r_min, r_max, steps)
    bif_r = []
    bif_x = []
    
    for r in r_values:
        x = 0.5  # Valor inicial
        # Descartamos el transitorio
        for _ in range(discard):
            x = logistic_map(x, r)
        # Guardamos las iteraciones "estacionarias"
        for _ in range(keep):
            x = logistic_map(x, r)
            bif_r.append(r)
            bif_x.append(x)
    
    return np.array(bif_r), np.array(bif_x)

# ------------------------------------------------------------
# 2) CONJUNTO DE MANDELBROT (2D)
# ------------------------------------------------------------
def mandelbrot_set(xmin=-2.0, xmax=1.0, ymin=-1.5, ymax=1.5,
                   width=600, height=400, max_iter=100):
    """
    Calcula el conjunto de Mandelbrot en la región [xmin, xmax] x [ymin, ymax].
    - width, height: resolución en píxeles
    - max_iter: número máximo de iteraciones
    Retorna:
      - mandelbrot_img: array 2D con los valores de iteración en cada punto.
    """
    # Discretización en ejes
    x_vals = np.linspace(xmin, xmax, width)
    y_vals = np.linspace(ymin, ymax, height)
    
    mandelbrot_img = np.zeros((height, width))
    
    for i, y in enumerate(y_vals):
        for j, x in enumerate(x_vals):
            c = complex(x, y)
            z = 0 + 0j
            iteration = 0
            # Iteramos z_{n+1} = z_n^2 + c
            while (abs(z) <= 2.0) and (iteration < max_iter):
                z = z*z + c
                iteration += 1
            mandelbrot_img[i, j] = iteration
    return mandelbrot_img

# ------------------------------------------------------------
# 3) REPRESENTACIÓN 3D DE LAS ÓRBITAS DEL MAPA LOGÍSTICO
# ------------------------------------------------------------
def generar_datos_3D(r_min=2.4, r_max=4.0, steps=50, n_iter=100):
    """
    Genera datos (r, n, x_n) en 3D para visualizar cómo evolucionan
    las órbitas x_n en función de r y del número de iteración n.
    - steps: cuántos valores de r tomamos en [r_min, r_max].
    - n_iter: cuántas iteraciones calculamos para cada r.
    Retorna:
      - R, N, X: arrays 1D con las coordenadas para un scatter 3D.
    """
    r_values = np.linspace(r_min, r_max, steps)
    R, N, X = [], [], []
    
    for r in r_values:
        x = 0.5
        for n in range(n_iter):
            x = logistic_map(x, r)
            R.append(r)
            N.append(n)
            X.append(x)
    return np.array(R), np.array(N), np.array(X)

# ------------------------------------------------------------
# SCRIPT PRINCIPAL
# ------------------------------------------------------------
def main():
    # 1) Diagrama de bifurcaciones (2D)
    bif_r, bif_x = generar_bifurcacion(r_min=2.4, r_max=4.0,
                                       steps=800, discard=200, keep=100)
    
    # 2) Conjunto de Mandelbrot (2D)
    mandelbrot_img = mandelbrot_set(xmin=-2.0, xmax=1.0,
                                    ymin=-1.5, ymax=1.5,
                                    width=600, height=400,
                                    max_iter=200)
    
    # 3) Datos 3D para el mapa logístico
    R_3D, N_3D, X_3D = generar_datos_3D(r_min=2.4, r_max=4.0,
                                        steps=50, n_iter=100)
    
    # Creamos la figura con 3 subplots
    fig = plt.figure(figsize=(14, 4.5))
    
    # --- Subplot 1: Diagrama de Bifurcación ---
    ax1 = fig.add_subplot(1, 3, 1)
    ax1.scatter(bif_r, bif_x, s=0.1, color='black')
    ax1.set_title("Diagrama de Bifurcaciones (Mapa Logístico)")
    ax1.set_xlabel("r")
    ax1.set_ylabel("x")
    ax1.set_xlim(2.4, 4.0)
    ax1.set_ylim(0, 1)
    
    # --- Subplot 2: Conjunto de Mandelbrot ---
    ax2 = fig.add_subplot(1, 3, 2)
    ax2.set_title("Conjunto de Mandelbrot")
    ax2.set_xlabel("Re(c)")
    ax2.set_ylabel("Im(c)")
    # Mostramos la imagen de Mandelbrot
    # mandelbrot_img está indexada como [fila, columna] => [y, x]
    # pero el "y" va de arriba a abajo. Invertimos el eje Y con origin='lower'.
    ax2.imshow(mandelbrot_img[::-1,:], cmap='hot', extent=(-2, 1, -1.5, 1.5))
    # O si prefieres no voltear, usar: origin='lower' (pero ajusta si es necesario).
    # ax2.imshow(mandelbrot_img, cmap='hot', extent=(-2, 1, -1.5, 1.5), origin='lower')
    
    # --- Subplot 3: Representación 3D ---
    ax3 = fig.add_subplot(1, 3, 3, projection='3d')
    ax3.scatter(R_3D, N_3D, X_3D, s=1, c=X_3D, cmap='viridis', alpha=0.6)
    ax3.set_title("Mapa Logístico en 3D")
    ax3.set_xlabel("r")
    ax3.set_ylabel("Iteración n")
    ax3.set_zlabel("x_n")
    ax3.set_xlim(2.4, 4.0)
    ax3.set_ylim(0, 100)
    ax3.set_zlim(0, 1)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
