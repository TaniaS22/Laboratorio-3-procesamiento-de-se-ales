# Laboratorio 3 Procesamiento de señales electromiográficas EMG
Autores: Fabián Alberto López Lemus y Tania Angélica Sandoval Ramírez
## Introducción
El propósito de este laboratorio es aplicar técnicas de filtrado de señales para procesar una señal electromiográfica y detectar la fatiga muscular mediante un análisis estadístico y espectral. Según la teoría, la frecuencia de la señal disminuye cuando el músculo alcanza la fatiga, lo cual será comprobado a través de un test- T de hipótesis.

Para la adquisición de la señal, se utilizó un sensor ...., junto con un ARDUINO para realizar la conversión analógica-digital (ADC) de la señal y transferir los datos al entorno de Python. El análisis de la señal se realizó utilizando Python, donde se importaron, visualizaron y procesaron los datos.

**Recomendaciones para terceros:** Se recomienda el software "Anaconda Navigator" con su herramienta "Spyder" para el análisis en Python. Al final de este repositorio, se incluyen las instrucciones detalladas para la correcta utilización del código.

## Procedimiento 
### Primera parte

En este laboratorio, se usaron unos electrodos superficiales que estaban en una configuración como se muestra en la imágen (capturando la señal del músculo flexor ulnar del carpo, también conocido como cubital anterior, es un músculo del antebrazo que se encarga de flexionar y aducir la mano) que estan conectados al sensor AD8232 y este tiene 3 PINES conectados al ARDUINO, uno para los 3.3V del sensor, otro GROUND del sensor y el último esta conectado al OUTPUT del sensor. 
![image](https://github.com/user-attachments/assets/668733eb-a0c3-4d71-8d04-8e21cb634be6)
![image](https://github.com/user-attachments/assets/850edf43-4900-4839-b8d2-a6d08a017236)

### Segunda parte
Para poder recoger los datos de la señal se realizó un programa para que captura una frecuencia de muestreo de 3000 Hz ya que las señales EMG se encuentran en el rango de 10 Hz a 1000 Hz, y como dice el teorema de muestreo de Nyquist  la frecuencia de muestreo debe ser mayor que el doble del de interés de frecuencia más alta en la señal medida.


### Tercera parte

También se realizó una interfaz en Qt designer, en donde ......

### Cuarta parte


