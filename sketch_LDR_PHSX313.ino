const int echoPin = 11;
const int photoresistorPin = A0; // Photoresistor connected to A0
const int buttonPin = 2; // Button connected to digital pin D2

// Constants for light level calculation
const int Rc = 10;              // Calibration resistance in kOhms
const int R0 = 15;              // Light resistance at 10 Lux in kOhms
const float Vcc = 5.0;          // Supply voltage
const float I0 = 10.0;          // Reference illuminance at 10 Lux

void setup() {
  Serial.begin(9600);
  pinMode(echoPin, INPUT);
  pinMode(photoresistorPin, INPUT);
  pinMode(buttonPin, INPUT);
}

void loop() {
  if (digitalRead(buttonPin) == HIGH) {
    // read and calculate distance from UDS
    long duration = pulseIn(echoPin, HIGH); // variable for ultrasonic pulse round-trip time
    float distance = duration * 0.034 / 2; // variable for calculated distance

    // read and convert voltage from photoresistor
    float V_ADC = analogRead(photoresistorPin); // Read the ADC value from the photoresistor
    float V_LDR = (V_ADC * Vcc) / 1023.0;     // Convert ADC value to voltage

    // Calculate resistance of the LDR
    float R = (V_LDR * Rc) / (Vcc - V_LDR);

    // Calculate illuminance using the derived formula
    float I = I0 * sqrt((R / R0));

    // Check if button is released before printing (to avoid bounce in the data)
    if (digitalRead(buttonPin) == LOW) {
      Serial.print("Distance: ");
      Serial.print(distance / 100);
      Serial.print(" m, Light Level: ");
      Serial.print(I);
      Serial.println(" lux");
    }
  }
}
