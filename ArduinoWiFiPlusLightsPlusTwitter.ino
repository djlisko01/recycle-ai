#include <WiFiNINA.h>
#include "arduino_secrets.h"
#include <ThingSpeak.h>
#include <SPI.h>
#include <LiquidCrystal.h>
//#include <Adafruit_NeoPixel.h> //strip lights


 
// WiFiNINA_Generic - Version: Latest 
/*

*/

char ssid[] = SECRET_SSID;        // Network SSID (name)
char pass[] = SECRET_PASS;        // Network password (use for WPA, or use as key for WEP)
int status = WL_IDLE_STATUS;     // the Wifi radio's status

WiFiClient  client;

// TalkBack
unsigned long myTalkBackID = 45743;
const char * myTalkBackKey = "3MXD0NIV0W0VDVYM";
//Channel
const char * myChannelTalkBackKey = "AM4R84IBHPIZNFLY";
//Twitter API Keys to be used in ThingTweet 
const char * twitterAPIKEY = "SXYXCFX71VYD60K8"; // Semaa's personal twitter account

// LCD setup
// const int rs = 12, en = 10, d4 = 7, d5 = 6, d6 = 5, d7 = 4;
// LiquidCrystal lcd(rs, en, d4, d5, d6, d7);
// Strip setup

// #define PIN 6

// Parameter 1 = number of pixels in strip
// Parameter 2 = pin number (most are valid)
// Parameter 3 = pixel type flags, add together as needed:
//   NEO_KHZ800  800 KHz bitstream (most NeoPixel products w/WS2812 LEDs)
//   NEO_KHZ400  400 KHz (classic 'v1' (not v2) FLORA pixels, WS2811 drivers)
//   NEO_GRB     Pixels are wired for GRB bitstream (most NeoPixel products)
//   NEO_RGB     Pixels are wired for RGB bitstream (v1 FLORA pixels, not v2)
// Adafruit_NeoPixel strip = Adafruit_NeoPixel(60, PIN, NEO_GRB + NEO_KHZ800);

// here we are assigning the Arduino pins on the MKR1010 board to their respective fields. 
// i.e. the trash LED light is connected to pin 0, the Glass is connected to Pin 1 and so far
const int Trash = 0;
const int Glass = 1;
const int Metal = 2;
const int Plastic = 3;
const int Cardboard = 4;
const int Paper = 5;

// initializing the counters for the different bins; to be used in Twitter to avoid repeating tweets
int totalTrash = 0;
int totalGlass = 0;
int totalMetal = 0;
int totalPlastic = 0;
int totalCardboard = 0;
int totalPaper = 0;

int outputResult = 0;     // this is used to update the channel what the outputs of the Jetson Nano are

// mandsotry, built-in Arduino process
void setup() {
  //Initialize serial and wait for port to open:
  Serial.begin(9600);
  while (!Serial);
  
// init lcd
// lcd.begin(16,2);

//  strip.begin();               // initialize strip
//  strip.show();                // Update all LEDs (= turn OFF, since none of them have been set yet!)
  


  

  
  // attempt to connect to Wifi network:
  while (status != WL_CONNECTED) {

    Serial.print("Attempting to connect to network: ");
    Serial.println(ssid);
    // Connect to WPA/WPA2 network:
    status = WiFi.begin(ssid, pass);
    //lcd.write("Connecting");
    // wait 10 seconds for connection:
//    delay(10000);
//    lcd.clear();
  }

  // you're connected now, so print out the data:
  Serial.println("You're connected to the network");

  Serial.println("----------------------------------------");
  printData();
  Serial.println("----------------------------------------");

// stating that the the LED light pins are outputd, not inputs
  pinMode(Trash, OUTPUT);  // Set up LED
  pinMode(Glass, OUTPUT);
  pinMode(Paper, OUTPUT);
  pinMode(Cardboard, OUTPUT);
  pinMode(Metal, OUTPUT);
  pinMode(Plastic, OUTPUT);
  Serial.begin(115200);          // Initialize serial
}

