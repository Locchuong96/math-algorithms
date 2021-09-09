#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

#include <Wire.h>
#include <FaBo9Axis_MPU9250.h>

#include <ArduinoJson.h>

/*Put your SSID & Password*/
const char* ssid = "SUNYMAP";  // Enter SSID here
const char* password = "099459060trt";  //Enter Password here

ESP8266WebServer server(80);

// Initialize mpu9250 sensor.
FaBo9Axis fabo_9axis;

float ax,ay,az;
float gx,gy,gz;
float mx,my,mz;
float temp;

long loopTime = 10000;   // microseconds
unsigned long timer = 0;

void setup() {
  Serial.begin(115200);
  delay(100);
 
 // init sensor
 Serial.println("configuring device.");

  if (fabo_9axis.begin()) {
    Serial.println("configured FaBo 9Axis I2C Brick");
  } else {
    Serial.println("device error");
    while(1);
  }           

  Serial.println("Connecting to ");
  Serial.println(ssid);

  //connect to your local wi-fi network
  WiFi.begin(ssid, password);

  //check wi-fi is connected to wi-fi network
  while (WiFi.status() != WL_CONNECTED) {
  delay(1000);
  Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected..!");
  Serial.print("Got IP: ");  Serial.println(WiFi.localIP());

  server.on("/", handle_OnConnect);
  server.onNotFound(handle_NotFound);

  server.begin();
  Serial.println("HTTP server started");

}

void loop() {
  // put your main code here, to run repeatedly:
  server.handleClient();
}

void handle_OnConnect() {

  // Gets the values of the sensor

  timeSync(loopTime);

  fabo_9axis.readAccelXYZ(&ax,&ay,&az);
  fabo_9axis.readGyroXYZ(&gx,&gy,&gz);
  fabo_9axis.readMagnetXYZ(&mx,&my,&mz);
  fabo_9axis.readTemperature(&temp);
  
  String webPage;
  
  // Allocate JsonBuffer
  // Use arduinojson.org/assistant to compute the capacity.
  StaticJsonBuffer<500> jsonBuffer;

  // Create the root object
  JsonObject& root = jsonBuffer.createObject();

  root["ax"] = ax;
  root["ay"] = ay;
  root["az"] = az;
  root["gx"] = gx;
  root["gy"] = gy;
  root["gz"] = gz;
  root["mx"] = mx;
  root["my"] = my;
  root["mz"] = mz;
  root["temp"] = temp;

  root.printTo(webPage);  //Store JSON in String variable
  server.send(200, "text/html", webPage);
}

void handle_NotFound(){
  server.send(404, "text/plain", "Not found");
}

void timeSync(unsigned long deltaT)
{
  unsigned long currTime = micros();
  long timeToDelay = deltaT - (currTime - timer);
  if (timeToDelay > 5000)
  {
    delay(timeToDelay / 1000);
    delayMicroseconds(timeToDelay % 1000);
  }
  else if (timeToDelay > 0)
  {
    delayMicroseconds(timeToDelay);
  }
  else
  {
      // timeToDelay is negative so we start immediately
  }
  timer = currTime + timeToDelay;
}
