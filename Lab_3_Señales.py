from scipy.signal import butter, filtfilt
import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft
from scipy import stats

# Leer los datos desde el archivo de texto
emg_signal = np.loadtxt('datos.txt')

# Especificar la frecuencia de muestreo manualmente
fs = 3000  # Por ejemplo, 3000 Hz

# Filtro Butterworth
def butter_bandpass(lowcut, highcut, fs, order=4):
    nyquist = 0.5 * fs  # Frecuencia de Nyquist
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return b, a

def apply_filter(data, lowcut, highcut, fs):
    b, a = butter_bandpass(lowcut, highcut, fs, order=4)
    y = filtfilt(b, a, data)
    return y

# Filtro de 10 Hz - 450 Hz
lowcut = 10.0
highcut = 450.0
filtered_emg = apply_filter(emg_signal, lowcut, highcut, fs)

# Crear vector de tiempo para graficar
t = np.arange(0, len(emg_signal)) / fs

# Graficar la señal original y filtrada
plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.plot(t, emg_signal, label='Señal EMG sin filtrar')
plt.title('Señal EMG Original')
plt.xlabel('Tiempo [s]')
plt.ylabel('Amplitud')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(t, filtered_emg, label='Señal EMG Filtrada (10-450 Hz)', color='orange')
plt.title('Señal EMG Filtrada')
plt.xlabel('Tiempo [s]')
plt.ylabel('Amplitud')
plt.legend()

plt.tight_layout()
plt.show()

# FFT para analizar el espectro de frecuencias
N = len(filtered_emg)
fft_values = np.abs(fft(filtered_emg))
f = np.fft.fftfreq(N, 1/fs)

# Tomar solo la mitad positiva del espectro
fft_values = fft_values[:N//2]
f = f[:N//2]

# Encontrar la frecuencia dominante
dominant_freq = f[np.argmax(fft_values)]
print(f"Frecuencia dominante: {dominant_freq:.2f} Hz")

# Calcular la desviación estándar del espectro
std_fft = np.std(fft_values)
print(f"Desviación estándar del espectro: {std_fft:.2f}")

# Graficar el espectro de frecuencias
plt.figure(figsize=(8, 4))
plt.plot(f, fft_values)
plt.title('Espectro de Frecuencias de la Señal Filtrada')
plt.xlabel('Frecuencia [Hz]')
plt.ylabel('Amplitud')
plt.axvline(x=dominant_freq, color='r', linestyle='--', label=f'Frecuencia Dominante: {dominant_freq:.2f} Hz')
plt.legend()
plt.show()

# Tamaño de la ventana (ajústalo si es necesario)
window_size = 1000  # Ajusta esto según la longitud de tu señal
num_windows = len(filtered_emg) // window_size + (len(filtered_emg) % window_size > 0)

# Matriz para almacenar los espectros de frecuencia y medias
frequency_spectra = np.zeros((num_windows, window_size // 2))
means = np.zeros(num_windows)
std_devs = np.zeros(num_windows)  # Para almacenar la desviación estándar por ventana

# Se recorre la señal en ventanas
for i in range(num_windows):
    start_index = i * window_size
    end_index = start_index + window_size
    window = filtered_emg[start_index:end_index]

    # Si la ventana está incompleta, aplica una ventana de Hanning y recorta
    if len(window) < window_size:
        window *= np.hanning(len(window))
    else:
        window *= np.hanning(window_size)

    # Calcula la FFT
    fft_window = fft(window)
    magnitude = np.abs(fft_window)
    magnitude = 2 / window_size * magnitude
    frequency_spectra[i] = magnitude[: window_size // 2]

    # Calcular la media de la ventana
    means[i] = np.mean(window)

    # Calcular la desviación estándar del espectro de la ventana
    std_devs[i] = np.std(magnitude[: window_size // 2])

# Calcula las frecuencias correspondientes
frequencies = np.fft.fftfreq(window_size, 1/fs)[:window_size // 2]

# Graficar los espectros de frecuencia de algunas ventanas
plt.figure(figsize=(10, 6))
for i in range(num_windows):
    plt.plot(frequencies, frequency_spectra[i], label=f'Ventana {i+1}')
plt.title('Espectros de Frecuencia de las Ventanas')
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Magnitud')
plt.legend()
plt.xlim(0, fs/2)
plt.show()

# Calcular la desviación estándar general del análisis espectral
overall_std_fft = np.std(frequency_spectra)
print(f"Desviación estándar general del análisis espectral: {overall_std_fft:.2f}")

# Última media
last_mean = np.mean(filtered_emg[-window_size:])

# Media general, excluyendo la última ventana
overall_mean = np.mean(filtered_emg[:-window_size]) if len(filtered_emg) > window_size else np.mean(filtered_emg)

# Test t para comparar la última ventana con el resto de la señal
if len(filtered_emg) > window_size:
    t_stat, p_value = stats.ttest_ind(filtered_emg[-window_size:], filtered_emg[:-window_size])
else:
    t_stat, p_value = (np.nan, np.nan)

# Imprimir los resultados
print(f"Última media: {last_mean}")
print(f"Media general: {overall_mean}")
print(f"Estadística t: {t_stat}")
print(f"Valor p: {p_value}")

# Comparar medias de ventanas con la media general
error_margin = 0.5 * overall_mean  

for i, mean in enumerate(means):
    abs_mean = abs(mean)  # Valor absoluto de la media de la ventana
    if overall_mean - error_margin <= abs_mean <= overall_mean + error_margin:
        print(f"Hubo fatiga en la ventana {i + 1}.")
    else:
        print(f"No hubo fatiga en la ventana {i + 1}.")

# Graficar la señal filtrada con la ventana resaltada
plt.figure(figsize=(10, 6))
plt.plot(filtered_emg, label='Señal EMG Filtrada')
plt.plot(range(len(filtered_emg)-window_size, len(filtered_emg)), filtered_emg[-window_size:], label='Ventana', color='red')
plt.axhline(y=last_mean, color='green', linestyle='--', label='Última media')
plt.axhline(y=overall_mean, color='orange', linestyle='--', label='Media general')
plt.title('Señal EMG con Ventana para Test t')
plt.xlabel('Muestras')
plt.ylabel('Amplitud')
plt.legend()
plt.show()
