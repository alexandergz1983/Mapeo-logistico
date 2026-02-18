import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from mpl_toolkits.mplot3d import Axes3D

# 1) MAPA LOGÍSTICO: Diagrama de bifurcaciones
def logistic_map(x, r):
    return r * x * (1 - x)

def generar_bifurcacion(r_min=2.4, r_max=4.0, steps=600, discard=100, keep=50):
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

# 2) CONJUNTO DE MANDELBROT (2D)
def mandelbrot_set(xmin=-2.0, xmax=1.0, ymin=-1.5, ymax=1.5,
                   width=400, height=300, max_iter=100):
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

# 3) DATOS 3D DEL MAPA LOGÍSTICO
def generar_datos_3D(r_min=2.4, r_max=4.0, steps=40, n_iter=60):
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

def main():
    # Parámetros
    r_min, r_max = 2.4, 4.0
    max_iter = 200  # para Mandelbrot
    
    # 1) Diagrama de bifurcación
    bif_r, bif_x = generar_bifurcacion(r_min, r_max, steps=600, discard=100, keep=50)
    
    # 2) Mandelbrot (cálculo completo)
    mandelbrot_img = mandelbrot_set(xmin=-2.0, xmax=1.0,
                                    ymin=-1.5, ymax=1.5,
                                    width=400, height=300,
                                    max_iter=max_iter)
    mb_height, mb_width = mandelbrot_img.shape
    x_min, x_max = -2.0, 1.0
    y_min, y_max = -1.5, 1.5
    
    # 3) Datos 3D
    R_3D, N_3D, X_3D = generar_datos_3D(r_min, r_max, steps=40, n_iter=60)
    
    # FIGURA con 3 subplots
    fig = plt.figure(figsize=(14, 5))
    
    # Subplot 1: Diagrama de bifurcaciones
    ax1 = fig.add_subplot(1, 3, 1)
    ax1.set_title("Bifurcaciones (Mapa Logístico)")
    ax1.set_xlabel("r")
    ax1.set_ylabel("x")
    ax1.set_xlim(r_min, r_max)
    ax1.set_ylim(0, 1)
    scatter_bif = ax1.scatter([], [], s=0.1, color='black')
    
    # Subplot 2: Conjunto de Mandelbrot
    ax2 = fig.add_subplot(1, 3, 2)
    ax2.set_title("Conjunto de Mandelbrot")
    ax2.set_xlabel("Re(c)")
    ax2.set_ylabel("Im(c)")
    # Imagen vacía inicial, con clim y colormap
    image_mandel = ax2.imshow(
        np.zeros((1,1)),
        extent=(x_min, x_min, y_min, y_min),
        origin='lower',
        cmap='hot',
        vmin=0,
        vmax=max_iter  # fuerza el rango de colores
    )
    
    # Subplot 3: Vista 3D del mapa logístico
    ax3 = fig.add_subplot(1, 3, 3, projection='3d')
    ax3.set_title("Mapa Logístico en 3D")
    ax3.set_xlabel("r")
    ax3.set_ylabel("Iteración (n)")
    ax3.set_zlabel("x_n")
    ax3.set_xlim(r_min, r_max)
    ax3.set_ylim(0, 60)
    ax3.set_zlim(0, 1)
    scatter_3d = None
    
    plt.subplots_adjust(left=0.1, bottom=0.25, wspace=0.4)
    
    # Slider
    ax_slider = plt.axes([0.15, 0.1, 0.7, 0.03])
    slider = Slider(ax_slider, 'Progreso', 0.0, 1.0, valinit=0.0)
    
    def actualizar(val):
        nonlocal scatter_3d
        frac = slider.val
        
        # 1) Diagrama de bifurcación
        r_limite = r_min + frac * (r_max - r_min)
        mask_bif = (bif_r <= r_limite)
        coords_bif = np.column_stack((bif_r[mask_bif], bif_x[mask_bif]))
        scatter_bif.set_offsets(coords_bif)
        
        # 2) Mandelbrot: mostrar de izq. a der.
        col_actual = int(frac * mb_width)
        if col_actual < 1:
            col_actual = 1
        mb_slice = mandelbrot_img[:, :col_actual]
        # Actualiza la imagen
        image_mandel.set_data(mb_slice[::-1, :])  # si lo quieres invertido verticalmente
        x_actual = x_min + (col_actual / mb_width) * (x_max - x_min)
        image_mandel.set_extent((x_min, x_actual, y_min, y_max))
        
        # 3) Vista 3D
        if scatter_3d is not None:
            scatter_3d.remove()
        mask_3d = (R_3D <= r_limite)
        scatter_3d = ax3.scatter(
            R_3D[mask_3d], N_3D[mask_3d], X_3D[mask_3d],
            s=5, c=X_3D[mask_3d], cmap='viridis', alpha=0.7
        )
        
        fig.canvas.draw_idle()
    
    slider.on_changed(actualizar)
    
    plt.show()

if __name__ == "__main__":
    main()
