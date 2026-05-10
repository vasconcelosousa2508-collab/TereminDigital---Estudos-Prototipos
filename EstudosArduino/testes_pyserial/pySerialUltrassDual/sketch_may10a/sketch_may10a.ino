void setup() {
  Serial.begin(9600);

  // Sensor1
  pinMode(9, OUTPUT); // Trig na porta 9
  pinMode(10, INPUT); // Echo na porta 10

  //Sensor2
  pinMode(7, OUTPUT); // Trig na porta 9
  pinMode(6, INPUT); // Echo na porta 10
}

void loop() {
  // Sensor1
  digitalWrite(9, LOW);  delayMicroseconds(2);
  digitalWrite(9, HIGH); delayMicroseconds(10);
  digitalWrite(9, LOW);

  long tempo1 = pulseIn(10, HIGH);
  int distancia1 = tempo1 * 0.034 / 2;
  
  //Sensor2
  digitalWrite(7, LOW);  delayMicroseconds(2);
  digitalWrite(6, HIGH); delayMicroseconds(10);
  digitalWrite(7, LOW);

  long tempo2 = pulseIn(6, HIGH);
  int distancia2 = tempo2 * 0.034 / 2;

  Serial.print(distancia1);  Serial.print(","); Serial.println(distancia2); 
  delay(250);
}