// mandatory Arduino process
void loop() {

  // check the network connection once every 10 seconds:
 delay(10000);
 printData();
 Serial.println("----------------------------------------");

  // Create the TalkBack URI
  String tbURI = String("/talkbacks/") + String(myTalkBackID) + String("/commands/execute");

  // Create the Update Channel and TalkBack URI
  String ch_tbURI = String("/update.json");
  
  // Create the message body for the POST out of the values
  //String postMessage =  String("api_key=") + String(myTalkBackKey);                      
  
   // Create the message body for the POST out of the values
  String postMessage =  String("field1=") + String(outputResult) +
                        String("field2=") + String(outputResult) +
                        String("&api_key=") + String(myChannelTalkBackKey) +
                        String("&talkback_key=") + String(myTalkBackKey);                    
   // Make a string for any commands in the queue
  String newCommand = String();

  // Make a string for any fields in the queue
  String field = String();

  //Make a String for Channel API, different from TalkBack API
  String channel_api_key = String();



  // initialize thingtweet
  postTwitterMssg("");
  
  // Make the POST to ThingSpeak
  int x = httpPOSTChannel(postMessage,newCommand);
  


  // Check  the result
  if(x == 200){
     Serial.println("checking queue..."); 

    // check for a command returned from TalkBack
    if(newCommand.length() != 0){

      Serial.print("  Latest command from queue: ");
      
      for(int i = 0; i < 10; i ++){
         Serial.println(newCommand[i]);
      }

      
      //Recycling Sorting Begins here

        
      /*auto trashColor = strip.Color(255, 0, 0);  // define the variable c as RED (R,G,B)
      auto glassColor = strip.Color(255,255,255); //WHITE
      auto metalColor = strip.Color(241,255,1); //YELLOW
      auto plasticColor = strip.Color(0,0,255);//BLUE
      auto cardboardColor = strip.Color(0,255,0); //GREEN
      auto paperColor = strip.Color(181,182,290); //SILVER*/
      

      
      // Trash = 0 = red light
      if((String)newCommand[3] == "5"){
           //strip.setPixelColor(5, trashColor);  // set LED 10 to the color in variable c (red)
           //strip.show();                // Update all LEDs (= make LED 10 red)
           totalTrash ++;
           outputResult = 0;
           //lcd.write("Trash");
           postTwitterMssg(createStatus("Trash"));
           Serial.print("Trash, ");
           Serial.print("The red light is ON now \n");
           digitalWrite(Trash, HIGH);    // turn on Red LED on Pin 0 
           delay(5000);                  // wait for 5s
           Serial.print("The red light is OFF now \n");
           digitalWrite(Trash, LOW);    // turn off Red LED on Pin 0
           delay(2000);
           //lcd.clear();
           //turnOffAllStripLights();
       }
       // Glass = 1 = purple light
      if((String)newCommand[3] == "1"){
          //strip.setPixelColor(10, glassColor);  // set LED 10 to the color in variable c (red)
          //lcd.write("Glass");
          totalGlass ++;
          postTwitterMssg(createStatus("Glass"));
          outputResult = 1;
          Serial.print("Glass, ");
          Serial.print("The purple light is ON now \n");
          digitalWrite(Glass, HIGH);    // turn on White LED on Pin 1
          delay(5000);                  // wait for 5s
          Serial.print("The purple light is OFF now \n");
          digitalWrite(Glass, LOW);     // turn off Yellow LED on Pin 1
          delay(2000);
          //lcd.clear();
          //turnOffAllStripLights();
       }

      // Metal = 2 = Yellow
      if((String)newCommand[3] == "2"){
          //strip.setPixelColor(15, metalColor);  // set LED 10 to the color in variable c (red)
          //lcd.write("Metal");
          totalMetal ++;
          postTwitterMssg(createStatus("Metal"));
          outputResult = 2;
          Serial.print("Metal, ");
          Serial.print("The yellow light is ON now \n");          
          digitalWrite(Metal, HIGH);    // turn on Yellow LED on Pin 2
          delay(5000);                  // wait for 5s
          Serial.print("The yellow light is OFF now \n"); 
          digitalWrite(Metal, LOW);     // turn off Yellow LED on Pin 2
          delay(2000);
          //lcd.clear();
          //turnOffAllStripLights();
       }
      // Plastic = 3 = Blue
      if((String)newCommand[3] == "4"){
        //strip.setPixelColor(20, plasticColor);  // set LED 10 to the color in variable c (red)
        totalPlastic ++;
        //lcd.write("Plastic");
        postTwitterMssg(createStatus("Plastic"));
        outputResult = 3;
        Serial.print("Plastic, ");
        Serial.print("The blue light is ON now \n");     
        digitalWrite(Plastic, HIGH);    // turn on Blue LED on Pin 3
        delay(5000);                    // wait for 5s
        Serial.print("The blue light is OFF now \n");     
        digitalWrite(Plastic, LOW);     // turn on Blue LED on Pin 3
        delay(2000);
        //lcd.clear();
        //turnOffAllStripLights();
      }

      // Cardboard = 4 = Green
      if((String)newCommand[3] == "0"){
        //strip.setPixelColor(25, cardboardColor);  // set LED 10 to the color in variable c (red)
        totalCardboard ++;
        //lcd.write("Cardboard");
        postTwitterMssg(createStatus("Cardboard"));
        outputResult = 4;
        Serial.print("Cardboard, ");
        Serial.print("The green light is ON now \n");     
        digitalWrite(Cardboard, HIGH);   // turn on Green LED on Pin 4
        delay(5000);                     // wait for 5s
        Serial.print("The green light is OFF now\n");     
        digitalWrite(Cardboard, LOW);    // turn off Green LED on Pin 4
        delay(2000);
        //lcd.clear();
        //turnOffAllStripLights();
       }

      // Paper = 5 = orange 
      if((String)newCommand[3] == "3"){
        //strip.setPixelColor(30, paperColor);  // set LED 10 to the color in variable c (red)
        totalPaper ++;
        //lcd.write("Paper");
        postTwitterMssg(createStatus("Paper"));
        outputResult = 5;
        Serial.print("Paper, ");
        Serial.print("The orange light is ON now \n");     
        digitalWrite(Paper, HIGH);    // turn on Orange LED on Pin 5
        delay(5000);                  // wait for 5s
        Serial.print("The orange light is OFF now \n");     
        digitalWrite(Paper, LOW);     // turn off Orange LED on Pin 5
        delay(2000);
        //lcd.clear();
        //turnOffAllStripLights();
       }

    }
    else{
      Serial.println("  Nothing new.");  
    }
    
  }
  else{
    Serial.println("Problem checking queue. HTTP error code " + String(x));
  }
  
  delay(3000); // Wait 30 seconds to check queue again
}


