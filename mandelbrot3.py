import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from mpl_toolkits.mplot3d import Axes3D  # Para gráficos 3D (si se requiere en el futuro)
import time

# -------------------------------------------
# 1) Funciones para el mapa logístico y diagrama de bifurcación
# -------------------------------------------
def logistic_map(x, r):
    """Mapa logístico: x_{n+1} = r * x_n * (1 - x_n)."""
    return r * x * (1 - x)

def generar_bifurcacion(r_min=2.4, r_max=4.0, steps=600, discard=100, keep=50):
    """
    Genera puntos (r, x) para el diagrama de bifurcación.
      - r_min, r_max: rango de valores para r.
      - steps: cantidad de valores de r.
      - discard: iteraciones para descartar (transitorio).
      - keep: iteraciones a guardar.
    Retorna dos arrays: bif_r y bif_x.
    """
    r_values = np.linspace(r_min, r_max, steps)
    bif_r, bif_x = [], []
    for r in r_values:
        x = 0.5
        for _ in range(discard):
            x = logistic_map(x, r)
        for _ in range(keep):
            x = logistic_map(x, r)
            bif_r.append(r)
            bif_x.append(x)
    return np.array(bif_r), np.array(bif_x)

# -------------------------------------------
# 2) Funciones para calcular el conjunto de Mandelbrot
# -------------------------------------------
def mandelbrot_set(xmin=-2.0, xmax=1.0, ymin=-1.5, ymax=1.5,
                   width=400, height=300, max_iter=100):
    """
    Calcula el conjunto de Mandelbrot en la región [xmin,xmax]x[ymin,ymax].
    Retorna un array 2D (dimensión height x width) con la cantidad de iteraciones.
    """
    x_vals = np.linspace(xmin, xmax, width)
    y_vals = np.linspace(ymin, ymax, height)
    mandelbrot_img = np.zeros((height, width))
    
    for i, y in enumerate(y_vals):
        for j, x in enumerate(x_vals):
            c = complex(x, y)
            z = 0 + 0j
            iteration = 0
            while abs(z) <= 2.0 and iteration < max_iter:
                z = z*z + c
                iteration += 1
            mandelbrot_img[i, j] = iteration
    return mandelbrot_img

# -------------------------------------------
# 3) Función para calcular el conjunto de Julia
# -------------------------------------------
def julia_set(c, xmin=-1.5, xmax=1.5, ymin=-1.5, ymax=1.5,
              width=400, height=400, max_iter=100):
    """
    Calcula el conjunto de Julia para el parámetro c en la región dada.
    Retorna un array 2D (height x width) con la cantidad de iteraciones.
    """
    x_vals = np.linspace(xmin, xmax, width)
    y_vals = np.linspace(ymin, ymax, height)
    julia_img = np.zeros((height, width))
    
    for i, y in enumerate(y_vals):
        for j, x in enumerate(x_vals):
            z = complex(x, y)
            iteration = 0
            while abs(z) <= 2.0 and iteration < max_iter:
                z = z*z + c
                iteration += 1
            julia_img[i, j] = iteration
    return julia_img

