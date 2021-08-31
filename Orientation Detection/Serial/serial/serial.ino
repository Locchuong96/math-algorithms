void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  while (!Serial){
    Serial.println("Wait for the connection");
    delay(1000);
    }
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println("Serial connection success!");
  delay(1000);
}