// General function to POST to ThingSpeak
int httpPOSTChannel(String postMessage, String &response){

  bool connectSuccess = false;
  connectSuccess = client.connect("api.thingspeak.com",80);

  if(!connectSuccess){
      return -301;   
  }
  
  postMessage += "&headers=false";
  
  String Headers =  String("POST /update HTTP/1.1\r\n") +
                    String("Host: api.thingspeak.com\r\n") +
                    String("Content-Type: application/x-www-form-urlencoded\r\n") +
                    String("Connection: close\r\n") +
                    String("Content-Length: ") + String(postMessage.length()) +
                    //String("api_key= ") + String(twitterAPIKEY) +
                    //String("&status=") + String("I+just+posted+this+from+my+Thing!")+
                    String("\r\n\r\n");

  client.print(Headers);
  client.print(postMessage);

  long startWaitForResponseAt = millis();
  while(client.available() == 0 && millis() - startWaitForResponseAt < 5000){
      delay(100);
  }

  if(client.available() == 0){       
    return -304; // Didn't get server response in time
  }

  if(!client.find(const_cast<char *>("HTTP/1.1"))){
      return -303; // Couldn't parse response (didn't find HTTP/1.1)
  }
  
  int status = client.parseInt();
  if(status != 200){
    return status;
  }

  if(!client.find(const_cast<char *>("\n\r\n"))){
    return -303;
  }

  String tempString = String(client.readString());
  response = tempString;
  
  return status;
    
}
void printData() {
  Serial.println("Board Information:");
  // print your board's IP address:
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);

  Serial.println();
  Serial.println("Network Information:");
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  // print the received signal strength:
  long rssi = WiFi.RSSI();
  Serial.print("signal strength (RSSI):");
  Serial.println(rssi);

}

// turning off lightstrip 
//void turnOffAllStripLights(){
//  
//  for(int i = 0; i < 59; i ++){
//    
//    strip.setPixelColor(i, strip.Color(0,0,0));  // set LED 10 to the color in variable c (red)
//    strip.show();
//  }  
//  
//}
String createStatus(String material){
          String message = 
          String("Great News! #EyeRecAIcle just #sorted 1 piece of #")+material+String(" from #NUSFBA. The total waste saved from the landfill to date from that bin is:\n")+
          String("Cardboard:") +  String(totalCardboard) + String(",\n")+
          String("Paper:") +  String(totalPaper) + String(",\n")+
          String("Trash:") +  String(totalTrash) + String(",\n")+
          String("Glass:") +  String(totalGlass) + String(",\n")+
          String("Plastic:") +  String(totalPlastic) + String(",\n")+
          String("Metal:") +  String(totalMetal) + String("\n")+
          String("#Recycle #Environment #Nvidia #Arduino #ThingSpeak #MachineLearning #AI");

          return message;
}
//used to post message to twitter, must be a completly unique message twitter does not allow duplicate posts
void postTwitterMssg(String msg){
  

  bool connectSuccess = false;
  connectSuccess = client.connect("api.thingspeak.com",80);

  msg = "api_key="+String(twitterAPIKEY)+"&status="+ msg;
            
    client.print("POST /apps/thingtweet/1/statuses/update HTTP/1.1\n");
    client.print("Host: api.thingspeak.com\n");
    client.print("Connection: close\n");
    client.print("Content-Type: application/x-www-form-urlencoded\n");
    client.print("Content-Length: ");
    client.print(msg.length());
    client.print("\n\n");

    client.print(msg);
    
  long startWaitForResponseAt = millis();
  while(client.available() == 0 && millis() - startWaitForResponseAt < 5000){
      delay(100);
  }
  
  
  
}
