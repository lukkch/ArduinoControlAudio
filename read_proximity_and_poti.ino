// Ultrasound sensor
const int triggerPin = 7;
const int echoPin = 6;
// Potentiometer
const int potPin = A0;

long duration = 0;
long distance = 0;
int potiValue;

void setup()
{
  Serial.begin (9600);
  pinMode(triggerPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(potPin, INPUT);
}

// Programm encodes values in int and sends them to the serial OUTPUT
// Proximity values can be 0-500 and poti values 1000-1100 (0-100%)
void loop()
{
  // Proximity Sensor
  digitalWrite(triggerPin, LOW);
  delay(5);
  digitalWrite(triggerPin, HIGH);
  delay(10);
  digitalWrite(triggerPin, LOW);
  duration = pulseIn(echoPin, HIGH); 
  distance = (duration/2) * 0.03432;
  if (distance >= 500 || distance <= 0){
      Serial.println("Invalid value read");
  } else{
      Serial.println(distance);
  }

  // Potentiometer
  potiValue = analogRead(potPin);   //Read and save analog value from potentiometer
  potiValue = map(potiValue, 0, 686, 1000, 1100);   // Map value 0-686 to 1000-1100
  Serial.println(potiValue);

  delay(200);
}
