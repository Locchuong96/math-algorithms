#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

#include <Wire.h>
#include <FaBo9Axis_MPU9250.h>

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
  
  //send the values
  server.send(200, "text/html", SendHTML(ax,ay,az,gx,gy,gz,mx,my,mz));
}

void handle_NotFound(){
  server.send(404, "text/plain", "Not found");
}

String SendHTML(float ax,float ay, float az,float gx,float gy, float gz,float mx,float my, float mz)
{
  String ptr = "<!DOCTYPE html> <html>\n";
  ptr +="<head><meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0, user-scalable=no\">\n";
  ptr +="<meta http-equiv=\"refresh\", content=\"1\">";
  ptr +="<title>ESP8266 IMU</title>\n";
  ptr +="<style>html { font-family: Helvetica; display: inline-block; margin: 0px auto; text-align: center;}\n";
  ptr +="body{margin-top: 50px;} h1 {color: #444444;margin: 50px auto 30px;}\n";
  ptr +="p {font-size: 24px;color: #444444;margin-bottom: 10px;}\n";
  ptr +="</style>\n";
  ptr +="</head>\n";
  ptr +="<body>\n";
  ptr +="<div id=\"webpage\">\n";
  ptr +="<h1>MPU9250 Report</h1>\n";
  
  ptr +="<p>Acceletation Ax: ";
  ptr +=(float)ax;
  ptr +=" m/s^2</p>";
  
  ptr +="<p>Acceletation Ay: ";
  ptr +=(float)ay;
  ptr +=" m/s^2</p>";

  ptr +="<p>Acceletation Az: ";
  ptr +=(float)az;
  ptr +=" m/s^2</p>";

  ptr +="<p>Gyrometer Gx: ";
  ptr +=(float)gx;
  ptr +=" deg/s</p>";

  ptr +="<p>Gyrometer Gy: ";
  ptr +=(float)gy;
  ptr +=" deg/s</p>";

  ptr +="<p>Gyrometer Gz: ";
  ptr +=(float)gz;
  ptr +=" deg/s</p>";

  ptr +="<p>Magnetor Mx: ";
  ptr +=(float)mx;
  ptr +=" uT</p>";

  ptr +="<p>Magnetor My: ";
  ptr +=(float)my;
  ptr +=" uT</p>";

  ptr +="<p>Magnetor Mz: ";
  ptr +=(float)mz;
  ptr +=" uT</p>";
  
  ptr +="</div>\n";
  ptr +="</body>\n";
  ptr +="</html>\n";
  return ptr;
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
