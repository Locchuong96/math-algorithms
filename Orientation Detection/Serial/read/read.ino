String InBytes;

void setup(){
  Serial.begin(115200);
  pinMode(LED_BUILTIN,OUTPUT);
  digitalWrite(LED_BUILTIN,HIGH);
  }

void loop(){
  if (Serial.available()>0){
    InBytes = Serial.readStringUntil('\n');
    if (InBytes == "on"){
      digitalWrite(LED_BUILTIN,LOW);
      Serial.write("Led on");
      }
    if (InBytes == "off"){
      digitalWrite(LED_BUILTIN,HIGH);
      Serial.write("Led off");
      }
    else{
      Serial.write("Invalid input");
      }
    }
  }

  
