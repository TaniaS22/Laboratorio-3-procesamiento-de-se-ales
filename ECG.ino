// Definir el pin analógico donde se conecta el OUTPUT del AD8232
const int ECG_PIN = A0;

// Variables para almacenar los valores leídos
int valorECG = 0;

void setup() {
  // Iniciar la comunicación serial a 1000 baudios
  Serial.begin(250000);
  // Esperar a que se inicie la comunicación serial
  while (!Serial) {
    ; // Espera hasta que se conecte el puerto serial
  }
  // Opcional: Configurar el pin como entrada (aunque por defecto lo es)
  pinMode(ECG_PIN, INPUT);
}

void loop() {
  // Leer el valor analógico del AD8232
  valorECG = analogRead(ECG_PIN);

  // Imprimir el valor en el Monitor Serial
  Serial.println(valorECG);

  // Esperar un breve momento antes de la siguiente lectura
   delayMicroseconds(333); // 1 milisegundo para una tasa de muestreo de aproximadamente 1000 Hz
}
