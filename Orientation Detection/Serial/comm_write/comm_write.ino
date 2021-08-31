float a = 0;
float b = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly:
  a = 1;
  b = a +1;
  sendtoPC(&a,&b);
  Serial.println();
//  Serial.print(a);
//  Serial.print("x");
//  Serial.println(b);
   //delay(1000);
}

void sendtoPC(float* data1, float* data2){
  byte* bytedata1 = (byte*)(data1);
  byte* bytedata2 = (byte*)(data2);
  byte buf[4] = {bytedata1[0],bytedata1[1],
                  bytedata2[0],bytedata2[1]};
  }
