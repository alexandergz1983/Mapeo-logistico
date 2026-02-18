import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# PARTE 1

# Parámetros iniciales
x0 = 2                # Número inicial de conejos
r_inicial = 0.5       # Tasa de crecimiento inicial
t = np.linspace(0, 10, 400)  # Vector de tiempo (10 años)

# Función de crecimiento exponencial
def crecimiento(t, r):
    return x0 * np.exp(r * t)

# Configuración de la figura y el eje
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.3)
linea, = ax.plot(t, crecimiento(t, r_inicial), lw=2)
ax.set_title('Crecimiento Exponencial de Conejos')
ax.set_xlabel('Tiempo (años)')
ax.set_ylabel('Número de conejos')
ax.grid(True)

# Creación del slider para la tasa de crecimiento 'r'
ax_slider = plt.axes([0.25, 0.1, 0.65, 0.03])
slider_r = Slider(ax_slider, 'Tasa de crecimiento (r)', 0.0, 2.0, valinit=r_inicial)

# Función de actualización al mover el slider
def actualizar(val):
    r = slider_r.val
    linea.set_ydata(crecimiento(t, r))
    fig.canvas.draw_idle()

slider_r.on_changed(actualizar)

plt.show()

############################################################################################################

# PARTE 2

# Función que representa el mapa logístico
def logistic_map(x, r):
    return r * x * (1 - x)

# Función para generar los datos de la evolución
def generar_datos(r, x0, num_iter):
    datos = [x0]
    for _ in range(num_iter):
        datos.append(logistic_map(datos[-1], r))
    return datos

# Parámetros iniciales
r_inicial = 2.0      # Tasa de crecimiento inicial
x0_inicial = 0.1     # Población inicial (como porcentaje del máximo)
num_iter = 100        # Número de iteraciones

# Genera los datos iniciales
datos = generar_datos(r_inicial, x0_inicial, num_iter)

# Configuración de la figura y el gráfico
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.1, bottom=0.3)
linea, = ax.plot(datos, marker='o', linestyle='-', color='b')
ax.set_ylim(0, 1)
ax.set_xlabel("Iteración")
ax.set_ylabel("Población (X)")
ax.set_title("Evolución de la población de conejos (Mapa Logístico)")

# Configuración de los sliders
ax_r = plt.axes([0.15, 0.15, 0.75, 0.03])
slider_r = Slider(ax_r, 'r', 0.1, 4.0, valinit=r_inicial)

ax_x0 = plt.axes([0.15, 0.1, 0.75, 0.03])
slider_x0 = Slider(ax_x0, 'x0_poblacion_inicial', 0.01, 1.0, valinit=x0_inicial)

# Función de actualización cuando se mueven los sliders
def actualizar(val):
    r = slider_r.val
    x0_poblacion_inicial = slider_x0.val
    nuevos_datos = generar_datos(r, x0_poblacion_inicial, num_iter)
    linea.set_ydata(nuevos_datos)
    fig.canvas.draw_idle()

# Conecta los sliders a la función de actualización
slider_r.on_changed(actualizar)
slider_x0.on_changed(actualizar)

plt.show()
