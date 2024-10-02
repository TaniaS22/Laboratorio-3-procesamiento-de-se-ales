# Laboratorio 3 Procesamiento de señales electromiográficas EMG
Autores: Fabián Alberto López Lemus y Tania Angélica Sandoval Ramírez
## Introducción
El propósito de este laboratorio es aplicar técnicas de filtrado de señales para procesar una señal electromiográfica y detectar la fatiga muscular mediante un análisis estadístico y espectral. Según la teoría, la frecuencia de la señal disminuye cuando el músculo alcanza la fatiga, lo cual será comprobado a través de un test- T de hipótesis.

Para la adquisición de la señal, se utilizó un sensor ...., junto con un ARDUINO para realizar la conversión analógica-digital (ADC) de la señal y transferir los datos al entorno de Python. El análisis de la señal se realizó utilizando Python, donde se importaron, visualizaron y procesaron los datos.

**Recomendaciones para terceros:** Se recomienda el software "Anaconda Navigator" con su herramienta "Spyder" para el análisis en Python. Al final de este repositorio, se incluyen las instrucciones detalladas para la correcta utilización del código.

## Procedimiento 
### Primera parte

En este laboratorio, se usaron unos electrodos superficiales que estaban en una configuración como se muestra en la imágen (capturando la señal del músculo flexor ulnar del carpo, también conocido como cubital anterior, es un músculo del antebrazo que se encarga de flexionar y aducir la mano) que estan conectados al sensor AD8232 y este tiene 3 PINES conectados al ARDUINO, uno para los 3.3V del sensor, otro GROUND del sensor y el último esta conectado al OUTPUT del sensor. 

<img src="https://github.com/user-attachments/assets/668733eb-a0c3-4d71-8d04-8e21cb634be6" alt="Descripción de la imagen" width="300"/>
<img src="https://github.com/user-attachments/assets/850edf43-4900-4839-b8d2-a6d08a017236" alt="Descripción de la imagen" width="300"/>



### Segunda parte
Para poder recoger los datos de la señal se realizó un programa "ECG.ino" para que captura una frecuencia de muestreo de 3000 Hz ya que las señales EMG se encuentran en el rango de 10 Hz a 1000 Hz, y como dice el teorema de muestreo de Nyquist  la frecuencia de muestreo debe ser mayor que el doble del de interés de frecuencia más alta en la señal medida.

En ARDUINO, ese valor de 333 microsegundos representa el periodo (T) entre cada muestra para una frecuencia de muestreo de aproximadamente 3000 Hz
```c++
delayMicroseconds(333);
```

### Tercera parte
Despúes se realizó un programa de python "Toma_Datos.py" en donde se conecta a un puerto serie configurado a 250,000 baudios y durante 60 segundos lee continuamente los datos disponibles, imprimiéndolos y guardándolos en un archivo de texto. Luego, cierra el puerto serie una vez completada la operación. Se estableció el puerto de comunicación COM4  y una velocidad de transmisión de 250,000 baudios.
```python
com_port = 'COM4'
baud_rate = 250000
duration = 60  # Duración de la lectura (60 segundos)
```
Se abre un archivo llamado datos.txt para almacenar los datos recibidos.
```python
with open('datos.txt', 'w') as file:
```
Al finalizar la captura de datos, se cierra la conexión del puerto serie.
```python
ser.close()
print("Lectura completada y datos guardados en 'datos_ecg.txt'.")
```
### Cuarta parte
El código "Lab_3_ Señales.py" seimportan las librerías necesarias para el procesamiento de señales, análisis estadístico y graficación.
```python
from scipy.signal import butter, filtfilt
import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft
from scipy import stats
```
### Quinta parte
Se leen los datos desde un archivo de texto (datos.txt) que contiene la señal electromiográfica. Se establece una frecuencia de muestreo manualmente, en este caso 3000 Hz.
```python
emg_signal = np.loadtxt('datos.txt')
fs = 3000  # Frecuencia de muestreo (3000 Hz)
```
### Sexta parte
Se define un filtro pasa banda de Butterworth para filtrar la señal entre 10 Hz y 450 Hz. Y se crean dos funciones butter_bandpass para calcular los coeficientes del filtro y apply_filter para aplicar el filtro a la señal.

```python
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
```
Se definieron los valores del filtro pasabanda con:
-3 dB de atenuación en 10 Hz y 450 Hz.
-20 dB de atenuación en 5Hz y 1 KHz.
Y se realizó un programa en MATLAB "filtro_pasabanda.m" para comprobar el filtro, ya que se obtuvo que tendria un orden 4.En donde se definió la variable s y la función de transferencia.

<img src="https://github.com/user-attachments/assets/81163c11-7b51-4180-a3c8-7a74ea4e6a85" alt="Descripción de la imagen" width="400"/>

Y como se puede observar en la imágen los valores establecidos, si se cumplen.

Se genera un vector de tiempo para la señal y se grafican tanto la señal EMG original como la filtrada.
```python
t = np.arange(0, len(emg_signal)) / fs
```
<img src="https://github.com/user-attachments/assets/549429f8-3efb-4098-9f88-39c2515365d4" alt="Descripción de la imagen" width="400"/>

En la imágen de ariiba, podemos observar variaciones bruscas y picos en la amplitud, lo que indica la presencia de ruido, especialmente en las frecuencias altas.Y en la imágen de arriba se muestra la señal EMG filtrada, aplicandole el filtro pasa banda entre 10 Hz y 450 Hz. Esto mejora la señal, como se puede observar en la suavización de la gráfica, resaltando mejor los patrones de la señal EMG sin la interferencia de ruido.