# -------------------------------------------
# SCRIPT PRINCIPAL CON SLIDER
# -------------------------------------------
def main():
    # Parámetros para el mapa logístico y diagrama de bifurcación
    r_min, r_max = 2.4, 4.0
    bif_steps = 600
    discard = 100
    keep = 50
    bif_r, bif_x = generar_bifurcacion(r_min, r_max, steps=bif_steps, discard=discard, keep=keep)
    
    # Parámetros para Mandelbrot
    mb_xmin, mb_xmax = -2.0, 1.0
    mb_ymin, mb_ymax = -1.5, 1.5
    mb_width, mb_height = 400, 300
    mb_max_iter = 200
    mandelbrot_img = mandelbrot_set(mb_xmin, mb_xmax, mb_ymin, mb_ymax, mb_width, mb_height, mb_max_iter)
    
    # Para la imagen de Mandelbrot, usamos la versión completa (se "revela" con el slider)
    
    # Parámetros para el conjunto de Julia
    julia_width, julia_height = 400, 400
    julia_max_iter = 150
    # Usaremos una región centrada en 0,0 para Julia
    julia_xmin, julia_xmax = -1.5, 1.5
    julia_ymin, julia_ymax = -1.5, 1.5
    
    # Creamos la figura con 3 subplots
    fig = plt.figure(figsize=(14, 5))
    
    # Subplot 1: Diagrama de bifurcación (logístico)
    ax1 = fig.add_subplot(1, 3, 1)
    ax1.set_title("Diagrama de Bifurcación (Logístico)")
    ax1.set_xlabel("r")
    ax1.set_ylabel("x")
    ax1.set_xlim(r_min, r_max)
    ax1.set_ylim(0, 1)
    # Creamos un scatter vacío; se actualizará con set_offsets()
    scatter_bif = ax1.scatter([], [], s=0.5, color='black')
    
    # Subplot 2: Conjunto de Mandelbrot
    ax2 = fig.add_subplot(1, 3, 2)
    ax2.set_title("Conjunto de Mandelbrot")
    ax2.set_xlabel("Re(c)")
    ax2.set_ylabel("Im(c)")
    # Empezamos con una imagen "vacía" (se irá revelando)
    image_mandel = ax2.imshow(np.zeros((1,1)),
                              extent=(mb_xmin, mb_xmin, mb_ymin, mb_ymin),
                              origin='lower', cmap='hot',
                              vmin=0, vmax=mb_max_iter)
    
    # Subplot 3: Conjunto de Julia
    ax3 = fig.add_subplot(1, 3, 3)
    ax3.set_title("Conjunto de Julia")
    ax3.set_xlabel("Re(z)")
    ax3.set_ylabel("Im(z)")
    # Empezamos con una imagen vacía (se actualizará según c)
    image_julia = ax3.imshow(np.zeros((1,1)),
                             extent=(julia_xmin, julia_xmin, julia_ymin, julia_ymin),
                             origin='lower', cmap='inferno',
                             vmin=0, vmax=julia_max_iter)
    
    # Ajustamos el layout y creamos un slider en la parte inferior
    plt.subplots_adjust(left=0.1, bottom=0.25, wspace=0.4)
    ax_slider = plt.axes([0.15, 0.1, 0.7, 0.03])
    slider = Slider(ax_slider, 'Progreso', 0.0, 1.0, valinit=0.0)
    
    def actualizar(val):
        frac = slider.val  # valor entre 0 y 1
        
        # --- 1) Actualizamos el diagrama de bifurcación ---
        # Mostramos los puntos con r <= r_limite
        r_limite = r_min + frac * (r_max - r_min)
        mask = (bif_r <= r_limite)
        coords = np.column_stack((bif_r[mask], bif_x[mask]))
        scatter_bif.set_offsets(coords)
        
        # --- 2) Actualizamos la imagen de Mandelbrot ---
        # Usamos el slider para "revelar" columnas de la imagen de Mandelbrot
        col_actual = int(frac * mb_width)
        if col_actual < 1:
            col_actual = 1
        mb_slice = mandelbrot_img[:, :col_actual]
        # Actualizamos la imagen; invertimos verticalmente para usar origin='lower'
        image_mandel.set_data(mb_slice[::-1, :])
        # El extent se actualiza para mostrar desde mb_xmin hasta un x_actual
        x_actual = mb_xmin + (col_actual / mb_width) * (mb_xmax - mb_xmin)
        image_mandel.set_extent((mb_xmin, x_actual, mb_ymin, mb_ymax))
        
        # --- 3) Actualizamos el conjunto de Julia ---
        # Usamos el slider para variar el parámetro c. Por ejemplo, c recorre una circunferencia:
        # c = c0 + radio * exp(2*pi*i*frac)
        c0 = -0.8
        radio = 0.2
        angle = 2 * np.pi * frac
        c = c0 + radio * np.cos(angle) + 1j * radio * np.sin(angle)
        # Calculamos la imagen de Julia para c (puede tomar un poco de tiempo)
        # Para no congelar la interacción, podrías reducir la resolución
        julia_img = julia_set(c, julia_xmin, julia_xmax, julia_ymin, julia_ymax,
                              width=julia_width, height=julia_height, max_iter=julia_max_iter)
        image_julia.set_data(julia_img[::-1, :])
        image_julia.set_extent((julia_xmin, julia_xmax, julia_ymin, julia_ymax))
        ax3.set_title(f"Conjunto de Julia\n c = {c.real:.3f} + {c.imag:.3f}i")
        
        fig.canvas.draw_idle()
    
    slider.on_changed(actualizar)
    
    # Mostrar la figura interactiva
    plt.show()

if __name__ == "__main__":
    main()
