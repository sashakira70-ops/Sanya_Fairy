import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons
from scipy.signal import iirfilter, filtfilt

# --- Початкові параметри ---
INIT_AMP = 1.0
INIT_FREQ = 1.0
INIT_PHASE = 0.0
INIT_NOISE_MEAN = 0.0
INIT_NOISE_COV = 0.1
INIT_CUTOFF = 0.1

t = np.linspace(0, 10, 1000)

# Базовий шум генерується один раз і залишається незмінним
np.random.seed(42)
base_noise = np.random.randn(len(t))

def harmonic_with_noise(amplitude, frequency, phase, noise_mean, noise_covariance, show_noise):
    harmonic = amplitude * np.sin(2 * np.pi * frequency * t + phase)
    if show_noise:
        # Стандартне відхилення дорівнює кореню з дисперсії
        noise = noise_mean + np.sqrt(noise_covariance) * base_noise
        return harmonic + noise, harmonic
    return harmonic, harmonic

def apply_filter(data, cutoff):
    # Обмеження частоти зрізу для стабільності роботи фільтра
    if cutoff <= 0.001:
        cutoff = 0.001
    elif cutoff >= 0.999:
        cutoff = 0.999
    b, a = iirfilter(4, cutoff, btype='lowpass', ftype='butter')
    return filtfilt(b, a, data)

# Налаштування головного вікна
fig, (ax_main, ax_filtered) = plt.subplots(2, 1, figsize=(10, 9))
plt.subplots_adjust(left=0.1, bottom=0.45, hspace=0.3)

noisy_signal, pure_harmonic = harmonic_with_noise(INIT_AMP, INIT_FREQ, INIT_PHASE, INIT_NOISE_MEAN, INIT_NOISE_COV, True)
filtered_signal = apply_filter(noisy_signal, INIT_CUTOFF)

# Графік 1: Початковий сигнал
line_pure, = ax_main.plot(t, pure_harmonic, 'g--', label='Чиста гармоніка', alpha=0.8)
line_noisy, = ax_main.plot(t, noisy_signal, 'b-', label='Зашумлений сигнал', alpha=0.5)
ax_main.set_title("Початковий сигнал (Гармоніка + Шум)")
ax_main.legend(loc='upper right')
ax_main.grid(True)

# Графік 2: Відфільтрований сигнал
line_filtered_pure, = ax_filtered.plot(t, pure_harmonic, 'g--', label='Чиста гармоніка', alpha=0.8)
line_filtered, = ax_filtered.plot(t, filtered_signal, 'r-', label='Відфільтрований сигнал')
ax_filtered.set_title("Відфільтрований сигнал")
ax_filtered.legend(loc='upper right')
ax_filtered.grid(True)

# Осі для інтерактивних елементів
axcolor = 'lightgoldenrodyellow'
ax_amp    = plt.axes([0.15, 0.35, 0.65, 0.03], facecolor=axcolor)
ax_freq   = plt.axes([0.15, 0.30, 0.65, 0.03], facecolor=axcolor)
ax_phase  = plt.axes([0.15, 0.25, 0.65, 0.03], facecolor=axcolor)
ax_nmean  = plt.axes([0.15, 0.20, 0.65, 0.03], facecolor=axcolor)
ax_ncov   = plt.axes([0.15, 0.15, 0.65, 0.03], facecolor=axcolor)
ax_cutoff = plt.axes([0.15, 0.10, 0.65, 0.03], facecolor=axcolor)

# Слайдери
s_amp    = Slider(ax_amp, 'Амплітуда', 0.1, 5.0, valinit=INIT_AMP)
s_freq   = Slider(ax_freq, 'Частота', 0.1, 5.0, valinit=INIT_FREQ)
s_phase  = Slider(ax_phase, 'Фаза', 0.0, 2 * np.pi, valinit=INIT_PHASE)
s_nmean  = Slider(ax_nmean, 'Шум Mean', -2.0, 2.0, valinit=INIT_NOISE_MEAN)
s_ncov   = Slider(ax_ncov, 'Шум Cov', 0.0, 2.0, valinit=INIT_NOISE_COV)
s_cutoff = Slider(ax_cutoff, 'Фільтр Cutoff', 0.001, 0.999, valinit=INIT_CUTOFF)

# Чекбокс
ax_check = plt.axes([0.85, 0.25, 0.12, 0.1], facecolor=axcolor)
check = CheckButtons(ax_check, ['Шум'], [True])

def update(val):
    amp = s_amp.val
    freq = s_freq.val
    phase = s_phase.val
    nmean = s_nmean.val
    ncov = s_ncov.val
    cutoff = s_cutoff.val
    show_noise = check.get_status()[0]
    
    y_noisy, y_pure = harmonic_with_noise(amp, freq, phase, nmean, ncov, show_noise)
    y_filtered = apply_filter(y_noisy, cutoff)
    
    line_pure.set_ydata(y_pure)
    line_filtered_pure.set_ydata(y_pure)
    line_filtered.set_ydata(y_filtered)
    
    if show_noise:
        line_noisy.set_ydata(y_noisy)
        line_noisy.set_visible(True)
    else:
        line_noisy.set_visible(False)
        
    ax_main.relim()
    ax_main.autoscale_view()
    ax_filtered.relim()
    ax_filtered.autoscale_view()
    fig.canvas.draw_idle()

s_amp.on_changed(update)
s_freq.on_changed(update)
s_phase.on_changed(update)
s_nmean.on_changed(update)
s_ncov.on_changed(update)
s_cutoff.on_changed(update)
check.on_clicked(update)

# Кнопка Reset
ax_reset = plt.axes([0.85, 0.1, 0.1, 0.05])
btn_reset = Button(ax_reset, 'Reset', color=axcolor, hovercolor='0.975')

def reset(event):
    s_amp.reset()
    s_freq.reset()
    s_phase.reset()
    s_nmean.reset()
    s_ncov.reset()
    s_cutoff.reset()
    if not check.get_status()[0]:
        check.set_active(0)

btn_reset.on_clicked(reset)

plt.show()