### Séptima parte
Se realiza la Transformada Rápida de Fourier (FFT) sobre la señal filtrada para analizar su espectro de frecuencias.
```python
N = len(filtered_emg)
f = np.fft.fftfreq(N, 1/fs)
fft_values = np.abs(fft(filtered_emg))
```
<img src="https://github.com/user-attachments/assets/a09834ec-2210-41bd-a6cc-9d28bbc517c9" alt="Descripción de la imagen" width="400"/>

Como se puede ver en el gráfico, dado que se ha aplicado un filtro de banda entre 10 Hz y 450 Hz, lo que se observa son las componentes frecuenciales que quedan dentro de este rango. Y La magnitud de las diferentes frecuencias presentes en la señal. En este caso, se observa un pico pronunciado en las frecuencias más bajas, lo cual es común en señales EMG, donde las frecuencias más altas suelen tener menor potencia.

### Octava parte

Se divide la señal en ventanas (en este caso de 1000 muestras) para calcular los espectros de frecuencia y la media de cada ventana.

```python
window_size = 1000
num_windows = len(filtered_emg) // window_size + (len(filtered_emg) % window_size > 0)
# Calcular la FFT para cada ventana
```
<img src="https://github.com/user-attachments/assets/6c66975e-0a54-481b-b0e7-432aa66da262" alt="Descripción de la imagen" width="400"/>

En el gráfico, cada línea de color representa el espectro de frecuencias de una ventana específica de la señal EMG, desde la ventana 1 hasta la ventana 21. La mayoría de las ventanas muestran una concentración de energía en frecuencias bajas (entre 10 y 200 Hz). En el caso de la fatiga muscular, se suele observar que la frecuencia de la señal tiende a desplazarse hacia frecuencias más bajas. Esto se debe a que los músculos fatigados generan menos actividad eléctrica (como se muestra en la ventana 21).

### Novena parte
La señal se divide en ventanas de tamaño window_size (1000 muestras). Esto permite analizar segmentos específicos de la señal.

```python
# Matriz para almacenar los espectros de frecuencia y medias
frequency_spectra = np.zeros((num_windows, window_size // 2))
means = np.zeros(num_windows)
```
### Décima parte
Para cada ventana, se aplica una ventana de Hanning para suavizar los bordes y se calcula la FFT y la media de la señal en esa ventana. Se uso Hanning con el propósito de suavizar los bordes de la señal, reduciendo así las discontinuidades que pueden causar problemas al realizar análisis de frecuencia reduciendo la fuga espectral. La forma de la ventana de Hanning es similar a una campana. Al multiplicar la señal por esta ventana, los bordes de la señal se atenúan suavemente, reduciendo así las discontinuidades.

```python
# Test t para comparar la última ventana con el resto de la señal
t_stat, p_value = stats.ttest_ind(filtered_emg[-window_size:], filtered_emg[:-window_size]) if len(filtered_emg) > window_size else (np.nan, np.nan)
```
Se compara la última ventana con el resto de la señal mediante una prueba t (t-test) para detectar diferencias significativas.
...........
print(f"Última media: {last_mean}")
print(f"Media general: {overall_mean}")
print(f"Estadística t: {t_stat}")
print(f"Valor p: {p_value}")

Se comparan las medias de las ventanas con la media general de la señal, verificando si hay fatiga en cada ventana.
```python
error_margin = 0.5 * overall_mean
for i, mean in enumerate(means):
    if overall_mean - error_margin <= abs(mean) <= overall_mean + error_margin:
        print(f"Hubo fatiga en la ventana {i + 1}.")
    else:
        print(f"No hubo fatiga en la ventana {i + 1}.")
```
Y visualizamos la señal:

<img src="https://github.com/user-attachments/assets/c1b9096e-4468-4d8f-9f24-a8191d9dedbe" alt="Descripción de la imagen" width="400"/>


La línea azul representa la señal EMG después de haber sido filtrada y en la zona de rojo se ha aplicado un análisis en "ventanas" a la señal EMG, lo que implica dividir la señal en bloques para analizarlos individualmente para realizar el test t que compara las características de esta parte de la señal con el resto. Representa la media del segmento correspondiente a la última ventana en la señal. Esta media es calculada y luego usada para compararla estadísticamente con la media del resto de la señal.Y la línea amarilla es la media general de toda la señal filtrada, excluyendo la última ventana. Esta media sirve como referencia para identificar diferencias con la última ventana.

# Instrucciones para el usuario 

Se deberá cambiar la línea para cargar su archivo en el programa de "Lab_3_Señales.py".
```python
emg_signal = np.loadtxt('nombre_de_la_señal.txt')
```
 La persona debe cambiar este valor según la frecuencia de muestreo de su propia señal. 
 ```python
fs = "frecuencia que se requiere"
```
Si la persona quiere analizar otro rango de frecuencias, teniendo en cuenta que si se cambia las condiciones del filtro pueden variar.
 ```python
lowcut = "frecuencia que se requiere"
highcut = "frecuencia que se requiere"
```
Dependiendo de la longitud de la señal o del nivel de detalle requerido, el tamaño de la ventana puede ajustarse. Si la señal tiene muchas más muestras o si se quiere hacer un análisis más detallado, se podría aumentar el tamaño de la ventana:
 ```python
window_size = "muestras que desee"
```
Para cambiar el margen de error o comparar ventanas específicas
 ```python
error_margin = "margen_de_error" * overall_mean
```

Por favor, cite este artículo:
<br>
Lopez L., Sandoval R. (2024). Github 'Laboratorio 3 Procesamiento de señales'[Online].
### Informacion de contacto
est.fabiana.lopez@unimilitar.edu.co
<br>
est.tania.sandoval@unimilitar.edu.co
