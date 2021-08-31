/*
 * Uses a fo loop to print numbers n various formats
 */

 void setup(){
  Serial.begin(115200);
 }
void loop(){
  // print labels
  Serial.print("NO FORMAT");
  Serial.print("\t");

  Serial.print("DEC");
  Serial.print("\t");

  Serial.print("HEX");
  Serial.print("\t");

  Serial.print("OCT");
  Serial.print("\t");

  Serial.print("BIN");
  Serial.println(); // carriage return after the last label

  for (int x = 0; x <64; x++){
    Serial.print(x);      // print as an ASCII encoded decimal = same as "DEC"
    Serial.print("\t\t"); // prints two tabs to accomodate label lenght

    Serial.print(x,DEC);      // print as an ASCII encoded decimal = same as "DEC"
    Serial.print("\t\t"); // print as tab

    Serial.print(x,HEX);      // print as an ASCII encoded decimal = same as "HEX"
    Serial.print("\t"); // print as tab

    Serial.print(x,OCT);      // print as an ASCII encoded decimal = same as "OCT"
    Serial.print("\t"); // print as tab

    Serial.print(x,BIN);      // print as an ASCII encoded decimal = same as "BIN"
    Serial.print("\t"); // print as tab

    delay(200);
    }
   Serial.println();
  }
  
  
