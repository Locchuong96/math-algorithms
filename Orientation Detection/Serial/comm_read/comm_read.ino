void setup(){
  Serial.begin(115200);
  pinMode(LED_BUILTIN,OUTPUT);
  digitalWrite(LED_BUILTIN,HIGH);
  }

 void loop(){
  String a = "Hello String";

  if(Serial.available()){
    a = Serial.read();
    Serial.print(a);
    if( a == "hello"){
      digitalWrite(LED_BUILTIN,LOW);
      delay(1000);
      digitalWrite(LED_BUILTIN,HIGH);
      }
    }
  }
  
 
