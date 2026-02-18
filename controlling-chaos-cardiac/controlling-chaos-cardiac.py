import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

# =============================================================================
# 1. Modelo del intervalo entre latidos (mapa logístico)
# =============================================================================
def logistic_map(r, x):
    """Mapa logístico: x_{n+1} = r * x_n * (1 - x_n)"""
    return r * x * (1 - x)

def generate_intervals(r, n_intervals=150, x0=0.5,
                       scale_min=0.20, scale_max=0.40):
    """
    Genera una secuencia de intervalos usando el mapa logístico.
    Los valores se escalan al rango [scale_min, scale_max] (segundos).
    """
    x = x0
    intervals = []
    for _ in range(n_intervals):
        x = logistic_map(r, x)
        intervals.append(x)
    intervals = np.array(intervals)
    # Escalar al rango fisiológico típico (~200-400 ms)
    intervals = scale_min + (scale_max - scale_min) * intervals
    return intervals

# =============================================================================
# 2. Generación de la señal de voltaje (potencial de acción monofásico)
# =============================================================================
def ap_waveform(t, t_peak=0.01, tau_decay=0.05):
    """
    Plantilla de un potencial de acción individual.
    Subida parabólica hasta t_peak, luego decaimiento exponencial.
    """
    if t < 0:
        return 0.0
    elif t < t_peak:
        return (t / t_peak) ** 2
    else:
        return np.exp(-(t - t_peak) / tau_decay)

ap_vec = np.vectorize(ap_waveform)

def generate_voltage(beat_times, total_time=5.0, fs=1000, noise=0.02):
    """
    Construye la señal de voltaje sumando la plantilla en cada tiempo de latido.
    """
    t = np.linspace(0, total_time, int(total_time * fs))
    v = np.zeros_like(t)
    for bt in beat_times:
        if bt <= total_time:
            rel_t = t - bt
            mask = rel_t >= 0
            v[mask] += ap_vec(rel_t[mask])
    v += noise * np.random.randn(len(v))
    v = np.clip(v, 0, 1.2)          # evitar valores negativos irreales
    return t, v

# =============================================================================
# 3. Configuración de la figura interactiva
# =============================================================================
# Parámetros fijos
TOTAL_TIME = 5.0          # segundos
N_INTERVALS = 200         # número de intervalos a generar
TRANSIENT = 50            # intervalos iniciales a descartar para el mapa

# Crear la figura y los ejes
fig, (ax_voltage, ax_poincare) = plt.subplots(1, 2, figsize=(12, 5))
plt.subplots_adjust(bottom=0.25)   # espacio para los widgets

# Elementos que se actualizarán
line_voltage, = ax_voltage.plot([], [], 'k-', lw=0.8)
scat_poincare = ax_poincare.scatter([], [], s=10, c='k', alpha=0.7)
diag_line, = ax_poincare.plot([], [], 'r--', lw=1, alpha=0.7, label='I_n = I_{n-1}')

# Configuración de los ejes
ax_voltage.set_xlim(0, TOTAL_TIME)
ax_voltage.set_ylim(-0.2, 1.5)
ax_voltage.set_xlabel('Tiempo (s)')
ax_voltage.set_ylabel('Voltaje (u.a.)')
ax_voltage.set_title('Potenciales de acción monofásicos')
ax_voltage.grid(True, alpha=0.3)

ax_poincare.set_xlim(0.15, 0.45)
ax_poincare.set_ylim(0.15, 0.45)
ax_poincare.set_xlabel('I_n (s)')
ax_poincare.set_ylabel('I_{n+1} (s)')
ax_poincare.set_title('Mapa de Poincaré (I_n vs I_{n-1})')
ax_poincare.legend()
ax_poincare.grid(True, alpha=0.3)

# =============================================================================
# 4. Función de actualización
# =============================================================================
def update_plot(r):
    """Genera nuevos datos con el parámetro r y actualiza la figura."""
    intervals = generate_intervals(r, n_intervals=N_INTERVALS)
    beat_times = np.cumsum(intervals)
    beat_times_in_window = beat_times[beat_times <= TOTAL_TIME]

    # Voltaje
    t, v = generate_voltage(beat_times_in_window, total_time=TOTAL_TIME)
    line_voltage.set_data(t, v)

    # Mapa de Poincaré (descartando transitorios)
    intervals_steady = intervals[TRANSIENT:]
    I_n = intervals_steady[1:]
    I_n_minus_1 = intervals_steady[:-1]
    scat_poincare.set_offsets(np.c_[I_n_minus_1, I_n])

    # Línea diagonal
    diag = np.linspace(0.15, 0.45, 10)
    diag_line.set_data(diag, diag)

    # Título con el valor de r
    ax_voltage.set_title(f'Potenciales de acción (r = {r:.2f})')
    ax_poincare.set_title(f'Mapa de Poincaré (r = {r:.2f})')

    fig.canvas.draw_idle()

# =============================================================================
# 5. Creación de los widgets
# =============================================================================
# Eje del slider
ax_slider = plt.axes([0.20, 0.10, 0.60, 0.03])
r_slider = Slider(
    ax=ax_slider,
    label='r (parámetro de bifurcación)',
    valmin=2.5,
    valmax=4.0,
    valinit=3.2,
    valstep=0.01
)

# Botones para valores típicos
ax_btn_p1 = plt.axes([0.15, 0.02, 0.12, 0.05])
btn_p1 = Button(ax_btn_p1, 'Periodo‑1 (2.8)')
ax_btn_p2 = plt.axes([0.30, 0.02, 0.12, 0.05])
btn_p2 = Button(ax_btn_p2, 'Bigeminia (3.2)')
ax_btn_p4 = plt.axes([0.45, 0.02, 0.12, 0.05])
btn_p4 = Button(ax_btn_p4, 'Periodo‑4 (3.5)')
ax_btn_chaos = plt.axes([0.60, 0.02, 0.12, 0.05])
btn_chaos = Button(ax_btn_chaos, 'Caos (3.8)')

# Conexión de los callbacks
r_slider.on_changed(update_plot)

btn_p1.on_clicked(lambda event: r_slider.set_val(2.8))
btn_p2.on_clicked(lambda event: r_slider.set_val(3.2))
btn_p4.on_clicked(lambda event: r_slider.set_val(3.5))
btn_chaos.on_clicked(lambda event: r_slider.set_val(3.8))

# =============================================================================
# 6. Mostrar la figura y la primera actualización
# =============================================================================
update_plot(r_slider.val)
plt.show()