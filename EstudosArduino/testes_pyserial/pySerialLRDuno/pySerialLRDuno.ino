// Definições de pinos
const int pinoLDR = A0;

void setup() {
  Serial.begin(9600); 
}

void loop() {
  int leituraLuz = analogRead(pinoLDR);

  Serial.println(leituraLuz);

 //Lembrar* No Python:
  // Se leituraLuz < limiteSombra -> Toca som
  // Se leituraLuz >= limiteSombra -> Silêncio

  delay(50); 
}