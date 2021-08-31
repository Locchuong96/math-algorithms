int incomingByte = 0;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()>0){
    // Read the incoming byte
    incomingByte = Serial.read();
    // Say what you got
    Serial.print("I received: ");
    Serial.println(incomingByte,OCT); //HEX,DEC,BIN,OCT
  }
}
