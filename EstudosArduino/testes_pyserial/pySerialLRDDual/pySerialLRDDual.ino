// Definições de pinos
const int pinoLDR_Nota = A0;   // Sensor que escolhe a nota
const int pinoLDR_Vol = A1;   // Sensor que seleciona o volume

void setup() {
  Serial.begin(9600); 
}

void loop() {
  int leituraNota = analogRead(pinoLDR_Nota);
  int leituraVol = analogRead(pinoLDR_Vol);

  Serial.print(leituraNota); Serial.print(","); Serial.println(leituraVol);

  delay(50); // Estabilidade
}