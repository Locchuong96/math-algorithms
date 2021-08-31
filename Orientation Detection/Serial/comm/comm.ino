void setup(){
  Serial.begin(115200);
  }

 void loop(){
  // int a= 2;
  // send2byte(&a);
  Serial.write(65);
  Serial.write(10);
  delay(100);
  }
  
void send2byte(int* data1){
  byte* bytedata1 = (byte*)(data1);
  byte buf[2]= { bytedata1[0],bytedata1[1] };
  Serial.write(buf,2);
  }
 
