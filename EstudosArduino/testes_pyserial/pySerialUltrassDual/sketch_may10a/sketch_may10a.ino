// Definições de pinos 
const int TRIG1 = 9;
const int ECHO1 = 10;
const int TRIG2 = 7;
const int ECHO2 = 6;

const int LIMITE_MAX = 30;

void setup() {
  Serial.begin(9600);

  pinMode(TRIG1, OUTPUT);
  pinMode(ECHO1, INPUT);
  
  pinMode(TRIG2, OUTPUT);
  pinMode(ECHO2, INPUT);
}

void loop() {
  // Sensor 1
  digitalWrite(TRIG1, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG1, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG1, LOW);
  long tempo1 = pulseIn(ECHO1, HIGH);
  int d1 = tempo1 * 0.034 / 2;

  // Sensor 2
  digitalWrite(TRIG2, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG2, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG2, LOW);
  long tempo2 = pulseIn(ECHO2, HIGH);
  int d2 = tempo2 * 0.034 / 2;
  
  int enviaD1 = (d1 > 0 && d1 <= LIMITE_MAX) ? d1 : 999;
  int enviaD2 = (d2 > 0 && d2 <= LIMITE_MAX) ? d2 : 999;

  Serial.print(enviaD1);
  Serial.print(",");
  Serial.println(enviaD2);

  delay(50); 
}
