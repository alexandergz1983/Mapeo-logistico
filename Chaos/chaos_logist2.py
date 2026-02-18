import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# --------------------------------------------
# 1) Definimos el mapa logístico
#    X_{n+1} = r * X_n * (1 - X_n)
# --------------------------------------------
def logistic_map(x, r):
    return r * x * (1 - x)

# --------------------------------------------
# 2) Generamos los datos de evolución temporal
#    (para la gráfica de la izquierda)
# --------------------------------------------
def generar_datos_iteracion(r, x0, num_iter):
    datos = [x0]
    for _ in range(num_iter):
        datos.append(logistic_map(datos[-1], r))
    return datos

# --------------------------------------------
# 3) Generamos los datos para el diagrama de bifurcación
#    (se hace una sola vez y luego se "filtra" con un slider)
# --------------------------------------------
def generar_bifurcacion(r_min=2.4, r_max=4.0, steps=800, discard=200, keep=50):
    """
    r_min, r_max: rango de valores de r
    steps: cuántos valores de r muestreamos en [r_min, r_max]
    discard: cuántas iteraciones descartamos (transitorio)
    keep: cuántas iteraciones guardamos para graficar
    """
    r_values = np.linspace(r_min, r_max, steps)
    r_list = []
    x_list = []
    
    for r in r_values:
        x = 0.5  # Valor inicial
        # Descartamos el transitorio
        for _ in range(discard):
            x = logistic_map(x, r)
        # Guardamos las iteraciones "estables"
        for _ in range(keep):
            x = logistic_map(x, r)
            r_list.append(r)
            x_list.append(x)
    
    return np.array(r_list), np.array(x_list)

# --------------------------------------------
# Parámetros iniciales para la simulación
# --------------------------------------------
r_inicial = 2.0       # Tasa de crecimiento inicial para la gráfica de la izquierda
x0_inicial = 0.1      # Población inicial (entre 0 y 1)
num_iter = 50         # Número de iteraciones a mostrar

# Generamos datos de la iteración inicial (gráfica izq.)
datos_iter = generar_datos_iteracion(r_inicial, x0_inicial, num_iter)

# Generamos los datos para el diagrama de bifurcación (gráfica der.)
# (solo una vez; luego usaremos un slider para "recortar" en r)
r_min, r_max = 2.4, 4.0
bif_r, bif_x = generar_bifurcacion(r_min, r_max, steps=800, discard=200, keep=50)

# --------------------------------------------
# 4) Preparamos la figura con dos subplots
# --------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
plt.subplots_adjust(left=0.1, bottom=0.25, wspace=0.3)

# -- Gráfica 1 (izquierda): Evolución temporal --
linea_iter, = ax1.plot(datos_iter, marker='o', linestyle='-', color='b')
ax1.set_ylim(0, 1)
ax1.set_xlabel("Iteración")
ax1.set_ylabel("Población (X)")
ax1.set_title("Evolución de la población (mapa logístico)")

# -- Gráfica 2 (derecha): Diagrama de bifurcación --
# Inicialmente, mostramos todo el rango de r
scatter_bif = ax2.scatter(bif_r, bif_x, s=1, color='black', alpha=0.3)
ax2.set_xlabel("r")
ax2.set_ylabel("X")
ax2.set_title("Diagrama de Bifurcación")
ax2.set_xlim(r_min, r_max)
ax2.set_ylim(0, 1)

# --------------------------------------------
# 5) Creamos sliders para r, x0 y r_max_bif
# --------------------------------------------
# Ejes para sliders (posiciones en la figura)
slider_ax_r = plt.axes([0.15, 0.15, 0.7, 0.03])
slider_ax_x0 = plt.axes([0.15, 0.10, 0.7, 0.03])
slider_ax_rmax = plt.axes([0.15, 0.05, 0.7, 0.03])

slider_r = Slider(slider_ax_r, 'r (iter)', 0.1, 4.0, valinit=r_inicial)
slider_x0 = Slider(slider_ax_x0, 'x0', 0.01, 1.0, valinit=x0_inicial)
slider_rmax = Slider(slider_ax_rmax, 'r max (bif)', r_min, r_max, valinit=r_max)

# --------------------------------------------
# 6) Función de actualización al mover sliders
# --------------------------------------------
def actualizar(val):
    # 6.1) Actualizar la gráfica de iteración (izq.)
    r_val = slider_r.val
    x0_val = slider_x0.val
    nuevos_datos_iter = generar_datos_iteracion(r_val, x0_val, num_iter)
    linea_iter.set_ydata(nuevos_datos_iter)
    ax1.set_xlim(0, num_iter)
    ax1.set_ylim(0, 1)
    
    # 6.2) Actualizar el diagrama de bifurcación (der.) con r_max
    r_max_val = slider_rmax.val
    # Creamos una máscara para filtrar sólo los puntos con r <= r_max_val
    mask = (bif_r <= r_max_val)
    # Actualizamos los offsets (x,y) del scatter
    coords = np.column_stack((bif_r[mask], bif_x[mask]))
    scatter_bif.set_offsets(coords)
    
    # Ajuste de ejes si deseas que se "contraiga" dinámicamente:
    ax2.set_xlim(r_min, r_max_val)
    ax2.set_ylim(0, 1)
    
    fig.canvas.draw_idle()

# Vinculamos los sliders con la función de actualización
slider_r.on_changed(actualizar)
slider_x0.on_changed(actualizar)
slider_rmax.on_changed(actualizar)

plt.show()
