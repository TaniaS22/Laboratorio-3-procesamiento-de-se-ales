import serial
import time

# Configurar el puerto serie y la velocidad
com_port = 'COM4'  # Cambia esto si es necesario
baud_rate = 250000
duration = 60  # Duración en segundos para leer datos

# Crear un objeto de conexión serial
ser = serial.Serial(com_port, baud_rate)

# Esperar un momento para asegurarse de que la conexión esté lista
time.sleep(2)

# Abrir el archivo para escribir
with open('datos.txt', 'w') as file:
    start_time = time.time()
    
    while time.time() - start_time < duration:
        # Leer una línea del puerto serie
        if ser.in_waiting > 0:  # Verificar si hay datos disponibles
            line = ser.readline().decode('utf-8', errors='ignore').strip()  # Leer y decodificar
            print(line)  # Imprimir en la consola
            file.write(line + '\n')  # Escribir en el archivo

# Cerrar el puerto serie
ser.close()
print("Lectura completada y datos guardados en 'datos_ecg.txt'.")
